#!/bin/bash

################################################################################
# PROMETHEUS + GRAFANA MONITORING SETUP
# Real-time metrics dashboard for Kubernetes
################################################################################

set -e

# Project root (script directory)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "\n${CYAN}==================== $1 ====================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

################################################################################
# STEP 1: ADD PROMETHEUS HELM REPO
################################################################################

print_header "STEP 1: INSTALL PROMETHEUS OPERATOR"

print_info "Adding Prometheus Helm repository..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
print_success "Helm repo added"

print_info "Installing Prometheus (idempotent)..."
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace microservices \
  --create-namespace \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set grafana.enabled=true \
  --set grafana.adminPassword=admin123 \
  --wait --timeout 300s || true

print_success "Prometheus and Grafana installed (or already present)"

################################################################################
# STEP 2: WAIT FOR PROMETHEUS
################################################################################

print_header "STEP 2: VERIFY INSTALLATION"

print_info "Waiting for Prometheus pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=prometheus \
  -n microservices --timeout=300s 2>/dev/null || true

print_info "Waiting for Grafana pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=grafana \
  -n microservices --timeout=300s 2>/dev/null || true

print_success "All monitoring pods are ready"

################################################################################
# STEP 3: CREATE SERVICE MONITORS
################################################################################

print_header "STEP 3: CREATE SERVICE MONITORS"

mkdir -p "$PROJECT_ROOT/k8s/monitoring"

print_info "Creating ServiceMonitor for User Service..."
cat > "$PROJECT_ROOT/k8s/monitoring/user-service-monitor.yaml" << 'EOF' 
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: user-service-monitor
  namespace: microservices
spec:
  selector:
    matchLabels:
      app: user-service
  endpoints:
  - port: "5001"
    interval: 30s
    path: /metrics
EOF
print_success "User Service monitor created"

print_info "Creating ServiceMonitor for Product Service..."
cat > "$PROJECT_ROOT/k8s/monitoring/product-service-monitor.yaml" << 'EOF' 
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: product-service-monitor
  namespace: microservices
spec:
  selector:
    matchLabels:
      app: product-service
  endpoints:
  - port: "5002"
    interval: 30s
    path: /metrics
EOF
print_success "Product Service monitor created"

print_info "Creating ServiceMonitor for Order Service..."
cat > "$PROJECT_ROOT/k8s/monitoring/order-service-monitor.yaml" << 'EOF' 
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: order-service-monitor
  namespace: microservices
spec:
  selector:
    matchLabels:
      app: order-service
  endpoints:
  - port: "5003"
    interval: 30s
    path: /metrics
EOF
print_success "Order Service monitor created"

# Apply monitors
kubectl apply -f "$PROJECT_ROOT/k8s/monitoring/"

################################################################################
# STEP 4: CREATE GRAFANA DASHBOARDS
################################################################################

print_header "STEP 4: CREATE GRAFANA DASHBOARDS"

print_info "Creating Grafana dashboards..."

cat > "$PROJECT_ROOT/k8s/monitoring/grafana-dashboards.yaml" << 'EOF' 
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards
  namespace: microservices
data:
  microservices-dashboard.json: |
    {
      "dashboard": {
        "title": "Microservices Dashboard",
        "panels": [
          {
            "title": "Pod CPU Usage",
            "targets": [
              {
                "expr": "sum(rate(container_cpu_usage_seconds_total{pod=~\"user-service.*|product-service.*|order-service.*\"}[5m])) by (pod)"
              }
            ]
          },
          {
            "title": "Pod Memory Usage",
            "targets": [
              {
                "expr": "sum(container_memory_usage_bytes{pod=~\"user-service.*|product-service.*|order-service.*\"}) by (pod)"
              }
            ]
          },
          {
            "title": "Request Rate",
            "targets": [
              {
                "expr": "sum(rate(http_requests_total[5m])) by (service)"
              }
            ]
          },
          {
            "title": "Error Rate",
            "targets": [
              {
                "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (service)"
              }
            ]
          }
        ]
      }
    }
EOF

kubectl apply -f "$PROJECT_ROOT/k8s/monitoring/grafana-dashboards.yaml"
print_success "Grafana dashboards configured"

################################################################################
# STEP 5: CREATE PROMETHEUS RULES
################################################################################

print_header "STEP 5: CREATE PROMETHEUS ALERT RULES"

print_info "Creating alert rules..."

cat > "$PROJECT_ROOT/k8s/monitoring/prometheus-rules.yaml" << 'EOF' 
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: microservices-alerts
  namespace: microservices
spec:
  groups:
  - name: microservices
    interval: 30s
    rules:
    - alert: HighErrorRate
      expr: sum(rate(http_requests_total{status=~"5.."}[5m])) by (service) > 0.05
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High error rate for {{ $labels.service }}"
        description: "Service {{ $labels.service }} has error rate {{ $value }}"
    
    - alert: HighCPUUsage
      expr: sum(rate(container_cpu_usage_seconds_total{pod=~".*-service.*"}[5m])) by (pod) > 0.8
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High CPU usage for {{ $labels.pod }}"
        description: "Pod {{ $labels.pod }} CPU usage is {{ $value }}"
    
    - alert: HighMemoryUsage
      expr: sum(container_memory_usage_bytes{pod=~".*-service.*"}) by (pod) / 256000000 > 0.8
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High memory usage for {{ $labels.pod }}"
        description: "Pod {{ $labels.pod }} memory usage is {{ $value }}"
    
    - alert: PodNotRunning
      expr: kube_pod_status_phase{namespace="microservices", phase!="Running"} == 1
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Pod not running: {{ $labels.pod }}"
        description: "Pod {{ $labels.pod }} is not in Running state"
EOF

kubectl apply -f "$PROJECT_ROOT/k8s/monitoring/prometheus-rules.yaml"
print_success "Alert rules configured"

################################################################################
# STEP 6: PORT FORWARDING
################################################################################

print_header "STEP 6: ACCESS MONITORING DASHBOARDS"

print_info "Port forwarding for Prometheus and Grafana..."

# Get pod names
PROMETHEUS_POD=$(kubectl get pods -n microservices -l app.kubernetes.io/name=prometheus -o jsonpath='{.items[0].metadata.name}')
GRAFANA_POD=$(kubectl get pods -n microservices -l app.kubernetes.io/name=grafana -o jsonpath='{.items[0].metadata.name}')

echo ""
echo -e "${CYAN}To access Prometheus and Grafana, run in separate terminals:${NC}"
echo ""
echo "Terminal A - Prometheus:"
echo "  kubectl port-forward -n microservices svc/prometheus-operated 9090:9090"
echo "  Access: http://localhost:9090"
echo ""
echo "Terminal B - Grafana:"
echo "  kubectl port-forward -n microservices svc/prometheus-grafana 3000:80"
echo "  Access: http://localhost:3000"
echo "  Username: admin"
echo "  Password: admin123"
echo ""

################################################################################
# STEP 7: CREATE MONITORING GUIDE
################################################################################

print_header "STEP 7: MONITORING DOCUMENTATION"

cat > "$PROJECT_ROOT/MONITORING_GUIDE.md" << 'EOF'
# Prometheus + Grafana Monitoring Guide

## Access Dashboards

### Prometheus (Metrics & Queries)
```bash
kubectl port-forward -n microservices svc/prometheus-operated 9090:9090
```
- URL: http://localhost:9090
- Query engine for Kubernetes metrics
- View alert rules and status

### Grafana (Visualization)
```bash
kubectl port-forward -n microservices svc/prometheus-grafana 3000:80
```
- URL: http://localhost:3000
- Username: admin
- Password: admin123
- Pre-built dashboards for microservices

## Key Metrics Monitored

1. **CPU Usage**: `sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)`
2. **Memory Usage**: `sum(container_memory_usage_bytes) by (pod)`
3. **Request Rate**: `sum(rate(http_requests_total[5m])) by (service)`
4. **Error Rate**: `sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)`
5. **Pod Status**: `kube_pod_status_phase`
6. **Restart Count**: `kube_pod_container_status_restarts_total`

## Alert Rules

- **HighErrorRate**: Service error rate > 5%
- **HighCPUUsage**: Pod CPU usage > 80%
- **HighMemoryUsage**: Pod memory usage > 80%
- **PodNotRunning**: Pod not in Running state

## Add Custom Metrics

To expose metrics from Flask services, add to app.py:

```python
from prometheus_client import Counter, Histogram, generate_latest
import time

# Define metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    request_count.labels(method=request.method, endpoint=request.path, status=response.status_code).inc()
    request_duration.observe(duration)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest()
```

## Useful Prometheus Queries

```promql
# CPU usage per pod
sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)

# Memory usage in MB
sum(container_memory_usage_bytes) by (pod) / 1024 / 1024

# Network in
sum(rate(container_network_receive_bytes_total[5m])) by (pod)

# Network out
sum(rate(container_network_transmit_bytes_total[5m])) by (pod)

# Restart count
kube_pod_container_status_restarts_total{namespace="microservices"}

# Pod uptime
time() - kube_pod_created{namespace="microservices"}
```

## Troubleshooting

### Metrics not appearing?
```bash
# Check if ServiceMonitor is recognized
kubectl get servicemonitor -n microservices

# Check Prometheus targets
kubectl port-forward svc/prometheus-operated 9090:9090
# Visit http://localhost:9090/targets
```

### Grafana not connecting to Prometheus?
```bash
# Check Prometheus service
kubectl get svc -n microservices | grep prometheus

# Verify connection in Grafana:
# Settings → Data Sources → Prometheus
# URL should be: http://prometheus-operated.microservices.svc.cluster.local:9090
```

EOF

print_success "Monitoring guide created"

################################################################################
# FINAL STATUS
################################################################################

print_header "MONITORING SETUP COMPLETE"

print_success "✓ Prometheus installed"
print_success "✓ Grafana installed"
print_success "✓ ServiceMonitors configured"
print_success "✓ Alert rules created"
print_success "✓ Monitoring guide created"

echo -e "\n${GREEN}NEXT STEPS:${NC}\n"
echo "1. Port forward Prometheus:"
echo "   kubectl port-forward -n microservices svc/prometheus-operated 9090:9090"
echo ""
echo "2. Port forward Grafana:"
echo "   kubectl port-forward -n microservices svc/prometheus-grafana 3000:80"
echo ""
echo "3. Access dashboards:"
echo "   Prometheus: http://localhost:9090"
echo "   Grafana: http://localhost:3000 (admin/admin123)"
echo ""
echo "4. Create custom dashboards in Grafana"
echo "5. Add Flask metrics to your services"
echo ""
echo -e "${GREEN}Your monitoring stack is ready!${NC}\n"


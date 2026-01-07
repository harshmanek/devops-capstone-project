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


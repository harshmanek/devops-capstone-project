# DevOps Capstone Project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.34.0-blue)](https://kubernetes.io/)
[![Python](https://img.shields.io/badge/Python-3.12-green)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-28.4.0-blue)](https://www.docker.com/)

A production-ready, cloud-native microservices architecture demonstrating modern DevOps practices with containerization, Kubernetes orchestration, CI/CD automation, and comprehensive monitoring.

## 🚀 Quick Start

### Prerequisites

- Linux (Ubuntu/Pop!\_OS/Debian)
- Docker 28.0+
- kubectl 1.30+
- Minikube 1.37+
- Python 3.12+

### Automated Setup (Recommended)

```bash
# Clone and setup
git clone <repository-url>
cd devops-capstone-project

# Run interactive setup wizard
chmod +x COMPLETION_WIZARD.sh
./COMPLETION_WIZARD.sh
```

### Manual Setup

```bash
# Start Minikube
minikube start --driver=docker --cpus=4 --memory=4096
eval $(minikube docker-env)

# Build and deploy
docker build -t user-service:1.0 ./services/user-service
docker build -t product-service:1.0 ./services/product-service
docker build -t order-service:1.0 ./services/order-service

kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/mysql-configmap.yaml
kubectl apply -f k8s/mysql-secret.yaml
kubectl apply -f k8s/mysql-pvc.yaml
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml
kubectl apply -f k8s/user-service-deployment.yaml
kubectl apply -f k8s/user-service-service.yaml
kubectl apply -f k8s/product-service-deployment.yaml
kubectl apply -f k8s/product-service-service.yaml
kubectl apply -f k8s/order-service-deployment.yaml
kubectl apply -f k8s/order-service-service.yaml

# Initialize database
MYSQL_POD=$(kubectl get pods -n microservices -l app=mysql -o jsonpath='{.items[0].metadata.name}')
kubectl exec -i -n microservices $MYSQL_POD -- mysql -uroot -proot -h127.0.0.1 < init-db.sql

# Port forward services
kubectl port-forward -n microservices svc/user-service 5001:5001 &
kubectl port-forward -n microservices svc/product-service 5002:5002 &
kubectl port-forward -n microservices svc/order-service 5003:5003 &

# Run tests
bash test_all_services.sh
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              Kubernetes Cluster (Minikube)          │
├─────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ User Service │  │Product Svc  │  │ Order Service│ │
│  │  (2 replicas)│  │ (2 replicas)│  │ (3 replicas)│ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                  │        │
│         └─────────────────┼──────────────────┘        │
│                           │                           │
│                    ┌──────▼──────┐                    │
│                    │  MySQL DB   │                    │
│                    │ (PVC: 5Gi)  │                    │
│                    └─────────────┘                    │
│                                                     │
│  ┌──────────────────┐  ┌──────────────────┐        │
│  │  Prometheus      │  │    Grafana       │        │
│  │  (Monitoring)    │  │  (Dashboards)    │        │
│  └──────────────────┘  └──────────────────┘        │
└─────────────────────────────────────────────────────┘
```

## 📦 Services

### User Service (Port 5001)

- User registration and authentication
- Profile management
- JWT-based security

### Product Service (Port 5002)

- Product catalog management
- Inventory tracking
- Price management

### Order Service (Port 5003)

- Order processing and lifecycle
- Inter-service communication
- Stock validation and updates

## 🛠️ Technology Stack

| Component            | Technology           | Version |
| -------------------- | -------------------- | ------- |
| **Runtime**          | Python Flask         | 3.0+    |
| **Database**         | MySQL                | 8.0     |
| **Orchestration**    | Kubernetes           | 1.34.0  |
| **Containerization** | Docker               | 28.4.0  |
| **CI/CD**            | GitHub Actions       | Native  |
| **Monitoring**       | Prometheus + Grafana | Latest  |

## 📚 Documentation

For comprehensive documentation including:

- Detailed API specifications
- Database schema
- Configuration management
- Security considerations
- Troubleshooting guides
- Performance optimization

Please see: **[DETAILED_PROJECT_DOCUMENTATION.md](DETAILED_PROJECT_DOCUMENTATION.md)**

## 🧪 Testing

Run the comprehensive test suite:

```bash
bash test_all_services.sh
```

Tests include:

- Service health checks
- CRUD operations
- Inter-service communication
- Error handling
- Data integrity validation

## 📊 Monitoring

Access monitoring dashboards:

```bash
# Grafana (admin/admin)
kubectl port-forward -n microservices svc/grafana 3000:3000

# Prometheus
kubectl port-forward -n microservices svc/prometheus 9090:9090
```

## 🔧 Development

### Code Quality

```bash
# Install development dependencies
pip install black flake8 isort pytest

# Run code quality checks
black .
flake8 .
isort .
```

### Local Development

```bash
# Start services with docker-compose
docker-compose up -d

# Run individual service
cd services/user-service
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: [Detailed Docs](DETAILED_PROJECT_DOCUMENTATION.md)

---

**Status**: ✅ Production Ready | **Last Updated**: March 15, 2026 | **Version**: 1.0.0

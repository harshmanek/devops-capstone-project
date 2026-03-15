# DevOps Capstone Project - Comprehensive Technical Documentation

## 📋 Executive Summary

This document provides complete technical documentation for the **DevOps Microservices Capstone Project**, a production-ready, cloud-native application demonstrating modern DevOps practices. The project implements a three-tier microservices architecture with containerization, Kubernetes orchestration, CI/CD automation, and comprehensive monitoring.

**Project Status:** ✅ Production Ready  
**Last Updated:** March 15, 2026  
**Version:** 1.0.0

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    External Users & Systems                         │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                    Load Balancer / Ingress                      │ │
│  └─────────────────────┬───────────────────────────────────────────┘ │
│                        │                                           │
│  ┌─────────────────────▼───────────────────────────────────────────┐ │
│  │              Kubernetes Cluster (Minikube)                     │ │
│  │                                                                 │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │            Application Layer (Microservices)               │ │ │
│  │  │                                                             │ │ │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │ │
│  │  │  │ User Service│ │Product Svc │ │ Order Svc   │           │ │ │
│  │  │  │ (2 replicas)│ │(2 replicas)│ │(3 replicas) │           │ │ │
│  │  │  │ Port: 5001  │ │Port: 5002  │ │Port: 5003   │           │ │ │
│  │  │  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘           │ │ │
│  │  │         │               │               │                   │ │ │
│  │  └─────────┼───────────────┼───────────────┼───────────────────┘ │ │
│  │           │               │               │                     │ │
│  │  ┌────────▼───────────────▼───────────────▼───────────────────┐ │ │
│  │  │                Data Layer (MySQL)                          │ │ │
│  │  │  - StatefulSet with PersistentVolumeClaim (5Gi)           │ │ │
│  │  │  - ConfigMaps for configuration                            │ │ │
│  │  │  │  - Secrets for credentials                              │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  │                                                                 │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │            Observability Layer                              │ │ │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │ │
│  │  │  │ Prometheus  │ │  Grafana   │ │ AlertManager│           │ │ │
│  │  │  │ (Metrics)   │ │(Dashboards) │ │ (Alerts)    │           │ │ │
│  │  │  └─────────────┘ └─────────────┘ └─────────────┘           │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                CI/CD Pipeline (GitHub Actions)                   │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │ │
│  │  │ Code Quality│ │Build & Test│ │Security Scan│ │Deploy to K8s│ │ │
│  │  │ (Linting)   │ │(Unit Tests) │ │(Vulnerabilities)│(Auto-deploy)│ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────┘
```

### Component Details

#### Application Services

- **User Service**: Manages user accounts, authentication, and profile data
- **Product Service**: Handles product catalog, inventory, and pricing
- **Order Service**: Processes orders, coordinates with User and Product services

#### Data Layer

- **MySQL 8.0**: Primary database with persistent storage
- **Persistent Volume**: 5Gi storage with automatic provisioning
- **Backup Strategy**: Volume snapshots (not implemented in this demo)

#### Infrastructure

- **Kubernetes**: Container orchestration platform
- **Minikube**: Local Kubernetes cluster for development
- **Docker**: Container runtime and image management

#### Observability

- **Prometheus**: Metrics collection and alerting
- **Grafana**: Dashboard visualization
- **AlertManager**: Alert routing and notification

---

## 🛠️ Technology Stack

### Core Technologies

| Component               | Technology     | Version | Purpose                |
| ----------------------- | -------------- | ------- | ---------------------- |
| **Application Runtime** | Python         | 3.12    | Backend services       |
| **Web Framework**       | Flask          | 3.0+    | REST API development   |
| **ORM**                 | SQLAlchemy     | 2.0+    | Database abstraction   |
| **Database**            | MySQL          | 8.0     | Data persistence       |
| **Container Runtime**   | Docker         | 28.4.0  | Containerization       |
| **Orchestration**       | Kubernetes     | 1.34.0  | Container management   |
| **CI/CD**               | GitHub Actions | Native  | Automation pipeline    |
| **Monitoring**          | Prometheus     | Latest  | Metrics collection     |
| **Visualization**       | Grafana        | Latest  | Dashboard creation     |
| **Version Control**     | Git            | 2.x     | Source code management |

### Development Tools

| Tool           | Purpose         | Configuration      |
| -------------- | --------------- | ------------------ |
| **Black**      | Code formatting | Line length: 88    |
| **Flake8**     | Linting         | Max complexity: 10 |
| **isort**      | Import sorting  | Profile: black     |
| **pytest**     | Testing         | Coverage: 80%+     |
| **pre-commit** | Git hooks       | Auto-formatting    |

### Infrastructure as Code

| Tool               | Purpose            | Files                     |
| ------------------ | ------------------ | ------------------------- |
| **Docker**         | Container images   | `Dockerfile` per service  |
| **Kubernetes**     | Orchestration      | `k8s/*.yaml`              |
| **Helm**           | Package management | Monitoring stack          |
| **GitHub Actions** | CI/CD              | `.github/workflows/*.yml` |

---

## 📋 Prerequisites

### System Requirements

#### Hardware Requirements

- **CPU**: 4+ cores (recommended for Minikube)
- **RAM**: 8GB+ (4GB for Minikube + 4GB for services)
- **Storage**: 20GB+ free disk space
- **Network**: Stable internet connection

#### Software Requirements

##### Core Dependencies

```bash
# Operating System
Ubuntu 20.04+ / Pop!_OS / Debian-based Linux distribution

# Container Runtime
Docker Engine 28.0+
kubectl 1.30+
minikube 1.37+

# Development Tools
Python 3.12+
pip 23.0+
git 2.30+
```

##### Verification Commands

```bash
# Check versions
docker --version          # Docker version 28.2.2+
kubectl version --client  # Client Version: v1.30.14+
minikube version          # minikube version: v1.37.0+
python3 --version         # Python 3.12.x
```

### Environment Setup

#### 1. Install Docker

```bash
# Update package index
sudo apt update

# Install Docker
sudo apt install -y docker.io

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (logout/login required)
sudo usermod -aG docker $USER
```

#### 2. Install kubectl

```bash
# Download kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify installation
kubectl version --client
```

#### 3. Install Minikube

```bash
# Download Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# Install Minikube
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify installation
minikube version
```

#### 4. Install Python Dependencies

```bash
# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Install development tools
pip3 install black flake8 isort pytest coverage
```

---

## 🚀 Quick Start Guide

### Option 1: Automated Setup (Recommended)

Use the interactive completion wizard for guided setup:

```bash
# Make script executable
chmod +x COMPLETION_WIZARD.sh

# Run the wizard
./COMPLETION_WIZARD.sh
```

The wizard will:

- Start Minikube cluster
- Build Docker images
- Deploy Kubernetes manifests
- Initialize database
- Set up monitoring
- Run comprehensive tests

### Option 2: Manual Setup

#### Step 1: Start Minikube

```bash
# Start Minikube with adequate resources
minikube start --driver=docker --cpus=4 --memory=4096

# Configure Docker environment
eval $(minikube docker-env)
```

#### Step 2: Build Docker Images

```bash
# Build all service images
docker build -t user-service:1.0 ./services/user-service
docker build -t product-service:1.0 ./services/product-service
docker build -t order-service:1.0 ./services/order-service
```

#### Step 3: Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy MySQL infrastructure
kubectl apply -f k8s/mysql-configmap.yaml
kubectl apply -f k8s/mysql-secret.yaml
kubectl apply -f k8s/mysql-pvc.yaml
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml

# Wait for MySQL readiness
kubectl wait --for=condition=ready pod -l app=mysql -n microservices --timeout=120s

# Deploy microservices
kubectl apply -f k8s/user-service-deployment.yaml
kubectl apply -f k8s/user-service-service.yaml
kubectl apply -f k8s/product-service-deployment.yaml
kubectl apply -f k8s/product-service-service.yaml
kubectl apply -f k8s/order-service-deployment.yaml
kubectl apply -f k8s/order-service-service.yaml
```

#### Step 4: Initialize Database

```bash
# Get MySQL pod name
MYSQL_POD=$(kubectl get pods -n microservices -l app=mysql -o jsonpath='{.items[0].metadata.name}')

# Initialize database schema
kubectl exec -i -n microservices $MYSQL_POD -- mysql -uroot -proot -h127.0.0.1 < init-db.sql
```

#### Step 5: Enable Local Access

```bash
# Port forward services
kubectl port-forward -n microservices svc/user-service 5001:5001 &
kubectl port-forward -n microservices svc/product-service 5002:5002 &
kubectl port-forward -n microservices svc/order-service 5003:5003 &

# Access Grafana (if monitoring deployed)
kubectl port-forward -n microservices svc/grafana 3000:3000 &
```

#### Step 6: Verify Deployment

```bash
# Check pod status
kubectl get pods -n microservices

# Run comprehensive tests
bash test_all_services.sh
```

### Option 3: Production Deployment with GHCR

#### Prerequisites

- GitHub repository with GitHub Container Registry (GHCR) access
- GitHub Personal Access Token with `packages:write` scope
- Repository secrets configured

#### Deployment Steps

1. Push code to GitHub repository
2. GitHub Actions will automatically:
   - Build Docker images
   - Run tests and linting
   - Push images to GHCR
   - Deploy to Kubernetes (if configured)

#### Manual GHCR Deployment

```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build and push images
docker build -t ghcr.io/USERNAME/repo/user-service:latest ./services/user-service
docker push ghcr.io/USERNAME/repo/user-service:latest

# Update Kubernetes manifests to use GHCR images
kubectl apply -f k8s/user-service-deployment-ghcr.yaml
```

---

## 📚 API Documentation

### User Service API (Port 5001)

#### Authentication

All endpoints except `/health` require authentication for production use.

#### Endpoints

##### Create User

```http
POST /users
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201):**

```json
{
  "message": "User created successfully",
  "user": {
    "id": "uuid-string",
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2026-03-15T10:00:00",
    "updated_at": "2026-03-15T10:00:00"
  }
}
```

##### List Users

```http
GET /users?page=1&per_page=10
```

**Response (200):**

```json
{
  "current_page": 1,
  "pages": 1,
  "per_page": 10,
  "total": 2,
  "users": [
    {
      "id": "uuid-string",
      "username": "johndoe",
      "email": "john@example.com",
      "created_at": "2026-03-15T10:00:00",
      "updated_at": "2026-03-15T10:00:00"
    }
  ]
}
```

##### Get User Details

```http
GET /users/{user_id}
```

**Response (200):**

```json
{
  "id": "uuid-string",
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2026-03-15T10:00:00",
  "updated_at": "2026-03-15T10:00:00"
}
```

##### Update User

```http
PUT /users/{user_id}
Content-Type: application/json

{
  "email": "john.doe@example.com"
}
```

**Response (200):**

```json
{
  "message": "User updated successfully",
  "user": {
    "id": "uuid-string",
    "username": "johndoe",
    "email": "john.doe@example.com",
    "updated_at": "2026-03-15T10:05:00"
  }
}
```

##### Delete User

```http
DELETE /users/{user_id}
```

**Response (200):**

```json
{
  "message": "User deleted successfully"
}
```

##### User Login

```http
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (200):**

```json
{
  "message": "Login successful",
  "user": {
    "id": "uuid-string",
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

##### Health Check

```http
GET /health
```

**Response (200):**

```json
{
  "service": "User Service",
  "status": "healthy",
  "timestamp": "2026-03-15T10:00:00.000000"
}
```

### Product Service API (Port 5002)

#### Endpoints

##### Create Product

```http
POST /products
Content-Type: application/json

{
  "name": "Gaming Laptop",
  "description": "High-performance gaming laptop",
  "price": 1299.99,
  "stock_quantity": 10
}
```

**Response (201):**

```json
{
  "message": "Product created successfully",
  "product": {
    "id": "uuid-string",
    "name": "Gaming Laptop",
    "description": "High-performance gaming laptop",
    "price": 1299.99,
    "stock_quantity": 10,
    "created_at": "2026-03-15T10:00:00",
    "updated_at": "2026-03-15T10:00:00"
  }
}
```

##### List Products

```http
GET /products?page=1&per_page=10
```

**Response (200):**

```json
{
  "current_page": 1,
  "pages": 1,
  "per_page": 10,
  "products": [
    {
      "id": "uuid-string",
      "name": "Gaming Laptop",
      "description": "High-performance gaming laptop",
      "price": 1299.99,
      "stock_quantity": 10,
      "created_at": "2026-03-15T10:00:00",
      "updated_at": "2026-03-15T10:00:00"
    }
  ],
  "total": 1
}
```

##### Get Product Details

```http
GET /products/{product_id}
```

##### Update Product

```http
PUT /products/{product_id}
Content-Type: application/json

{
  "price": 1399.99,
  "stock_quantity": 15
}
```

##### Delete Product

```http
DELETE /products/{product_id}
```

##### Health Check

```http
GET /health
```

### Order Service API (Port 5003)

#### Endpoints

##### Create Order

```http
POST /orders
Content-Type: application/json

{
  "user_id": "user-uuid",
  "product_id": "product-uuid",
  "quantity": 2
}
```

**Response (201):**

```json
{
  "message": "Order created successfully",
  "order": {
    "id": "uuid-string",
    "user_id": "user-uuid",
    "product_id": "product-uuid",
    "quantity": 2,
    "status": "pending",
    "total_price": 2599.98,
    "created_at": "2026-03-15T10:00:00",
    "updated_at": "2026-03-15T10:00:00"
  },
  "user": {
    "id": "user-uuid",
    "username": "johndoe",
    "email": "john@example.com"
  },
  "product": {
    "id": "product-uuid",
    "name": "Gaming Laptop",
    "price": 1299.99,
    "stock_quantity": 8
  }
}
```

##### List Orders

```http
GET /orders?page=1&per_page=10
```

##### Get Order Details

```http
GET /orders/{order_id}
```

##### Update Order Status

```http
PUT /orders/{order_id}
Content-Type: application/json

{
  "status": "confirmed"
}
```

##### Delete Order

```http
DELETE /orders/{order_id}
```

##### Get User Orders

```http
GET /orders/user/{user_id}
```

##### Health Check

```http
GET /health
```

---

## 🗄️ Database Schema

### Complete Schema

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS microservices_db;
USE microservices_db;

-- Users table
CREATE TABLE users (
  id VARCHAR(36) PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_username (username),
  INDEX idx_email (email),
  INDEX idx_created_at (created_at)
);

-- Products table
CREATE TABLE products (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_name (name),
  INDEX idx_price (price),
  INDEX idx_created_at (created_at)
);

-- Orders table
CREATE TABLE orders (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  product_id VARCHAR(36) NOT NULL,
  quantity INT NOT NULL CHECK (quantity > 0),
  status ENUM('pending', 'confirmed', 'shipped', 'cancelled') DEFAULT 'pending',
  total_price DECIMAL(10,2) NOT NULL CHECK (total_price >= 0),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  INDEX idx_user_id (user_id),
  INDEX idx_product_id (product_id),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
);
```

### Indexes and Constraints

#### Performance Indexes

- **Users**: username, email, created_at
- **Products**: name, price, created_at
- **Orders**: user_id, product_id, status, created_at

#### Data Integrity Constraints

- **Price**: Must be >= 0
- **Stock Quantity**: Must be >= 0
- **Order Quantity**: Must be > 0
- **Foreign Keys**: Cascade delete for referential integrity
- **Unique Constraints**: Username and email uniqueness

### Database Configuration

#### MySQL Configuration (ConfigMap)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mysql-config
  namespace: microservices
data:
  MYSQL_DATABASE: "microservices_db"
  MYSQL_USER: "devops_user"
  MYSQL_ROOT_PASSWORD: "root_password_123"
```

#### Connection Settings

- **Host**: mysql.microservices.svc.cluster.local
- **Port**: 3306
- **Charset**: utf8mb4
- **Collation**: utf8mb4_unicode_ci
- **Connection Pool**: 10 connections per service

---

## ⚙️ Configuration Management

### Environment Variables

#### User Service Configuration

```python
# config.py
import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql.microservices.svc.cluster.local')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'devops_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'microservices_db')

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')

    # Pagination
    USERS_PER_PAGE = int(os.getenv('USERS_PER_PAGE', 10))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

#### Product Service Configuration

```python
class Config:
    # Database settings (same as User Service)
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql.microservices.svc.cluster.local')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'devops_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'microservices_db')

    # Product-specific settings
    PRODUCTS_PER_PAGE = int(os.getenv('PRODUCTS_PER_PAGE', 10))
    MIN_STOCK_ALERT = int(os.getenv('MIN_STOCK_ALERT', 5))

    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

#### Order Service Configuration

```python
class Config:
    # Database settings (same as above)
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql.microservices.svc.cluster.local')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'devops_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'microservices_db')

    # Service URLs
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service.microservices.svc.cluster.local:5001')
    PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product-service.microservices.svc.cluster.local:5002')

    # Order settings
    ORDERS_PER_PAGE = int(os.getenv('ORDERS_PER_PAGE', 10))
    DEFAULT_ORDER_STATUS = os.getenv('DEFAULT_ORDER_STATUS', 'pending')

    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

### Kubernetes Secrets

#### MySQL Credentials Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
  namespace: microservices
type: Opaque
data:
  MYSQL_ROOT_PASSWORD: cm9vdF9wYXNzd29yZF8xMjM= # base64 encoded
  MYSQL_PASSWORD: ZGV2b3BzX3Bhc3N3b3JkXzEyMw== # base64 encoded
```

#### Application Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: microservices
type: Opaque
data:
  SECRET_KEY: ZGV2LXNlY3JldC1rZXk= # base64 encoded
  JWT_SECRET_KEY: androgenicdC1zZWNyZXQta2V5 # base64 encoded
```

---

## 🐳 Containerization

### Dockerfile Structure

#### Multi-Stage Build Pattern

```dockerfile
# Build stage
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
EXPOSE 5001
CMD ["python", "app.py"]
```

### Image Optimization

#### Build Optimizations

- **Multi-stage builds**: Separate build and runtime stages
- **Dependency caching**: Install dependencies before copying source code
- **Layer caching**: Order COPY commands for optimal caching
- **Minimal base images**: Use slim Python images

#### Runtime Optimizations

- **Non-root user**: Run as non-privileged user (not implemented in demo)
- **Read-only filesystem**: Mount volumes as read-only where possible
- **Resource limits**: CPU and memory constraints in Kubernetes

### Image Specifications

| Service         | Base Image       | Size  | Build Time | Layers    |
| --------------- | ---------------- | ----- | ---------- | --------- |
| User Service    | python:3.12-slim | ~45MB | ~2min      | 12 layers |
| Product Service | python:3.12-slim | ~45MB | ~2min      | 12 layers |
| Order Service   | python:3.12-slim | ~45MB | ~2min      | 12 layers |

---

## ☸️ Kubernetes Orchestration

### Cluster Architecture

#### Namespace Isolation

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: microservices
  labels:
    name: microservices
```

#### Resource Specifications

| Component       | Replicas | CPU Request | CPU Limit | Memory Request | Memory Limit |
| --------------- | -------- | ----------- | --------- | -------------- | ------------ |
| User Service    | 2        | 100m        | 200m      | 128Mi          | 256Mi        |
| Product Service | 2        | 100m        | 200m      | 128Mi          | 256Mi        |
| Order Service   | 3        | 100m        | 200m      | 128Mi          | 256Mi        |
| MySQL           | 1        | 250m        | 500m      | 256Mi          | 512Mi        |

### Health Checks

#### Liveness Probes

```yaml
livenessProbe:
  tcpSocket:
    port: 3306
  initialDelaySeconds: 60
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 6
```

#### Readiness Probes

```yaml
readinessProbe:
  tcpSocket:
    port: 3306
  initialDelaySeconds: 30
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

### Persistent Storage

#### PVC Specification

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
  namespace: microservices
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

### Service Discovery

#### ClusterIP Services

```yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: microservices
spec:
  selector:
    app: user-service
  ports:
    - port: 5001
      targetPort: 5001
  type: ClusterIP
```

### Deployment Strategy

#### Rolling Updates

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

#### Code Quality Workflow (`.github/workflows/code-quality.yml`)

```yaml
name: Code Quality
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          pip install black flake8 isort
      - name: Run linting
        run: |
          black --check .
          flake8 .
          isort --check-only .
```

#### Build and Test Workflow (`.github/workflows/devops-pipeline.yml`)

```yaml
name: DevOps Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root_password_123
          MYSQL_DATABASE: microservices_db
        ports:
          - 3306:3306
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          pip install -r services/user-service/requirements.txt
          pip install pytest
      - name: Run tests
        run: |
          python -m pytest services/user-service/tests/ -v
```

#### API Tests Workflow (`.github/workflows/api-tests.yml`)

```yaml
name: API Integration Tests
on:
  schedule:
    - cron: "0 */6 * * *" # Every 6 hours
  workflow_dispatch:

jobs:
  api-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Minikube
        run: |
          curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
          sudo install minikube-linux-amd64 /usr/local/bin/minikube
          minikube start --driver=docker
      - name: Deploy to Minikube
        run: |
          eval $(minikube docker-env)
          docker build -t user-service:test ./services/user-service
          kubectl apply -f k8s/namespace.yaml
          # ... deployment steps
      - name: Run API tests
        run: |
          bash test_all_services.sh
```

### Pipeline Stages

#### 1. Code Quality Gate

- **Black**: Code formatting
- **Flake8**: Linting and style checking
- **isort**: Import sorting
- **pre-commit**: Git hook validation

#### 2. Build Stage

- **Docker build**: Multi-stage image creation
- **Security scanning**: Vulnerability checks
- **Image optimization**: Layer caching and size reduction

#### 3. Test Stage

- **Unit tests**: Service-level testing
- **Integration tests**: API endpoint validation
- **Performance tests**: Load testing (not implemented)

#### 4. Deploy Stage

- **Image push**: To GitHub Container Registry
- **Kubernetes deploy**: Rolling updates
- **Health checks**: Post-deployment validation

---

## 📊 Monitoring & Observability

### Prometheus Configuration

#### Service Monitors

```yaml
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
    - port: http
      path: /metrics
      interval: 30s
```

#### Alert Rules

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: microservices-alerts
  namespace: microservices
spec:
  groups:
    - name: microservices
      rules:
        - alert: HighErrorRate
          expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High error rate detected"
```

### Grafana Dashboards

#### Key Metrics Dashboard

- **Service Health**: Uptime and response times
- **Resource Usage**: CPU, memory, and disk utilization
- **Error Rates**: HTTP status codes and error counts
- **Business Metrics**: Order volume, user registrations

#### Custom Panels

```json
{
  "title": "Service Response Time",
  "type": "graph",
  "targets": [
    {
      "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
      "legendFormat": "{{service}}"
    }
  ]
}
```

### Logging Strategy

#### Application Logs

- **Structured logging**: JSON format with consistent fields
- **Log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Correlation IDs**: Request tracing across services

#### Infrastructure Logs

- **Container logs**: Captured by Kubernetes
- **System logs**: Node-level monitoring
- **Audit logs**: Security events and access patterns

---

## 🔒 Security Considerations

### Container Security

#### Image Security

- **Base image scanning**: Vulnerability checks
- **Minimal attack surface**: Slim base images
- **No privileged containers**: Non-root execution
- **Image signing**: GPG signature verification

#### Runtime Security

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```

### Network Security

#### Service Mesh (Future Implementation)

- **mTLS**: Mutual TLS encryption
- **Traffic policies**: Rate limiting and circuit breakers
- **Service authentication**: JWT token validation

#### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: microservices
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-internal
  namespace: microservices
spec:
  podSelector:
    matchLabels:
      app: user-service
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: order-service
      ports:
        - protocol: TCP
          port: 5001
```

### Data Security

#### Database Security

- **Encrypted connections**: TLS 1.3 for MySQL
- **Password hashing**: bcrypt for user passwords
- **Access controls**: Least privilege principle
- **Audit logging**: Database access monitoring

#### Secret Management

- **Kubernetes Secrets**: Base64 encoded credentials
- **Environment separation**: Different secrets per environment
- **Rotation policy**: Regular credential updates

### API Security

#### Authentication & Authorization

- **JWT tokens**: Stateless authentication
- **Role-based access**: User permission levels
- **API rate limiting**: Prevent abuse
- **Input validation**: SQL injection prevention

---

## 🧪 Testing Strategy

### Test Categories

#### Unit Tests

```python
# tests/test_user_model.py
import pytest
from models import User

def test_user_creation():
    user = User(username="testuser", email="test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_user_password_hashing():
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    assert user.check_password("password123")
    assert not user.check_password("wrongpassword")
```

#### Integration Tests

```bash
# test_all_services.sh excerpt
echo "→ Creating Order 1 (User 1 buys 2x Laptop)..."
ORDER1=$(curl -s -X POST "$ORDER_API/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "'$USER1_ID'",
    "product_id": "'$PRODUCT1_ID'",
    "quantity": 2
  }')

# Validate order creation
ORDER1_ID=$(echo $ORDER1 | jq -r '.order.id')
if [ "$ORDER1_ID" = "null" ] || [ -z "$ORDER1_ID" ]; then
    print_error "Order creation failed"
    exit 1
fi
```

#### End-to-End Tests

- **User registration flow**: Complete user lifecycle
- **Order placement flow**: Full order processing
- **Inventory management**: Stock level validation
- **Cross-service communication**: Inter-service calls

### Test Coverage

#### Code Coverage Targets

- **Unit tests**: 80%+ coverage
- **Integration tests**: All API endpoints
- **E2E tests**: Critical user journeys

#### Performance Benchmarks

- **Response time**: <200ms for API calls
- **Throughput**: 1000+ requests/minute
- **Error rate**: <1% under normal load

---

## 🚨 Troubleshooting Guide

### Common Issues

#### Minikube Issues

**Problem**: Minikube fails to start

```bash
# Solution: Clean up and restart
minikube delete
minikube start --driver=docker --cpus=4 --memory=4096
```

**Problem**: kubectl cannot connect to cluster

```bash
# Solution: Update kubeconfig
kubectl config use-context minikube
```

#### Database Issues

**Problem**: MySQL pod not ready

```bash
# Check pod status
kubectl get pods -n microservices -l app=mysql

# Check logs
kubectl logs -n microservices mysql-pod-name

# Check PVC status
kubectl get pvc -n microservices
```

**Problem**: Connection refused

```bash
# Verify service exists
kubectl get svc -n microservices mysql

# Check endpoints
kubectl get endpoints -n microservices mysql
```

#### Service Issues

**Problem**: Service pods crashing

```bash
# Check pod logs
kubectl logs -n microservices -l app=user-service --tail=50

# Check resource usage
kubectl top pods -n microservices

# Describe pod for events
kubectl describe pod pod-name -n microservices
```

**Problem**: Service not accessible

```bash
# Check service endpoints
kubectl get endpoints -n microservices user-service

# Test internal connectivity
kubectl exec -n microservices user-service-pod -- curl http://localhost:5001/health
```

### Debug Commands

#### Cluster Diagnostics

```bash
# Cluster info
kubectl cluster-info

# Node status
kubectl get nodes

# All resources
kubectl get all -n microservices

# Events
kubectl get events -n microservices --sort-by=.metadata.creationTimestamp
```

#### Application Debugging

```bash
# Port forward for local testing
kubectl port-forward -n microservices svc/user-service 5001:5001

# Execute into pod
kubectl exec -it -n microservices user-service-pod -- /bin/bash

# Check environment variables
kubectl exec -n microservices user-service-pod -- env

# Test database connectivity
kubectl exec -n microservices user-service-pod -- python -c "
import mysql.connector
conn = mysql.connector.connect(host='mysql.microservices.svc.cluster.local', user='devops_user', password='devops_password_123', database='microservices_db')
print('Database connection successful')
conn.close()
"
```

---

## 📈 Performance Optimization

### Application Performance

#### Database Optimization

- **Connection pooling**: Reuse database connections
- **Query optimization**: Use indexes effectively
- **Caching strategy**: Redis for session data (future)
- **Read replicas**: Database scaling (future)

#### API Optimization

- **Pagination**: Limit result sets
- **Compression**: Gzip response compression
- **Caching**: HTTP cache headers
- **Async processing**: Background task processing

### Infrastructure Performance

#### Kubernetes Optimization

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 200m
    memory: 256Mi
```

#### Horizontal Scaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### Monitoring Performance

#### Key Metrics

- **Latency**: P95 response time <500ms
- **Throughput**: Requests per second
- **Error rate**: <1% of total requests
- **Resource utilization**: CPU <80%, Memory <85%

---

## 🔮 Future Enhancements

### Phase 2: Advanced Features

#### Service Mesh Implementation

- **Istio**: Traffic management and observability
- **mTLS**: Service-to-service encryption
- **Circuit breakers**: Fault tolerance
- **Canary deployments**: Gradual rollouts

#### Advanced Monitoring

- **Distributed tracing**: Jaeger integration
- **Log aggregation**: ELK stack
- **Metrics correlation**: Advanced alerting
- **Performance profiling**: APM tools

#### Security Enhancements

- **OAuth2/OIDC**: External authentication
- **API Gateway**: Kong or Traefik
- **Secrets management**: HashiCorp Vault
- **Compliance**: SOC2, GDPR compliance

### Phase 3: Production Readiness

#### High Availability

- **Multi-zone deployment**: Regional redundancy
- **Database clustering**: MySQL Galera cluster
- **Load balancing**: External load balancer
- **Backup strategy**: Automated backups

#### Scalability

- **Auto-scaling**: HPA and VPA
- **CDN integration**: Static asset delivery
- **Caching layers**: Redis clusters
- **Message queues**: Event-driven architecture

#### DevOps Maturity

- **GitOps**: ArgoCD for deployments
- **Infrastructure as Code**: Terraform modules
- **Configuration management**: Ansible playbooks
- **Compliance automation**: Policy as code

---

## 📞 Support & Contributing

### Getting Help

#### Documentation Resources

- **API Documentation**: `/docs` endpoint per service
- **Kubernetes Docs**: https://kubernetes.io/docs/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy Docs**: https://sqlalchemy.org/

#### Community Support

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and discussions
- **Wiki**: Detailed guides and tutorials

### Contributing Guidelines

#### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit pull request
5. Code review and merge

#### Code Standards

- **PEP 8**: Python style guide
- **Black**: Code formatting
- **Type hints**: Static typing where possible
- **Documentation**: Docstrings for all functions

#### Testing Requirements

- **Unit tests**: All new code
- **Integration tests**: API changes
- **Documentation**: Updated for new features

---

## 📋 Change Log

### Version 1.0.0 (March 15, 2026)

- ✅ Initial production release
- ✅ Three-tier microservices architecture
- ✅ Kubernetes orchestration
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Monitoring stack (Prometheus + Grafana)
- ✅ Comprehensive testing suite
- ✅ Security hardening
- ✅ Performance optimization

### Version 0.9.0 (January 2026)

- ✅ Core microservices implementation
- ✅ Basic Kubernetes deployment
- ✅ Database integration
- ✅ API development

### Version 0.1.0 (December 2025)

- ✅ Project initialization
- ✅ Architecture planning
- ✅ Development environment setup

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Kubernetes Community**: For excellent documentation and tools
- **Flask Framework**: For the robust web framework
- **SQLAlchemy**: For powerful ORM capabilities
- **Prometheus & Grafana**: For monitoring and visualization
- **GitHub Actions**: For CI/CD automation

---

_This documentation is maintained by the DevOps Capstone Project team. Last updated: March 15, 2026_</content>
<parameter name="filePath">/home/harshmanek/self/projects/devops-capstone-project/DETAILED_PROJECT_DOCUMENTATION.md

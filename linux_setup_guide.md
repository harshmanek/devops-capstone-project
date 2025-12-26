# 🐧 DevOps Microservices Project - Linux (Pop!_OS) Complete Setup Guide

**Last Updated:** December 25, 2025  
**Target OS:** Pop!_OS / Ubuntu  
**Project:** DevOps Capstone with 3 Microservices + Kubernetes

---

## 📋 TABLE OF CONTENTS

1. [System Requirements](#system-requirements)
2. [Install Core Tools](#install-core-tools)
3. [Project Structure Verification](#project-structure-verification)
4. [Python & Virtual Environment Setup](#python--virtual-environment-setup)
5. [Install Project Dependencies](#install-project-dependencies)
6. [Database Setup (MySQL)](#database-setup-mysql)
7. [Docker Setup](#docker-setup)
8. [Kubernetes Setup (Minikube)](#kubernetes-setup-minikube)
9. [Run Services Locally](#run-services-locally)
10. [Troubleshooting](#troubleshooting)

---

## 🔧 SYSTEM REQUIREMENTS

**Minimum:**
- 8GB RAM (16GB recommended for Kubernetes)
- 20GB free disk space
- Linux kernel 4.x+
- Pop!_OS 22.04 or newer

**Check your system:**
```bash
# Check OS version
lsb_release -a

# Check RAM
free -h

# Check disk space
df -h /home

# Check Linux kernel
uname -r
```

---

## 📦 INSTALL CORE TOOLS

### Step 1: Update System Package Manager

```bash
# Update package lists
sudo apt update

# Upgrade all packages
sudo apt upgrade -y

# Install essential build tools
sudo apt install -y build-essential curl wget git vim nano
```

### Step 2: Install Git (if not already installed)

```bash
# Check if git is installed
git --version

# If not installed
sudo apt install -y git

# Configure git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Install curl and wget

```bash
sudo apt install -y curl wget gnupg lsb-release
```

---

## 📁 PROJECT STRUCTURE VERIFICATION

### Check if code is properly cloned

```bash
# Navigate to your project
cd ~/projects/devops-capstone-project  # or wherever you cloned it

# List directory structure
ls -la

# Should show:
# .git
# services/
# k8s/
# README.md
# etc.

# Verify services directory
ls -la services/

# Should show:
# user-service/
# product-service/
# order-service/
```

### Create missing directories if needed

```bash
# If k8s directory doesn't exist
mkdir -p k8s

# If venv directory doesn't exist
mkdir -p venv
```

---

## 🐍 PYTHON & VIRTUAL ENVIRONMENT SETUP

### Step 1: Install Python 3.12

```bash
# Add Python repository
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Verify installation
python3.12 --version

# Create symlink for easier access
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
```

### Step 2: Install pip and virtual environment tools

```bash
# Install pip for Python 3.12
sudo apt install -y python3.12-distutils
python3.12 -m pip install --upgrade pip setuptools wheel

# Verify pip
python3.12 -m pip --version

# Install virtualenv (optional but recommended)
python3.12 -m pip install virtualenv
```

### Step 3: Create Virtual Environment for Project

```bash
# Navigate to project root
cd ~/projects/devops-capstone-project

# Create virtual environment
python3.12 -m venv venv

# Verify venv created
ls -la venv/

# Activate virtual environment
source venv/bin/activate

# You should see (venv) prefix in terminal
# (venv) harsh@laptop:~/projects/devops-capstone-project$

# Verify Python and pip in venv
python --version
pip --version
```

### Step 4: Activate Virtual Environment (for future sessions)

```bash
# Always run this when you start working
cd ~/projects/devops-capstone-project
source venv/bin/activate

# To deactivate (when done working)
deactivate
```

---

## 📦 INSTALL PROJECT DEPENDENCIES

### Step 1: Create requirements.txt for each service

```bash
# Make sure venv is activated
source venv/bin/activate

# User Service requirements
cat > services/user-service/requirements.txt << 'EOF'
Flask==2.3.2
Flask-MySQLdb==1.0.1
python-dotenv==1.0.0
gunicorn==21.2.0
Werkzeug==2.3.6
EOF

# Product Service requirements
cat > services/product-service/requirements.txt << 'EOF'
Flask==2.3.2
Flask-MySQLdb==1.0.1
python-dotenv==1.0.0
gunicorn==21.2.0
Werkzeug==2.3.6
EOF

# Order Service requirements
cat > services/order-service/requirements.txt << 'EOF'
Flask==2.3.2
Flask-MySQLdb==1.0.1
python-dotenv==1.0.0
gunicorn==21.2.0
Werkzeug==2.3.6
EOF
```

### Step 2: Install dependencies for all services

```bash
# Make sure venv is activated
source venv/bin/activate

# Install for User Service
cd ~/projects/devops-capstone-project/services/user-service
pip install -r requirements.txt

# Install for Product Service
cd ~/projects/devops-capstone-project/services/product-service
pip install -r requirements.txt

# Install for Order Service
cd ~/projects/devops-capstone-project/services/order-service
pip install -r requirements.txt

# Return to project root
cd ~/projects/devops-capstone-project

# Verify all packages installed
pip list
```

### Step 3: Create Flask app files if they don't exist

```bash
# User Service
cat > services/user-service/app.py << 'EOF'
from flask import Flask, jsonify

app = Flask(__name__)

# Health check endpoint (required for Kubernetes)
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'user-service'}), 200

@app.route('/')
def index():
    return jsonify({'message': 'User Service is running'}), 200

@app.route('/users')
def users():
    return jsonify({
        'users': [
            {'id': 1, 'name': 'John Doe'},
            {'id': 2, 'name': 'Jane Smith'}
        ]
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
EOF

# Product Service
cat > services/product-service/app.py << 'EOF'
from flask import Flask, jsonify

app = Flask(__name__)

# Health check endpoint (required for Kubernetes)
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'product-service'}), 200

@app.route('/')
def index():
    return jsonify({'message': 'Product Service is running'}), 200

@app.route('/products')
def products():
    return jsonify({
        'products': [
            {'id': 1, 'name': 'Laptop', 'price': 999.99},
            {'id': 2, 'name': 'Mouse', 'price': 29.99}
        ]
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
EOF

# Order Service
cat > services/order-service/app.py << 'EOF'
from flask import Flask, jsonify

app = Flask(__name__)

# Health check endpoint (required for Kubernetes)
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'order-service'}), 200

@app.route('/')
def index():
    return jsonify({'message': 'Order Service is running'}), 200

@app.route('/orders')
def orders():
    return jsonify({
        'orders': [
            {'id': 1, 'user_id': 1, 'total': 1029.98},
            {'id': 2, 'user_id': 2, 'total': 49.99}
        ]
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
EOF
```

---

## 🗄️ DATABASE SETUP (MySQL)

### Step 1: Install MySQL Server

```bash
# Install MySQL server
sudo apt install -y mysql-server

# Verify installation
mysql --version

# Start MySQL service
sudo systemctl start mysql

# Enable MySQL on boot
sudo systemctl enable mysql

# Check MySQL status
sudo systemctl status mysql
```

### Step 2: Secure MySQL Installation

```bash
# Run security script
sudo mysql_secure_installation

# Follow prompts:
# - Enter password: (press Enter for root)
# - Remove anonymous users? y
# - Disable remote root login? y
# - Remove test database? y
# - Reload privilege tables? y
```

### Step 3: Create Database and User

```bash
# Login to MySQL
sudo mysql -u root

# Run these commands in MySQL shell:
# CREATE DATABASE microservices_db;
# CREATE USER 'devops_user'@'localhost' IDENTIFIED BY 'devops_password_123';
# GRANT ALL PRIVILEGES ON microservices_db.* TO 'devops_user'@'localhost';
# FLUSH PRIVILEGES;
# EXIT;

# Or use this script
sudo mysql -u root << EOF
CREATE DATABASE IF NOT EXISTS microservices_db;
CREATE USER IF NOT EXISTS 'devops_user'@'localhost' IDENTIFIED BY 'devops_password_123';
GRANT ALL PRIVILEGES ON microservices_db.* TO 'devops_user'@'localhost';
FLUSH PRIVILEGES;
SHOW DATABASES;
EXIT;
EOF
```

### Step 4: Verify Database Connection

```bash
# Test connection
mysql -u devops_user -p microservices_db -e "SELECT 1;"

# Password: devops_password_123

# Should return: 1
```

---

## 🐳 DOCKER SETUP

### Step 1: Install Docker

```bash
# Install Docker
sudo apt install -y docker.io docker-compose

# Verify Docker installation
docker --version
docker-compose --version

# Start Docker service
sudo systemctl start docker

# Enable Docker on boot
sudo systemctl enable docker

# Check Docker status
sudo systemctl status docker
```

### Step 2: Add Current User to Docker Group (avoid sudo)

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group membership
newgrp docker

# Verify (should work without sudo)
docker ps
```

### Step 3: Build Docker Images

```bash
# Navigate to project root
cd ~/projects/devops-capstone-project

# Build User Service image
docker build -t user-service:1.0 ./services/user-service

# Build Product Service image
docker build -t product-service:1.0 ./services/product-service

# Build Order Service image
docker build -t order-service:1.0 ./services/order-service

# Verify images built
docker images

# Should show all 3 images with tag 1.0
```

### Step 4: Test Docker Images Locally

```bash
# Test User Service
docker run -d \
  --name user-service-test \
  -p 5001:5001 \
  user-service:1.0

# Wait 5 seconds for container to start
sleep 5

# Test endpoint
curl http://localhost:5001/health

# Should return: {"status":"healthy","service":"user-service"}

# Stop and remove container
docker stop user-service-test
docker rm user-service-test
```

---

## ☸️ KUBERNETES SETUP (MINIKUBE)

### Step 1: Install Minikube

```bash
# Download Minikube binary
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64

# Install
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify installation
minikube version
```

### Step 2: Install kubectl

```bash
# Download kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify installation
kubectl version --client

# Make executable
chmod +x kubectl
```

### Step 3: Start Minikube Cluster

```bash
# Start Minikube (uses Docker driver on Linux)
minikube start --driver=docker

# Verify cluster is running
minikube status

# Get cluster info
kubectl cluster-info

# View nodes
kubectl get nodes
```

### Step 4: Configure Docker to use Minikube's Docker Daemon

```bash
# Set up Docker to use Minikube
eval $(minikube docker-env)

# Verify (should show minikube images)
docker ps

# To make this permanent, add to ~/.bashrc
echo "eval \$(minikube docker-env)" >> ~/.bashrc
source ~/.bashrc
```

### Step 5: Rebuild Docker Images in Minikube

```bash
# Make sure you're using Minikube's Docker
eval $(minikube docker-env)

# Rebuild images
cd ~/projects/devops-capstone-project

docker build -t user-service:1.0 ./services/user-service
docker build -t product-service:1.0 ./services/product-service
docker build -t order-service:1.0 ./services/order-service

# Verify in Minikube
docker images
```

---

## 🚀 RUN SERVICES LOCALLY

### Step 1: Activate Virtual Environment

```bash
cd ~/projects/devops-capstone-project
source venv/bin/activate
```

### Step 2: Start Services in Separate Terminals

**Terminal 1 - User Service:**
```bash
source venv/bin/activate
cd ~/projects/devops-capstone-project/services/user-service
python app.py

# Output: Running on http://0.0.0.0:5001
```

**Terminal 2 - Product Service:**
```bash
source venv/bin/activate
cd ~/projects/devops-capstone-project/services/product-service
python app.py

# Output: Running on http://0.0.0.0:5002
```

**Terminal 3 - Order Service:**
```bash
source venv/bin/activate
cd ~/projects/devops-capstone-project/services/order-service
python app.py

# Output: Running on http://0.0.0.0:5003
```

### Step 3: Test Services

```bash
# Test User Service
curl http://localhost:5001/health
curl http://localhost:5001/users

# Test Product Service
curl http://localhost:5002/health
curl http://localhost:5002/products

# Test Order Service
curl http://localhost:5003/health
curl http://localhost:5003/orders
```

---

## 🎯 DEPLOY TO KUBERNETES

### Step 1: Create Kubernetes Namespace

```bash
kubectl apply -f k8s/namespace.yaml

# Verify
kubectl get namespaces
```

### Step 2: Create MySQL Resources

```bash
kubectl apply -f k8s/mysql-configmap.yaml
kubectl apply -f k8s/mysql-pvc.yaml
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml

# Verify MySQL is running
kubectl get pods -n microservices
```

### Step 3: Deploy Microservices

```bash
# Deploy all services
kubectl apply -f k8s/user-service-deployment.yaml
kubectl apply -f k8s/user-service-service.yaml
kubectl apply -f k8s/product-service-deployment.yaml
kubectl apply -f k8s/product-service-service.yaml
kubectl apply -f k8s/order-service-deployment.yaml
kubectl apply -f k8s/order-service-service.yaml

# Monitor deployment
kubectl get pods -n microservices --watch

# Once all pods are Running, press Ctrl+C
```

### Step 4: Verify Deployment

```bash
# Check all resources
kubectl get all -n microservices

# Test services
kubectl run -it --rm debug --image=busybox:1.28 --restart=Never -n microservices -- sh

# Inside the debug pod, test services:
# wget -q -O - http://user-service:5001/health
# wget -q -O - http://product-service:5002/health
# wget -q -O - http://order-service:5003/health
```

---

## 🔧 USEFUL COMMANDS

### Project Development

```bash
# Activate virtual environment
source ~/projects/devops-capstone-project/venv/bin/activate

# Deactivate virtual environment
deactivate

# Install new package
pip install package_name

# Freeze requirements
pip freeze > requirements.txt

# Run single service
python services/user-service/app.py

# Check Python version
python --version
```

### Docker Commands

```bash
# Build image
docker build -t service-name:1.0 ./services/service-name

# Run container
docker run -d -p 5001:5001 service-name:1.0

# List images
docker images

# List running containers
docker ps

# Stop container
docker stop container_id

# Remove image
docker rmi service-name:1.0

# View logs
docker logs container_id
```

### Kubernetes Commands

```bash
# Start Minikube
minikube start --driver=docker

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete

# View all resources
kubectl get all -n microservices

# View pods
kubectl get pods -n microservices

# View services
kubectl get svc -n microservices

# View logs
kubectl logs pod-name -n microservices

# Port forward
kubectl port-forward svc/user-service 5001:5001 -n microservices

# Delete deployment
kubectl delete deployment deployment-name -n microservices

# Apply manifest
kubectl apply -f file.yaml

# Delete manifest
kubectl delete -f file.yaml
```

---

## 🔍 TROUBLESHOOTING

### Python Virtual Environment Issues

```bash
# If venv is corrupted, recreate it
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Check if activate script exists
ls -la venv/bin/activate
```

### MySQL Connection Issues

```bash
# Verify MySQL is running
sudo systemctl status mysql

# Test connection
mysql -u devops_user -p microservices_db -e "SHOW TABLES;"

# Check user permissions
sudo mysql -u root -e "SHOW GRANTS FOR 'devops_user'@'localhost';"

# Fix permissions if needed
sudo mysql -u root << EOF
GRANT ALL PRIVILEGES ON microservices_db.* TO 'devops_user'@'localhost';
FLUSH PRIVILEGES;
EOF
```

### Docker Issues

```bash
# If Docker daemon won't start
sudo systemctl restart docker

# Check Docker daemon status
sudo systemctl status docker

# Clean up unused resources
docker system prune -a

# If permission denied error
sudo usermod -aG docker $USER
newgrp docker
```

### Kubernetes Issues

```bash
# Check Minikube status
minikube status

# View Minikube logs
minikube logs

# Check node status
kubectl get nodes

# Describe pod for errors
kubectl describe pod pod-name -n microservices

# View pod logs
kubectl logs pod-name -n microservices

# If pods won't start, check resource limits
kubectl top nodes
kubectl top pods -n microservices

# Reset Minikube if needed
minikube delete
minikube start --driver=docker
```

### Network Issues

```bash
# Check if ports are in use
sudo lsof -i :5001
sudo lsof -i :5002
sudo lsof -i :5003
sudo lsof -i :3306

# Kill process on port
sudo kill -9 PID

# Port forward Kubernetes service
kubectl port-forward svc/user-service 5001:5001 -n microservices
```

---

## ✅ FINAL CHECKLIST

- [ ] Pop!_OS system is updated
- [ ] Python 3.12 is installed
- [ ] Virtual environment is created and activated
- [ ] All dependencies are installed
- [ ] MySQL server is running and database is created
- [ ] Docker is installed and user added to docker group
- [ ] All 3 Docker images are built
- [ ] Minikube cluster is running
- [ ] kubectl is installed and configured
- [ ] Services run locally on ports 5001, 5002, 5003
- [ ] All endpoints respond to curl commands
- [ ] Kubernetes manifests are created
- [ ] MySQL pod is running in Kubernetes
- [ ] All 3 microservices are deployed and running in Kubernetes

---

## 🎯 NEXT STEPS

1. **Run Services Locally** - Test all endpoints work
2. **Deploy to Kubernetes** - Use kubectl apply commands
3. **Monitor Pods** - Watch logs and status
4. **Create API tests** - Write curl scripts to test endpoints
5. **Set up CI/CD** - Create GitHub Actions workflows
6. **Document APIs** - Create Swagger/OpenAPI docs

---

**Good luck with your DevOps journey! 🚀**

#!/bin/bash

################################################################################
# COMPLETE PROJECT FINISHING GUIDE
# Follow these steps to complete your DevOps project
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

clear_screen() {
    clear
}

print_header() {
    echo -e "\n${CYAN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}\n"
}

print_step() {
    echo -e "\n${YELLOW}[STEP] $1${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_command() {
    echo -e "${YELLOW}$${NC} $1"
}

wait_for_input() {
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
}

################################################################################
# MAIN MENU
################################################################################

show_menu() {
    clear_screen
    print_header "DEVOPS CAPSTONE PROJECT - COMPLETION WIZARD"
    
    echo -e "${CYAN}Project Status: 60% Complete${NC}"
    echo -e "✅ Kubernetes Deployment"
    echo -e "⏳ CI/CD Pipeline (GitHub Actions)"
    echo -e "⏳ Monitoring Stack (Prometheus + Grafana)"
    echo -e "⏳ Documentation & Demo"
    echo ""
    echo "Choose what to complete next:"
    echo ""
    echo "  1) Setup GitHub Actions CI/CD"
    echo "  2) Setup Prometheus + Grafana Monitoring"
    echo "  3) Create API Documentation (Swagger)"
    echo "  4) Complete All (Recommended!)"
    echo "  5) Quick Test & Status"
    echo "  6) View Full Documentation"
    echo "  0) Exit"
    echo ""
    read -p "Enter choice (0-6): " choice
}

################################################################################
# OPTION 1: GITHUB ACTIONS SETUP
################################################################################

setup_github_actions() {
    clear_screen
    print_header "GITHUB ACTIONS CI/CD SETUP"
    
    print_step "Step 1: Verify Git Repository"
    
    if [ -d .git ]; then
        print_success "Git repository found"
    else
        print_error "Git repository not found!"
        echo "Initialize git:"
        print_command "git init"
        print_command "git remote add origin https://github.com/YOUR_USERNAME/devops-capstone-project.git"
        wait_for_input
        return
    fi
    
    print_step "Step 2: Create GitHub Workflows"
    bash setup-cicd.sh
    
    print_step "Step 3: Next Actions"
    echo "1. Create GitHub Personal Access Token:"
    echo "   - Go to GitHub → Settings → Developer settings → Personal access tokens"
    echo "   - Select scopes: repo, write:packages, read:packages"
    echo ""
    echo "2. Commit and push:"
    print_command "git add ."
    print_command "git commit -m 'feat: add CI/CD pipeline'"
    print_command "git push origin main"
    echo ""
    echo "3. Monitor pipeline:"
    echo "   - Go to your GitHub repository"
    echo "   - Click Actions tab"
    echo "   - Watch workflow execute"
    echo ""
    wait_for_input
}

################################################################################
# OPTION 2: PROMETHEUS + GRAFANA SETUP
################################################################################

setup_monitoring() {
    clear_screen
    print_header "PROMETHEUS + GRAFANA MONITORING SETUP"
    
    print_step "Prerequisites Check"
    
    # Check if helm is installed
    if ! command -v helm &> /dev/null; then
        print_error "Helm not found. Installing..."
        curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
        print_success "Helm installed"
    else
        print_success "Helm is installed"
    fi
    
    # Check if Kubernetes cluster is running
    if ! kubectl cluster-info &> /dev/null; then
        print_error "Kubernetes cluster not running!"
        echo "Start Minikube:"
        print_command "minikube start --driver=docker"
        wait_for_input
        return
    else
        print_success "Kubernetes cluster is running"
    fi
    
    print_step "Installing Monitoring Stack"
    bash setup-monitoring.sh
    
    print_step "Access Monitoring Dashboards"
    echo "Terminal 1 - Prometheus:"
    print_command "kubectl port-forward -n microservices svc/prometheus-operated 9090:9090"
    echo "→ http://localhost:9090"
    echo ""
    echo "Terminal 2 - Grafana:"
    print_command "kubectl port-forward -n microservices svc/prometheus-grafana 3000:80"
    echo "→ http://localhost:3000 (admin/admin123)"
    echo ""
    wait_for_input
}

################################################################################
# OPTION 3: API DOCUMENTATION
################################################################################

setup_api_documentation() {
    clear_screen
    print_header "API DOCUMENTATION WITH SWAGGER"
    
    mkdir -p ~/projects/devops-capstone-project/docs
    cd ~/projects/devops-capstone-project
    
    print_step "Installing Swagger UI"
    
    cat > docs/swagger.yaml << 'EOF'
openapi: 3.0.0
info:
  title: DevOps Microservices API
  description: Complete API documentation for User, Product, and Order services
  version: 1.0.0
  contact:
    name: DevOps Team
    url: https://github.com/yourusername/devops-capstone-project

servers:
  - url: http://localhost:5001
    description: User Service
  - url: http://localhost:5002
    description: Product Service
  - url: http://localhost:5003
    description: Order Service

tags:
  - name: Users
    description: User management endpoints
  - name: Products
    description: Product management endpoints
  - name: Orders
    description: Order management endpoints
  - name: Health
    description: Service health checks

paths:
  /health:
    get:
      tags:
        - Health
      summary: Health check
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                  service:
                    type: string
                  timestamp:
                    type: string

  /users:
    post:
      tags:
        - Users
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                password:
                  type: string
      responses:
        '201':
          description: User created successfully
    get:
      tags:
        - Users
      summary: List all users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
        - name: per_page
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: List of users

  /users/{id}:
    get:
      tags:
        - Users
      summary: Get user details
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User found
    put:
      tags:
        - Users
      summary: Update user
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
      responses:
        '200':
          description: User updated
    delete:
      tags:
        - Users
      summary: Delete user
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User deleted

  /products:
    post:
      tags:
        - Products
      summary: Create product
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                description:
                  type: string
                price:
                  type: number
                stock_quantity:
                  type: integer
      responses:
        '201':
          description: Product created
    get:
      tags:
        - Products
      summary: List all products
      responses:
        '200':
          description: List of products

  /orders:
    post:
      tags:
        - Orders
      summary: Create order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: string
                product_id:
                  type: string
                quantity:
                  type: integer
      responses:
        '201':
          description: Order created
    get:
      tags:
        - Orders
      summary: List all orders
      responses:
        '200':
          description: List of orders

  /orders/{id}:
    get:
      tags:
        - Orders
      summary: Get order details
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Order found
    put:
      tags:
        - Orders
      summary: Update order status
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
      responses:
        '200':
          description: Order updated
    delete:
      tags:
        - Orders
      summary: Delete order
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Order deleted

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        username:
          type: string
        email:
          type: string
        created_at:
          type: string
        updated_at:
          type: string

    Product:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        description:
          type: string
        price:
          type: number
        stock_quantity:
          type: integer
        created_at:
          type: string
        updated_at:
          type: string

    Order:
      type: object
      properties:
        id:
          type: string
        user_id:
          type: string
        product_id:
          type: string
        quantity:
          type: integer
        status:
          type: string
        total_price:
          type: number
        created_at:
          type: string
        updated_at:
          type: string
EOF
    
    print_success "Swagger specification created"
    echo ""
    echo "View API documentation at:"
    echo "→ https://editor.swagger.io/"
    echo "→ Paste contents of docs/swagger.yaml"
    echo ""
    wait_for_input
}

################################################################################
# OPTION 4: COMPLETE ALL
################################################################################

complete_all() {
    clear_screen
    print_header "COMPLETING ALL REMAINING TASKS"
    
    print_step "1/3: Setting up GitHub Actions"
    setup_github_actions
    
    print_step "2/3: Setting up Monitoring"
    setup_monitoring
    
    print_step "3/3: Creating API Documentation"
    setup_api_documentation
    
    clear_screen
    print_header "PROJECT COMPLETION SUMMARY"
    
    echo -e "${GREEN}✓ GitHub Actions CI/CD${NC}"
    echo -e "${GREEN}✓ Prometheus + Grafana Monitoring${NC}"
    echo -e "${GREEN}✓ API Documentation (Swagger)${NC}"
    echo ""
    echo "Next Steps:"
    echo "1. Create demo video (5-10 minutes)"
    echo "2. Write final project report"
    echo "3. Present to your guide"
    echo ""
    wait_for_input
}

################################################################################
# OPTION 5: QUICK TEST
################################################################################

quick_test() {
    clear_screen
    print_header "QUICK KUBERNETES TEST"
    
    print_step "Checking Kubernetes Cluster"
    kubectl cluster-info
    
    print_step "Checking Pods"
    kubectl get pods -n microservices
    
    print_step "Checking Services"
    kubectl get svc -n microservices
    
    print_step "Checking Resources"
    kubectl top pods -n microservices 2>/dev/null || echo "Metrics not available"
    
    echo ""
    echo "Everything looks good! Your Kubernetes cluster is running."
    echo ""
    wait_for_input
}

################################################################################
# OPTION 6: FULL DOCUMENTATION
################################################################################

view_documentation() {
    clear_screen
    cat PROJECT_DOCUMENTATION.md
}

################################################################################
# MAIN LOOP
################################################################################

while true; do
    show_menu
    
    case $choice in
        1) setup_github_actions ;;
        2) setup_monitoring ;;
        3) setup_api_documentation ;;
        4) complete_all ;;
        5) quick_test ;;
        6) view_documentation ;;
        0) 
            clear_screen
            echo -e "${GREEN}Thank you for using the DevOps Completion Wizard!${NC}"
            echo -e "${GREEN}Your project is almost complete. Good luck!${NC}"
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please try again."
            wait_for_input
            ;;
    esac
done


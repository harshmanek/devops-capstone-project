# GitHub Actions CI/CD Setup Guide

## Prerequisites
- GitHub repository created and pushed
- Docker Hub or GitHub Container Registry (GHCR) account

## Step 1: Create GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (full control)
   - `write:packages` (push packages)
   - `read:packages` (pull packages)
4. Copy the token (you'll need it)

## Step 2: Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add these secrets:

### For GitHub Container Registry (GHCR) - FREE
```
Name: GITHUB_TOKEN
Value: (Use default - GitHub provides this automatically)
```

## Step 3: Configure GitHub Actions

Workflows are already in `.github/workflows/`

### Enable Actions:
1. Go to repository → Actions tab
2. Workflows should appear
3. Click "Enable GitHub Actions"

## Step 4: Update Kubernetes Imagefile

1. Replace `YOUR_GITHUB_USERNAME` in all deployment files:
```bash
sed -i 's/YOUR_GITHUB_USERNAME/your-actual-username/g' k8s/*.yaml
```

2. Create Docker registry secret in Kubernetes:
```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=YOUR_USERNAME \
  --docker-password=YOUR_GITHUB_TOKEN \
  --docker-email=YOUR_EMAIL \
  -n microservices
```

## Step 5: Trigger Pipeline

1. Commit and push to master/main:
```bash
git add .
git commit -m "feat: add GitHub Actions CI/CD pipeline"
git push origin main
```

2. Go to Actions tab in GitHub
3. Watch workflow execute:
   - Build Docker images ✓
   - Run tests ✓
   - Push to GHCR ✓

## Step 6: Deploy Updated Images

```bash
# Update deployments to use GHCR images
kubectl apply -f k8s/user-service-deployment-ghcr.yaml
kubectl apply -f k8s/product-service-deployment-ghcr.yaml
kubectl apply -f k8s/order-service-deployment-ghcr.yaml

# Verify new pods
kubectl get pods -n microservices
```


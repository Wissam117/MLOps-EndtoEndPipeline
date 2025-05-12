#!/bin/bash

# Exit on error
set -e

echo "Starting Minikube deployment process..."

# Check if Minikube is running
if ! minikube status | grep -q "Running"; then
  echo "Starting Minikube..."
  minikube start
else
  echo "Minikube is already running."
fi

# Point shell to minikube's docker-daemon
echo "Configuring Docker environment to use Minikube's Docker daemon..."
eval $(minikube docker-env)

# Build Docker images
echo "Building Docker images..."
echo "Building Frontend image..."
docker build -t microservices-app/frontend:latest ./frontend

echo "Building Backend image..."
docker build -t microservices-app/backend:latest ./backend

echo "Building Auth Service image..."
docker build -t microservices-app/auth-service:latest ./auth-service

echo "All images built successfully."

# Apply Kubernetes configurations
echo "Applying Kubernetes configurations..."

# Create namespace if it doesn't exist
kubectl create namespace microservices-app --dry-run=client -o yaml | kubectl apply -f -

# Apply secrets and configmaps first
echo "Applying Secrets and ConfigMaps..."
kubectl apply -f kubernetes/app-secrets.yaml -n microservices-app
kubectl apply -f kubernetes/db-deployment.yaml -n microservices-app

# Wait for database to be ready
echo "Waiting for database to be ready..."
kubectl wait --for=condition=Available deployment/db-deployment -n microservices-app --timeout=120s

# Apply other services
echo "Deploying services..."
kubectl apply -f kubernetes/auth-deployment.yaml -n microservices-app
kubectl apply -f kubernetes/backend-deployment.yaml -n microservices-app
kubectl apply -f kubernetes/frontend-deployment.yaml -n microservices-app

# Wait for all deployments to be available
echo "Waiting for all services to be ready..."
kubectl wait --for=condition=Available deployment/auth-deployment -n microservices-app --timeout=120s
kubectl wait --for=condition=Available deployment/backend-deployment -n microservices-app --timeout=120s
kubectl wait --for=condition=Available deployment/frontend-deployment -n microservices-app --timeout=120s

# Get the URL for the frontend service
FRONTEND_URL=$(minikube service frontend-service -n microservices-app --url)

echo "Deployment completed successfully!"
echo "You can access the application at: $FRONTEND_URL"
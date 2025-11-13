#!/bin/bash
echo "=== Deploying Unified Kubernetes Project ==="

# Build Flask image
echo "Building Flask image..."
cd ../src/flask-app
docker build -t flask-app:latest .
cd ../../scripts

# Apply all Kubernetes manifests
echo "Deploying to Kubernetes..."
kubectl apply -f ../k8s/file-server/
kubectl apply -f ../k8s/flask-backend/
kubectl apply -f ../k8s/nginx-reverse-proxy/

# Wait for pods to be ready
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=flask-backend --timeout=120s
kubectl wait --for=condition=ready pod -l app=file-server-persistent --timeout=120s
kubectl wait --for=condition=ready pod -l app=nginx-reverse-proxy --timeout=120s

# Create symlink for uploads
echo "Setting up uploads directory..."
FILE_POD=$(kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ ! -z "$FILE_POD" ]; then
    kubectl exec -it $FILE_POD -- sh -c 'ln -sf /shared-uploads /usr/share/nginx/html/uploads 2>/dev/null || true'
fi

echo "=== Deployment Complete ==="
echo "Services:"
kubectl get services
echo ""
echo "Pods:"
kubectl get pods

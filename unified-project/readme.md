# Kubernetes Unified Project

A comprehensive Kubernetes learning project that demonstrates a complete microservices architecture with Flask backend, Nginx reverse proxy, and persistent file storage.

## 🏗️ Architecture

```
Internet → Nginx Reverse Proxy (port 80)
    ├── /flask/* → Flask Backend (port 5000) → /shared-uploads/ (Persistent Volume)
    ├── /upload → Flask Backend (file upload handling)
    ├── /files/* → File Server (port 80) → /uploads/ → /shared-uploads/ (symlink)
    └── /health → Health check endpoint
```

## 📁 Project Structure

```
unified-project/
├── k8s/                          # Kubernetes manifests
│   ├── nginx-reverse-proxy/
│   │   ├── nginx-configmap.yaml  # Nginx routing configuration
│   │   ├── nginx-deployment.yaml # Nginx proxy deployment
│   │   └── nginx-service.yaml    # Nginx service (NodePort/LoadBalancer)
│   ├── flask-backend/
│   │   ├── flask-deployment.yaml # Flask app with PVC mount
│   │   └── flask-service.yaml    # Flask internal service
│   └── file-server/
│       ├── file-server-pvc.yaml           # Persistent Volume Claim (5GB)
│       ├── file-server-deployment.yaml    # Nginx file server with PVC
│       ├── file-server-service.yaml       # File server service (NodePort 30002)
│       └── file-server-nginx-configmap.yaml # File server nginx config
├── src/                          # Application source code
│   └── flask-app/
│       ├── server.py             # Flask application with upload API
│       ├── requirements.txt      # Python dependencies
│       └── Dockerfile            # Flask container definition
├── scripts/                      # Deployment and management scripts
│   ├── deploy-all.sh             # Complete deployment script
│   └── get-pod-name.sh           # Utility to get pod names
└── README.md                     # This file
```

## 🚀 Features

* Reverse Proxy: Nginx routing between services
* REST API: Flask backend with file upload endpoints
* Persistent Storage: File server with 5GB persistent volume
* File Upload: Web interface and API for file uploads
* Resource Limits: CPU and memory limits for all services
* Health Checks: Built-in health monitoring

## 📋 Prerequisites

* Minikube
* kubectl
* Docker

## 🛠️ Quick Start

```bash
# 1. Start Minikube
minikube start
eval $(minikube docker-env)

# 2. Deploy Everything
cd unified-project/scripts
./deploy-all.sh

# 3. Access the Application
minikube service nginx-svc --url
echo "File Server: http://$(minikube ip):30002"
```

## 🔧 Manual Deployment

**Build Flask Image:**

```bash
cd src/flask-app
docker build -t flask-app:latest .
```

**Deploy Persistent Volume and File Server:**

```bash
kubectl apply -f k8s/file-server/
```

**Deploy Flask Backend:**

```bash
kubectl apply -f k8s/flask-backend/
```

**Deploy Nginx Reverse Proxy:**

```bash
kubectl apply -f k8s/nginx-reverse-proxy/
```

**Setup Uploads Symlink:**

```bash
FILE_POD=$(kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $FILE_POD -- sh -c 'mkdir -p /shared-uploads && ln -sf /shared-uploads /usr/share/nginx/html/uploads'
```

## 📡 API Endpoints

| Endpoint       | Description             |
| -------------- | ----------------------- |
| `/flask`       | Flask API hello message |
| `/upload`      | File upload web form    |
| `POST /upload` | File upload API         |
| `/flask/files` | List uploaded files     |
| `/health`      | Health check            |

**Direct Access:**

```
http://[minikube-ip]:30002/ - File server main page
http://[minikube-ip]:30002/uploads/ - Uploaded files directory
```

## 📤 File Upload Examples

**Web Interface:**

```bash
curl http://$(minikube ip):30000/upload
```

**API Upload:**

```bash
curl -X POST -F "file=@/path/to/file.txt" http://$(minikube ip):30000/upload
curl http://$(minikube ip):30000/flask/files
curl http://$(minikube ip):30002/uploads/file.txt
```

## 🛠️ Management Commands

```bash
./scripts/get-pod-name.sh flask
./scripts/get-pod-name.sh nginx
./scripts/get-pod-name.sh file-server
kubectl get pods,svc,pvc
kubectl logs -l app=flask-backend
kubectl rollout restart deployment/nginx-reverse-proxy
```

## 🔍 Troubleshooting

**502 Bad Gateway:** Ensure Flask pods are running.
**403 Forbidden:** Verify symlink path in `/usr/share/nginx/html/`.
**ImagePullBackOff:** Ensure Docker is configured for Minikube.
**PVC Pending:** Check `kubectl get pvc` and storage class.

## 🗂️ Resource Limits

| Component     | RAM        | CPU       |
| ------------- | ---------- | --------- |
| Flask Backend | 64Mi-128Mi | 100m-200m |
| File Server   | 64Mi-128Mi | 100m-200m |
| Nginx Proxy   | 64Mi-128Mi | 100m-200m |

## 🔄 Persistence Testing

```bash
curl -X POST -F "file=@test.txt" http://$(minikube ip):30000/upload
kubectl delete pod -l app=file-server-persistent
curl http://$(minikube ip):30002/uploads/test.txt
```

## 🚮 Cleanup

```bash
kubectl delete -f k8s/nginx-reverse-proxy/
kubectl delete -f k8s/flask-backend/
kubectl delete -f k8s/file-server/
kubectl delete pvc file-server-pvc
```

## 🎯 Learning Objectives

* Kubernetes Deployments and Services
* Persistent Volumes and Volume Claims
* Reverse Proxy Configuration
* Inter-service Communication
* Resource Management and Limits
* File Upload Handling in Microservices
* Health Checks and Monitoring

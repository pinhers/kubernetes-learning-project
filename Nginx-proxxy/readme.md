# Kubernetes Nginx Reverse Proxy Learning Project

Hands-on lab to practice Kubernetes fundamentals by deploying a Flask backend behind an Nginx reverse proxy.

## 📋 Project Overview

This project demonstrates:

* Containerizing a Flask application
* Configuring Nginx as a reverse proxy
* Kubernetes Deployments and Services
* ConfigMaps for configuration management
* Multi-container orchestration

## 🏗️ Architecture

```
Internet
   ↓
Nginx Reverse Proxy (LoadBalancer/NodePort:80)
   ↓
Flask Backend Service (ClusterIP:5000)
   ↓
Flask Application Pods (Port:5000)
```

## 📁 Project Structure

```
Nginx-proxxy/
├── server.py                    # Flask app
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Flask container definition
├── readme.md                    # This file
└── custom_niginx/               # Nginx configuration
    ├── Dockerfile               # Custom Nginx image (not currently used)
    ├── nginx.conf               # Basic Nginx config
    ├── nginx-configmap.yaml     # Enhanced ConfigMap
    ├── nginx-deployment.yaml    # Nginx reverse proxy deployment
    └── flask-deployment.yaml    # Flask backend deployment
```

## 🚀 Quick Start

### Prerequisites

* Minikube
* kubectl
* Docker

### Deployment Steps

Start cluster:

```bash
minikube start
```

Configure Docker for Minikube:

```bash
eval $(minikube docker-env)
```

Build Flask image:

```bash
docker build -t flask-app:latest .
```

Deploy manifests:

```bash
kubectl apply -f custom_niginx/
```

Verify:

```bash
kubectl get pods
kubectl get svc
```

Access app:

```bash
minikube service nginx-svc --url
curl http://<service-url>/flask
curl http://<service-url>/health
```

## 🔧 Configuration Details

### Flask Application

* Port: 5000
* Endpoints:

  * `/` → Returns JSON greeting
  * `/health` → Health check

### Nginx Reverse Proxy

* Container port: 8080, Service port: 80
* Routes:

  * `/flask` → Flask backend service
  * `/health` → Static health response
* Features:

  * Header forwarding (X-Real-IP, X-Forwarded-For)
  * Load balancing between replicas

### Kubernetes Resources

| Resource            | Type         | Purpose                         |
| ------------------- | ------------ | ------------------------------- |
| flask-backend       | Deployment   | Manages Flask pods (2 replicas) |
| backend-svc         | Service      | Exposes Flask pods internally   |
| nginx-reverse-proxy | Deployment   | Runs Nginx proxy                |
| nginx-svc           | LoadBalancer | Exposes Nginx externally        |
| nginx-config        | ConfigMap    | Stores Nginx config             |

## 🛠️ Technical Notes

### Current Implementation

* Uses `nginx:alpine` with ConfigMap
* Flask app replicas: 2
* Nginx service: LoadBalancer (or NodePort)
* Local Docker builds

### Development vs Production

✅ Ideal for learning basics
⚠️ Not production-ready:

* No TLS
* Basic health checks
* Local-only images
* No resource limits

## 🎯 Learning Objectives

* Dockerize Python apps
* Kubernetes Deployments and replicas
* Service discovery and networking
* ConfigMaps for configuration
* Reverse proxy routing
* Multi-service orchestration

## 📈 Next Steps

### Immediate

* Add health checks
* Add resource limits
* Add readiness/liveness probes

### Advanced

* PostgreSQL StatefulSet
* Persistent Volumes
* Helm charts
* Ingress controller with TLS
* CI/CD pipeline

### Production Readiness

* Use Gunicorn for Flask
* Push to Docker Hub/ECR
* Monitoring with Prometheus/Grafana
* Logging with ELK
* Network policies

## 🔍 Troubleshooting

### Images not found

```bash
eval $(minikube docker-env)
docker images | grep flask-app
```

### CrashLoopBackOff

```bash
kubectl logs <pod-name>
```

### Services not accessible

```bash
kubectl get svc
kubectl get pods
```

## 📝 Learning Resources

Focus areas:

* Pod networking
* Service discovery
* Reverse proxy config
* Multi-container apps
* Config management in Kubernetes

> Educational purpose only. Not for production.

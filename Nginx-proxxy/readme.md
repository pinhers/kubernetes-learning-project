Kubernetes Reverse Proxy Lab

Hands-on lab to practice Kubernetes by running a Flask backend behind an Nginx reverse proxy. Future additions: PostgreSQL and file-server pod.

Architecture Internet ↓ Nginx (reverse proxy, LoadBalancer/NodePort) ↓ Flask Application (backend service)

Repo Layout kubeproject/ ├── server.py # Flask app ├── requirements.txt # Python deps ├── Dockerfile # Flask container ├── README.md └── custom_nginx/ ├── nginx.conf # Proxy config ├── nginx-configmap.yaml ├── nginx-deployment.yaml └── flask-deployment.yaml

Quick Start

Start Minikube minikube start

Point Docker to Minikube eval $(minikube docker-env)

Build Flask Image docker build -t flask-app:latest .

Apply Manifests kubectl apply -f custom_nginx/

Verify Pods and Services kubectl get pods kubectl get svc

Access the App minikube service nginx-svc --url curl http:///flask

Notes

Designed for local lab use, not production.

Nginx runs as reverse proxy. No TLS here; add ingress later if needed.

Flask runs as simple backend. Use Gunicorn once scaling matters.

Next Steps

Add PostgreSQL StatefulSet

Persistent storage for uploads

Helm refactor for modularity

CI build for images, kustomize overlays

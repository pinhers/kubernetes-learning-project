# Persistent File Server in Kubernetes

Step‑by‑step build of a persistent file server using a PersistentVolumeClaim.

## Phase 1: Problem Understanding

* `emptyDir` loses files when pods restart
* Need persistent storage for file server

## Phase 2: Create Persistent Volume Claim

Create `file-server-pvc.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: file-server-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

Apply:

```bash
kubectl apply -f file-server-pvc.yaml
```

PVC requests storage. Minikube binds it to a PV automatically.

## Phase 3: Persistent Deployment

Create `file-server-deployment-persistent.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: file-server-persistent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: file-server-persistent
  template:
    metadata:
      labels:
        app: file-server-persistent
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
        volumeMounts:
        - name: persistent-storage
          mountPath: /usr/share/nginx/html
      volumes:
      - name: persistent-storage
        persistentVolumeClaim:
          claimName: file-server-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: file-server-svc
spec:
  type: NodePort
  selector:
    app: file-server-persistent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30002
```

Apply:

```bash
kubectl apply -f file-server-deployment-persistent.yaml
```

## Phase 4: Test Persistence

```bash
POD=$(kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}')

kubectl exec -it $POD -- sh -c 'echo "PERSISTENT FILE" > /usr/share/nginx/html/test.txt'

kubectl delete pod $POD

kubectl wait --for=condition=ready pod -l app=file-server-persistent --timeout=60s
POD=$(kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}')

kubectl exec -it $POD -- ls -la /usr/share/nginx/html/
```

Files persist after pod restart.

## Key Concepts

* PVC: storage request
* PV: storage provided (auto in Minikube)
* VolumeMount: attach storage to container
* Persistence: data survives restarts

## Current Architecture

```
Internet → NodePort:30002 → Service → Pod → Persistent Volume
```

## Troubleshooting

### Label Mismatch

```
no matching resources found
```

Fix:

```bash
kubectl get pods --show-labels
kubectl get pods -l app=file-server-persistent
```

### PV Appears Empty

Fresh PV starts empty. Create files after deploy.

```bash
kubectl exec -it $POD -- sh -c 'echo "content" > /usr/share/nginx/html/file.txt'
```

### Variable Lost

Shell variables do not persist.

```bash
POD=$(kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}')
```

## Useful Debug Commands

```bash
kubectl get pods --show-labels
kubectl describe pod
kubectl get pvc
kubectl logs
kubectl exec -it $POD -- ls -la /usr/share/nginx/html/
kubectl get events --sort-by=.metadata.creationTimestamp
```

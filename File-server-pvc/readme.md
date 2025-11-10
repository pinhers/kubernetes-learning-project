# Kubernetes Persistent File Server Lab

Hands-on project to understand persistent storage in Kubernetes using PersistentVolumeClaims (PVC) with an Nginx file server.

## 📋 Project Overview

This lab demonstrates how to achieve data persistence in Kubernetes by replacing `emptyDir` volumes with persistent storage that survives pod restarts and failures.

## 🎯 Learning Objectives

* Understand `emptyDir` limitations
* Learn PVC concepts and usage
* Configure persistent storage in deployments
* Test persistence across pod restarts
* Work with storage in Minikube

## 🏗️ Architecture

```
Internet
   ↓
NodePort Service (30002)
   ↓
File Server Pod
   ↓
Persistent Volume Claim (5Gi)
   ↓
Persistent Volume (auto-provisioned by Minikube)
```

## 📁 Project Structure

```
file-server-project/
├── file-server-pvc.yaml                   # PVC definition
├── file-server-deployment-persistent.yaml # Deployment using PVC
└── README.md                              # This file
```

## 🚀 Quick Start

### Prerequisites

* Minikube running
* kubectl configured

### Steps

Create PVC:

```bash
kubectl apply -f file-server-pvc.yaml
```

Deploy file server:

```bash
kubectl apply -f file-server-deployment-persistent.yaml
```

Verify:

```bash
kubectl get pvc
kubectl get pods -l app=file-server-persistent
kubectl get svc file-server-persistent-svc
```

Access:

```bash
minikube service file-server-svc --url
curl http://<minikube-ip>:30002/
```

## 🔧 Configuration Details

### PersistentVolumeClaim (`file-server-pvc.yaml`)

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

### Deployment (`file-server-deployment-persistent.yaml`)

* Image: `nginx:alpine`
* Mount: `/usr/share/nginx/html`
* Service: NodePort (30002)
* Replicas: 1

## 🧪 Testing Persistence

```bash
export POD=$(kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}')

kubectl exec -it $POD -- sh -c 'echo "PERSISTENT DATA SURVIVES RESTARTS" > /usr/share/nginx/html/test.txt'

kubectl exec -it $POD -- cat /usr/share/nginx/html/test.txt

kubectl delete pod $POD

kubectl wait --for=condition=ready pod -l app=file-server-persistent --timeout=60s
export NEW_POD=$(kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}')

kubectl exec -it $NEW_POD -- cat /usr/share/nginx/html/test.txt
```

## 📚 Key Concepts

### PersistentVolumeClaim (PVC)

Request for storage. Minikube auto-provisions the PV.

### PersistentVolume (PV)

Actual storage backing the PVC.

### Volume Mount

Connects PVC to container path.

### Access Modes

* `ReadWriteOnce`: single node read/write
* `ReadOnlyMany`: multi-node read
* `ReadWriteMany`: multi-node read/write

## 🛠️ Troubleshooting

### PVC Pending

```bash
kubectl get pvc
kubectl describe pvc file-server-pvc
kubectl get storageclass
```

### Pod Not Starting

```bash
kubectl describe pod -l app=file-server-persistent
kubectl logs -l app=file-server-persistent
```

### Label Mismatch

```bash
kubectl get pods --show-labels
kubectl get pods -l app=file-server-persistent
```

### File Missing

```bash
kubectl exec -it $POD -- sh -c 'echo "Welcome to Persistent File Server" > /usr/share/nginx/html/index.html'
```

### Debug Commands

```bash
kubectl get pvc,pv,pods,svc -o wide
kubectl get pods --show-labels
kubectl describe svc file-server-svc
kubectl describe pvc file-server-pvc
kubectl get pv
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl exec -it $POD -- ls -la /usr/share/nginx/html/
```

## 🎯 Learning Outcomes

* PVC vs emptyDir
* Storage provisioning
* Volume mounts
* Persistence testing
* Storage troubleshooting

## 📈 Next Steps

### Immediate

* Add `index.html`
* Add upload functionality
* Define resource limits

### Advanced

* `ReadWriteMany` access
* Dynamic provisioning
* File browser UI
* Authentication
* Backup strategies

### Production Considerations

* Cloud-specific StorageClasses
* Volume snapshots
* Storage monitoring
* Network policies

## 🔍 Practical Exercises

### Exercise 1: Scale and Observe

```bash
kubectl scale deployment file-server-persistent --replicas=2
kubectl scale deployment file-server-persistent --replicas=1
```

### Exercise 2: Modify Content

```bash
kubectl exec -it $POD -- sh -c 'echo "File 1" > /usr/share/nginx/html/file1.txt'
kubectl exec -it $POD -- sh -c 'echo "File 2" > /usr/share/nginx/html/file2.txt'
```

> Educational lab on persistent storage in Kubernetes. Ideal for understanding data durability in containerized environments.

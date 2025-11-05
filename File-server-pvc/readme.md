Step-by-Step: How We Built the Persistent File Server
Phase 1: Understanding the Problem
Learned that emptyDir loses files when pods restart

Identified the need for persistent storage for file servers

Phase 2: Created Persistent Volume Claim (PVC)
bash
# Created file-server-pvc.yaml
```
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
kubectl apply -f file-server-pvc.yaml
PVC = Request for storage ("I need 5GB")

Bound automatically by Minikube to a Persistent Volume

Phase 3: Created Persistent Deployment
bash
# Created file-server-deployment-persistent.yaml  
```
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
kubectl apply -f file-server-deployment-persistent.yaml
Uses PVC instead of emptyDir

Same Nginx file server but with persistent storage

Service exposes it on port 30002

Phase 4: Tested Persistence
bash
# Set pod variable
POD=$(kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}')

# Created test files
kubectl exec -it $POD -- sh -c 'echo "PERSISTENT FILE" > /usr/share/nginx/html/test.txt'

# Simulated pod crash
kubectl delete pod $POD

# Waited for new pod and updated variable
kubectl wait --for=condition=ready pod -l app=file-server-persistent --timeout=60s
POD=$(kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}')

# Verified files survived
kubectl exec -it $POD -- ls -la /usr/share/nginx/html/
Key Concepts Demonstrated:
PVC → Request storage from cluster

PV → Actual storage provisioned (auto by Minikube)

Volume Mount → Connect storage to container

Data Persistence → Files survive pod restarts

Shell Variables → Temporary session storage

Current Architecture:
text
Internet → NodePort:30002 → File Server Service → File Server Pod → Persistent Volume
Result: Your file server now maintains files even when pods crash/restart! 

------

 Pod Label Mismatch
Problem: no matching resources found / array index out of bounds

Root Cause: Using wrong label selector (app=file-server vs app=file-server-persistent)

Fix: Use correct label

bash
# Check actual labels:
kubectl get pods --show-labels
# Use correct label:
kubectl get pods -l app=file-server-persistent


Persistent Volume Connectivity
Problem: Empty directory after PVC creation

Root Cause: Fresh PV starts empty, need to populate it

Fix: Create files after deployment

bash
kubectl exec -it $POD -- sh -c 'echo "content" > /path/file.txt'


Variable Scope Issues
Problem: $POD variable empty in new terminal session

Root Cause: Shell variables are session-specific

Fix: Re-get pod name in each session

bash
POD=$(kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}')


---
Key Debugging Commands Used:
bash
kubectl get pods --show-labels                    # Check pod labels
kubectl describe pod <pod-name>                   # Detailed pod info
kubectl get pvc                                   # Check persistent volumes
kubectl logs <pod-name>                          # Check container logs
kubectl exec -it <pod> -- ls -la /path/          # Debug file system
kubectl get events --sort-by=.metadata.creationTimestamp  # Cluster events

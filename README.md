Here's the **cleaned-up, emoji-free professional version** of your `README.md`:

````markdown
# Kubernetes DNS Troubleshooting & GitOps Demo

Hi **gaurav_bohra** sir,

I tried to replicate everything exactly as per your task, especially the requirement:

> **Modify CoreDNS or create a network policy that breaks service discovery**  
> **Diagnose with tools like nslookup, dig, tcpdump, and restore functionality**

Here are the detailed steps I followed. This is not based on my own interpretation — every folder and file was created to fully match the intent of your task.

---

## Step-by-Step Breakdown

### 1. `charts/my-app/`

Contains a Helm chart that defines:
- Backend Deployment & Service using [`http-echo`](https://github.com/hashicorp/http-echo)
- Frontend Deployment & Service using NGINX
- Ingress that routes:
  - `/api` → `backend-service`
  - `/ui`  → `frontend-service`
- TLS enabled via a secret named `tls-cert`

**Purpose**: Declarative, reusable way to deploy the application using Helm.

---

### 2. `argocd/app.yaml`

ArgoCD Application manifest configured with:
- Auto-sync
- Prune
- Self-heal
- Source points to the Helm chart in this repo

**Purpose**: Manage deployments via GitOps using ArgoCD.

---

### 3. `tools/coredns-patch.yaml`

Patches CoreDNS `Corefile` to break Kubernetes service discovery:
- Removes internal Kubernetes DNS plugin block

**Purpose**: Simulate a DNS failure scenario from inside the cluster.

---

### 4. `tools/network-policy-block.yaml`

Creates a NetworkPolicy to block:
- UDP traffic on port 53 (DNS)
- Target: All pods attempting to reach CoreDNS in `kube-system` namespace

**Purpose**: Another way to simulate DNS resolution failure.

---

### 5. `tools/diagnosis.md`

Step-by-step instructions to debug DNS issues using:
- `nslookup`
- `dig`
- `tcpdump`

Also includes recovery steps:
- Restart CoreDNS
- Delete the blocking NetworkPolicy

**Purpose**: Help diagnose and restore broken DNS functionality.

---

### 6. `misconfigs/values-bad.yaml`

Intentionally invalid Helm values:

```yaml
replicaCount: "three"            # ❌ should be an integer
image:
  tag: "nonexistent-v1.0"        # ❌ invalid image tag
resources:
  limits:
    cpu: "10cores"               # ❌ invalid CPU format
service:
  port: "eighty"                 # ❌ should be an integer
````

**Purpose**: Simulate deployment failures for ArgoCD rollback testing.

---

## Repository Structure

```
.
├── README.md
├── charts/
│   └── my-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── ingress.yaml
│           └── tls-secret.yaml
├── argocd/
│   └── app.yaml
├── tools/
│   ├── coredns-patch.yaml
│   ├── network-policy-block.yaml
│   ├── debug-pod.yaml
│   └── diagnosis.md
└── misconfigs/
    └── values-bad.yaml
```

---

## Implementation Steps

### 1. Deploy the Application

```bash
kubectl apply -f argocd/app.yaml
argocd app wait my-app --sync
kubectl get pods,svc,ingress -n default
```

### 2. Break DNS Resolution

```bash
# Method 1: CoreDNS Configuration
kubectl apply -f tools/coredns-patch.yaml
kubectl rollout restart deployment/coredns -n kube-system

# Method 2: NetworkPolicy Block
kubectl apply -f tools/network-policy-block.yaml
kubectl apply -f tools/debug-pod.yaml
```

### 3. Diagnose with Tools

```bash
kubectl exec -it debug-pod -- bash

# nslookup testing
nslookup backend-service
nslookup backend-service.default.svc.cluster.local

# dig analysis
dig @10.96.0.10 backend-service.default.svc.cluster.local
dig backend-service.default.svc.cluster.local +trace

# tcpdump capture
tcpdump -i any -n port 53 -A
tcpdump -i any -n host backend-service
```

### 4. Restore Functionality

```bash
# Restore CoreDNS
kubectl rollout undo deployment/coredns -n kube-system

# Remove NetworkPolicy
kubectl delete -f tools/network-policy-block.yaml

# Verify Recovery
kubectl exec -it debug-pod -- nslookup backend-service
```

### 5. ArgoCD Rollback Demo

```bash
# Apply broken configuration
argocd app set my-app --values-literal-file misconfigs/values-bad.yaml

# Check application health
argocd app get my-app

# Perform rollback
argocd app history my-app
argocd app rollback my-app <REVISION-ID>
argocd app sync my-app
```

---

## Troubleshooting Commands

### DNS Resolution Testing

```bash
nslookup backend-service
dig backend-service.default.svc.cluster.local
host backend-service.default.svc.cluster.local
```

### Network Connectivity

```bash
telnet backend-service 80
nc -zv backend-service 80
curl backend-service
```

### Packet Capture

```bash
tcpdump -i any -n port 53
tcpdump -i any -n host backend-service
tcpdump -i any -n -vv 'port 53 or port 80'
```

### CoreDNS Investigation

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns
kubectl get configmap coredns -n kube-system -o yaml
```

---

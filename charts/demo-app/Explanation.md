# 📦 Helm Chart - `demo-app`

This Helm chart deploys a simple **frontend-backend** application architecture in Kubernetes with **TLS-enabled Ingress** and **path-based routing**. It is a part of a larger GitOps + DNS Failure Simulation demo.

---

## 📁 Folder Structure & Purpose

```

charts/
└── demo-app/
├── Chart.yaml
├── values.yaml
└── templates/
├── ingress.yaml
├── backend-deployment.yaml
├── backend-service.yaml
├── frontend-deployment.yaml
└── frontend-service.yaml

````

---

## 🔍 Explanation of Each File

### ✅ `Chart.yaml`
- Contains metadata for the Helm chart (e.g., name, version, description).
- Required for any Helm chart.

### ✅ `values.yaml`
- Default configuration values like image name, replica count, and service port.
- These values are injected into templates using `{{ .Values }}` syntax.
- Can be overridden during install/upgrade.

### ✅ `templates/ingress.yaml`
- Defines an **NGINX Ingress** resource.
- Routes:
  - `/api` → `backend-service`
  - `/ui` → `frontend-service`
- Uses **TLS** with a Kubernetes secret named `tls-cert`.
- Enables external access via:
  - `https://myapp.local/api`
  - `https://myapp.local/ui`

### ✅ `templates/backend-deployment.yaml`
- Deploys the **backend** app using the `hashicorp/http-echo` image.
- Responds with static text (e.g., "Hello from Backend API").
- Simulates a simple API service.

### ✅ `templates/backend-service.yaml`
- Exposes the backend deployment as a Kubernetes service named `backend-service`.
- Type: `ClusterIP`
- Port: 80

### ✅ `templates/frontend-deployment.yaml`
- Deploys a basic **frontend** app using the default `nginx` image.
- Can serve static files or a default index page.
- Simulates a basic web UI.

### ✅ `templates/frontend-service.yaml`
- Exposes the frontend deployment as a Kubernetes service named `frontend-service`.
- Type: `ClusterIP`
- Port: 80

---

## ✅ Why I Created This

This chart was created as part of a hands-on task to:

- Demonstrate NGINX Ingress with **TLS** and **path-based routing**
- Separate routing for `/api` (backend) and `/ui` (frontend)
- Provide a clean, minimal Helm-based setup for GitOps via **ArgoCD**
- Integrate with tools like CoreDNS, tcpdump, and nslookup to simulate and troubleshoot **DNS issues**
- Allow rollback testing with **Helm values misconfiguration**

Every file in this chart serves a specific purpose tied directly to the task requirements. The chart is modular, customizable, and designed for both learning and real-world usage.

---

## 🚀 Usage Example

```bash
# 1. Create TLS secret (if not already done)
kubectl create secret tls tls-cert \
  --cert=path/to/cert.crt \
  --key=path/to/key.key \
  -n default

# 2. Install Helm chart
helm install my-app ./charts/my-app

# 3. Add to /etc/hosts
echo "127.0.0.1 myapp.local" | sudo tee -a /etc/hosts

# 4. Access the services
curl -k https://myapp.local/api
curl -k https://myapp.local/ui
````

---

## 🧩 Next Steps

Once deployed, this chart integrates with:

* **ArgoCD** for GitOps-based continuous delivery
* **CoreDNS patching** or **NetworkPolicy** to simulate DNS failures
* **Diagnostic tools** like `dig`, `nslookup`, and `tcpdump` to troubleshoot networking

---

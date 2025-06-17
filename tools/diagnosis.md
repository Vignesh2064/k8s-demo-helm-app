## DNS Debug Tools

```bash
kubectl exec -it <pod> -- nslookup backend-service
kubectl exec -it <pod> -- dig backend-service.default.svc.cluster.local
kubectl exec -it <pod> -- tcpdump -i any port 53
```

## Restore CoreDNS
```bash
kubectl rollout restart deployment coredns -n kube-system
```

## Remove Network Policy
```bash
kubectl delete -f tools/network-policy-block.yaml
```

# README.md
# NGINX Ingress + ArgoCD GitOps Demo

This project demonstrates:
- NGINX Ingress with TLS and path-based routing
- Backend & frontend deployments
- Simulating and diagnosing DNS issues
- GitOps with Helm + ArgoCD
- Misconfig simulation + rollback

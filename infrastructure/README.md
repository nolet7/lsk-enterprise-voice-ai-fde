# Production deployment reference, NOT a ready-to-run release

These manifests are scaffolding: replace immutable image tags, configure external HTTPS ingress, TLS, LiveKit SFU/managed LiveKit, inference credentials and provision runtime secrets via approved secret manager. Set LSK_OPERATOR_KEY to a strong value; replace shared key with OIDC/RBAC before exposure. Current application stores data in each process's memory, so API replicas are NOT equivalent to a working clustered system. Replace with tenant-scoped durable database, shared cache/queues and distributed rate limits before enabling replicas. Do not apply to customer traffic.

Build from repo root:
```bash
docker build -f infrastructure/docker/Dockerfile.api -t lsk-api:local .
docker build -f infrastructure/docker/Dockerfile.worker -t lsk-worker:local .
kubectl kustomize infrastructure/k8s
```

Approved managed LiveKit is preferred for initial FDE delivery to avoid operating an SFU. Self-hosted option requires UDP/TURN load balancing, room routing, TLS, geographic placement, media QoS and capacity testing. SIP/PSTN requires separate provider trunks and consent policies; not configured in this repository.

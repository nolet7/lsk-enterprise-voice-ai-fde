# Middleware boundaries

POC uses FastAPI endpoint validation and explicit operator key for privileged console calls. Before production use: replace shared operator key with OIDC, RBAC and tenant-scoped claims; enforce per-caller rate limits, cryptographically binding verified customer identity to the LiveKit room, short-lived tokens, and audit trails. Do not enable public Internet access with the default demo key.

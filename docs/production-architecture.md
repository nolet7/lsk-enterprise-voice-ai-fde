# Production target architecture (not deployed)

## User to fulfillment and media/signaling
```mermaid
flowchart LR
 Customer[WebRTC browser / approved SIP gateway] --> Edge[TLS edge and auth]
 Edge --> API[Customer experience API]
 Customer --> SFU[Managed LiveKit / approved self-hosted SFU]
 SFU <--> Workers[Autoscaled voice agents STT LLM TTS]
 Workers -->|scoped service identity| API
 API --> PG[(Tenant-scoped Postgres)]
 API --> Redis[(Rate limit / ephemeral state)]
 API --> CRM[Project 1 v1 API or validated standalone adapter]
 API --> Handoff[Contact center routing and real human bridge]
 Workers --> OTEL[OpenTelemetry collector]
 API --> OTEL
 OTEL --> Monitor[Prometheus / tracing / alerts]
```

## Failure recovery
```mermaid
flowchart TD
 A[Call begins] --> B{Speech provider healthy?}
 B -->|Yes| T[Verified scoped tool calls]
 B -->|Timeout| C[Bounded retry if safe and idempotent]
 C -->|Recovered| T
 C -->|Failed| F[Deterministic failure message]
 T --> D{Answer grounded?}
 D -->|Yes| R[Speak permitted result]
 D -->|No| F
 F --> H[Case and human queue with explicit transfer state]
 H --> E{Human media bridge acknowledged?}
 E -->|Yes| X[Transfer complete]
 E -->|No| Y[Offer callback, maintain connection, or end explicitly]
```

Human audio bridging, enterprise identity, persistent state and distributed tracing are **target state only** and not present in the POC code. Do not present these drawings as deployed infrastructure.

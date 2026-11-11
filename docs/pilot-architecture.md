# Pilot architecture

```mermaid
flowchart LR
 Browser[Concurrent WebRTC browsers] --> LK[LiveKit SFU]
 LK <--> Pool[Voice worker pool]
 Pool --> API[Contact center service]
 API --> Store[(Pilot database - to implement)]
 Pool --> OTEL[Tracing / metrics integration - to implement]
 API --> Dashboard[Operator real-time dashboard - to implement]
 Cases[Evaluation replay] --> API
 Flags[Feature flag gate] -.-> Pool
 LK --> Error[Media interruption and fallback testing]
```

Pilot branch adds replay/load scaffolding and evidence requirements. Durable database, real-time streaming operator views, LiveKit concurrency measurements and feature-flag backend remain engineering work. Source artifacts must not be confused with a signed-off pilot.

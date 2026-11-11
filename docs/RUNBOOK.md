# Production runbook (pre-go-live checklist)

1. Check provider status, LiveKit room connectivity, signaling errors, ICE/TURN routes, STT/TTS/LLM uptime, request volume and worker concurrency.
2. Confirm customer verification is still enforced and no private records are spoken pre-verification. If violated, immediately disable AI and route to a human; initiate incident response and privacy assessment.
3. For elevated latency inspect separate STT, LLM, tool, TTS and packet/jitter spans; shed new sessions with HTTP 429 before overload.
4. On tool 5xx apply bounded retries only for idempotent reads; for writes require idempotency keys and explicit confirmation. Never retry a sensitive action blindly.
5. If media disruption occurs, announce failure (when audio channel works) and offer callback/agent; report unbridged cases distinctly.
6. Canary rollout: deploy to internal synthetic tenants, then limited real opt-in traffic, compare error budget and conversation adjudication; automatic rollback on objective regression.
7. Rollback: restore previous immutable API+worker image versions and compatible schema; verify session continuity and case preservation; never force rollback through incompatible migrations.
8. Record timestamps, impacted tenants, sampled traces, corrective actions, owner and customer notification decisions in incident log.

Current implementation does not meet runbook prerequisites: state is in-memory, no production identity provider, no completed live transfer and no provider credentials.

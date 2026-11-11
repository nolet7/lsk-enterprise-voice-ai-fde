# CTO mandate and phase gates

Business: fictional B2B food-ingredient distributor; delivery queries, order status, invoice questions, product information and safe transfer. Excludes manufacturing.

## POC exit
- Start legacy web-chat or browser-voice contact-center session; view agent queue and case.
- Prove 403 before verification and 403/404 for cross-customer lookup; 3 unsuccessful PINs lock verification.
- With real LiveKit + model credentials: record real browser microphone → inference → synthesized speaker audio test, interruption and fallback observation, transfer case created.
- Log real observed RTT and voice latencies; never claim POC voice success without hands-on test.

## Pilot exit
- Multi-call concurrency and session capacity tests; transcript stream and dashboard with explicit consent.
- Eval replay, hallucination/abstention, escalation and failure drills; quality scoring and operator acceptance.

## Production exit
- OIDC tenant isolation, distributed state and limits, secure human media bridge, model governance, prompt injection tests.
- Kubernetes rollout/canary, metrics/SLO, resilience, backup, credential rotation, tracing, incident runbook and customer handover.

**No phase is accepted without verifiable evidence**; source-code branch names are not evidence of release approval.

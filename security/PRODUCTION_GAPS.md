# Release blockers

1. Identity/tenant model: replace public session creation and unbound session IDs with authenticated tenant-bound identities, user/session authorization, rate limiting and abuse controls.
2. Customer verification: implement secure authenticated verification challenge (e.g., independently delivered OTP or account-authenticated SSO), not publicly documented demo PINs. Support secure DTMF through a compliant telephony provider when enabled.
3. Durable state: migrate fixtures to schema-enforced Postgres with row-level security and encryption, Redis for ephemeral session state and distributed limits; no in-memory stores at scale.
4. Consented transcript ingestion: enforce retention, deletion, access audit, PII redaction in all sinks, regional model/data processing terms and privacy DPIA.
5. Human live media handoff: coordinate agent room transfer and media bridge with explicit confirmation before reporting completion.
6. Real-time monitoring: instrument customer audio path, speech pipeline, provider billing, tracing, outlier/error sampling, SLOs and alert drills.
7. Model safety: evaluation-based release gating, prompt injection defense, tight tool allowlists, per-tenant query authorization, confidence/uncertainty policy, prompt versioning and rollback.
8. Infra release: supply actual secret manager, approved LiveKit architecture, TLS, ingress, egress and network policies, image signing/SBOM, vulnerability and penetration tests.

Production branch contains deployment *templates* and gates; these blockers prevent claiming production readiness.

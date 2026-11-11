# Proposed SLOs (draft; no measurements)

Provisional targets require business acceptance and real baseline:
- WebRTC join availability: 99.9% over 28 days (successful negotiated session / eligible attempts)
- Core verified order API availability: 99.9% over 28 days (non-5xx / valid requests)
- Turn latency: propose p95 < 2500 ms after measured regional/provider baseline; includes endpointing to audible output
- Human transfers: define success only after human and customer share an established live session; no success claim for case creation alone

Burn-rate alerts at 14.4x for 1h/5m and 6x for 6h/30m pending SRE review. All targets aspirational. Instrument source-specific time windows, trace exemplars and sampling bias. Do not put PII in tags or alerts.

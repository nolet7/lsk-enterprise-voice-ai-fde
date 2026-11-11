# Pilot evaluation protocol

Run `python -m evals.replay` from repo root. The harness tests privacy and deterministic API tools only. These tests do **not** demonstrate hallucination control, live interruption, STT accuracy, voice quality, latency or human audio bridging. Those require real voice sessions, model transcripts, reviewer rubric and persistent measurements.

Before customer pilot: have independent annotators rate correctness, helpfulness, consent adherence, escalation appropriateness and audio intelligibility on a 1–5 rubric. Save raw numerator/denominator, timestamp, model, room ID (pseudonymized), and cost source; never supply invented KPIs.

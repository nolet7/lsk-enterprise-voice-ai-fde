# Operational instrumentation contract

Required dimensions: tenant (bounded pseudonym), channel, model_version, workflow, result. Never put customer IDs, phone numbers, transcript or order IDs in Prometheus labels. Definitions:

- time_to_first_audio_ms: first user audio to first agent audio, with wall/monotonic timestamps and sample count
- turn_latency_ms: endpointed user turn to first bot audible output
- tool_success_rate = successful tool calls / attempted tool calls
- transfer_completion_rate = transfers accepted with live customer connected / transfer requests (case-only transfer does NOT count)
- call_failure_rate = browser call setup/media failures / attempts
- task_completion_rate = independently reviewed completed tasks / eligible tasks
- cost_per_interaction = provider billed audio+tokens+LiveKit usage / completed interactions, measured not guessed
- human_conversation_quality = mean blind reviewer score with sample size

POC /metrics is a health instrumentation endpoint only; it is **not** yet wired to these product KPI series. Pilot must instrument LiveKit usage/events and distributed storage before declaring gate passed.

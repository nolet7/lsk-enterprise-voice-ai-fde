# Pilot evidence register

| Gate | Evidence required | Current state |
|---|---|---|
| Deterministic API privacy tests | pytest and replay output | CI pending |
| Multiple real simultaneous voice sessions | room recordings and worker metrics | Not tested |
| STT / LLM / TTS latency percentiles | instrumented traces p50/p95/p99 | Not tested |
| Live transcript with consent | stream + consent propagation audit | Not implemented |
| Human-rated agent quality | reviewer rubric + sample size | Not measured |
| Model hallucination/abstention | adjudicated speech cases | Not measured |
| Fault injection / recovery | failure scenarios and recovery times | Not run |
| Feature flag rollback | enabled/disabled call transcripts | Not implemented |

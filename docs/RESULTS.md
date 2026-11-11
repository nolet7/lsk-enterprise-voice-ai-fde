# Verification results register — 2026-11-11

| Test / metric | Observed outcome |
|---|---|
| GitHub source commits and phase branches | Verified main, poc, pilot and production refs via GitHub API |
| Python unit/contract tests | GitHub Actions successful: 8 passed, 1 warning in 0.42s (run 43090925443); no local test execution |
| Live WebRTC microphone / two-way speech | Not run; LiveKit and inference credentials unavailable; browser remote-audio wiring updated after above CI run |
| Voice interruption / first-audio latency | Not measured |
| Real concurrent browser calls | Not run |
| Transfer to human audio | Not implemented; queue case only |
| PSTN/SIP integration | Not configured; no credentials |
| Deterministic pilot replay | GitHub Actions success (run 43090925203); provider/model quality not tested |
| Task completion, voice quality, cost | Not measured |

Use CI stdout, observed provider logs, real spans and operator rating forms to fill results. Do not substitute target SLOs for measured data.

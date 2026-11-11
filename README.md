# LSK Enterprise Voice AI — FDE

Fictional B2B food ingredients distributor. Existing contact center first; AI augmentation second. No manufacturing features.

## Promotion process

- `main`: CTO mandate, business requirements, and phase-gate plan.
- `poc`: standalone legacy contact-center simulator plus credential-gated LiveKit voice AI implementation.
- `pilot`: concurrency, replay/evaluations, instrumentation, failure testing, flags.
- `production`: Kubernetes/GitOps, SLOs, canary/rollback, operator and customer handover.

Branches represent **code maturity targets**, not claims of deployed production services. Production promotion requires the gates in docs/acceptance.md and recorded real evidence. LiveKit credentials and STT/LLM/TTS inference access are required for actual two-way speech; browser demo uses WebRTC (not PSTN). Never place secrets in the repository.

### Quick start after checking out a phase branch

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate # Windows Git Bash: source .venv/Scripts/activate
pip install -r backend/requirements.txt
uvicorn backend.app:app --host 127.0.0.1 --port 18743
# separate terminal, for voice: pip install -r voice-agents/requirements.txt && python voice-agents/worker.py dev
```

Visit http://127.0.0.1:18743 . Do not represent any simulated SMS or call event as an actual telephone call. See docs/ for architectures, demonstration, contracts and operational limitations.

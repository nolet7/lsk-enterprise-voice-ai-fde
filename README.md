# LSK Enterprise Voice AI — FDE

Legacy-first, fictional B2B food-ingredients contact center, with browser WebRTC LiveKit AI voice, web chat, and explicitly simulated SMS. No manufacturing and no claims of PSTN calling.

## Branch progression
- main: CTO charter and acceptance principles
- poc: working standalone API/console and LiveKit voice worker (credential dependent)
- pilot: evaluation, replay, basic load, instrumentation and quality gates
- production: deployment reference, hardening plan, SLOs and runbooks

## Local startup
```bash
cp .env.example .env
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash (Linux: source .venv/bin/activate)
pip install -r backend/requirements.txt
python -m uvicorn backend.app:app --host 127.0.0.1 --port 18743
# For real voice, in another shell:
pip install -r voice-agents/requirements.txt
python voice-agents/worker.py dev
```

Visit http://127.0.0.1:18743 . Set LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and provision working STT/LLM/TTS access; then set LSK_ENABLE_VOICE=true. No calls or measured production KPIs are claimed. Read docs/demo.md and docs/acceptance.md.

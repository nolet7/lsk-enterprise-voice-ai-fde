# Five-minute POC demonstration

0:00–1:00 CTO mandate, legacy architecture, fixtures and consent policy.
1:00–2:00 Start session; attempt order lookup before verification (403); enter demo customer C100 and PIN 2468; retrieve O-1001 and delivery ETA; attempt O-2001 (404).
2:00–3:00 With *actual* LiveKit account credentials and live inference provisioned, enable voice, start worker, click Connect real browser voice and speak: 'Where is order O-1001?' Observe response/audio and interruption. Without credentials, demonstrate explicit HTTP 503 — never substitute an invented voice interaction.
3:00–4:00 Request human; case appears in operator console; accept case. Explain this is a **case handoff**, not a bridged audio handoff.
4:00–5:00 Show threat model, phase gates, observability plan, and open pilot/production work. No invented latency or resolution measurements.

Run backend on port 18743; LiveKit credentials in private .env; voice worker: python voice-agents/worker.py dev.

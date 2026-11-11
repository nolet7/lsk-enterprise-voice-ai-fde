# Architecture / workflows

## POC: caller → fulfillment
```mermaid
flowchart LR
 C[Browser customer] -->|session, verify| API[Legacy FastAPI contact center]
 API --> D[(Fictional customer/order fixtures)]
 C -->|WebRTC media & signaling| LK[LiveKit room]
 LK <--> W[LiveKit Agents worker STT LLM TTS]
 W -->|guarded API tools| API
 API -->|case queued| H[Human agent console]
 H -->|accept case, no live audio bridge yet| API
```

## Media versus signaling
```mermaid
sequenceDiagram
 participant B as Browser
 participant A as Backend token service
 participant L as LiveKit media room
 participant W as Voice worker
 B->>A: Create session, request room token
 A-->>B: Room-scoped token
 B->>L: WSS signaling and WebRTC audio
 L->>W: Published customer media
 W->>W: STT → LLM/tool → TTS; interruption handling via framework
 W-->>L: Synthesized audio
 L-->>B: Playback via WebRTC track
```

## CRM lookup, handoff and failure recovery
```mermaid
flowchart TD
 U[Unverified customer] --> V{Secure verification passed?}
 V -->|No| N[Withhold account details; retry or human]
 V -->|Yes| T[AI order lookup tool]
 T -->|success| O[Return verified customer's status]
 T -->|timeout, mismatch, uncertain| F[Fallback response]
 F --> X[Create case with permitted context]
 X --> Q[Human queue]
 Q --> A[Agent accepts case]
```

Operator dashboard: browser → privileged API → queue/case/event state. All events are simulated or real browser events, never claimed PSTN. Pilot/production views on their own branches.

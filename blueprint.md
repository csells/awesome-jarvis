# Jarvis Blueprint

A reference architecture for a real-life J.A.R.V.I.S. and three ways to build one. Every component named here is linked from the [main list](readme.md).

## The Loop

```
            ┌──────────────────────────── Proactivity ───────────────────────────┐
            │  heartbeats · schedules · events (doorbell, calendar, inbox)       │
            ▼                                                                    │
 mic ─► Wake word ─► VAD + turn detection ─► Speech-to-text ─┐                    │
                                                            ▼                    │
 camera / presence / screen ───────────────────────────►  BRAIN  ◄──► Memory     │
                                                          (LLM +      (facts,    │
                                                         agent loop)  history,   │
                                                            │         skills)    │
                                                            ▼                    │
                                  Tools: MCP · home · browser · computer · APIs ─┘
                                                            │
 speaker ◄─ Text-to-speech ◄────────────────────────────────┘
       (or skip STT and TTS entirely with a speech-to-speech model)
```

Tony's Jarvis does five things that most assistants still don't:

1. **Always listening, rarely interrupting.** A wake word or a speech-to-speech model with good turn detection lets you talk naturally without buttons. Budget about 800 ms from the end of your speech to the start of Jarvis's reply. Past that, a conversation stops feeling like one.
2. **Remembers you.** Long-term memory of preferences, people, and past conversations, kept separate from the chat transcript.
3. **Acts, not just answers.** Tools for your home, calendar, email, browser and computer, with an authority model for what it may do without asking.
4. **Notices things.** Cameras, presence sensors, screen context and event streams feed the brain even when you aren't talking.
5. **Speaks first.** Heartbeats and schedules let it interrupt only when something matters.

## Starter Builds

### 1. Fully Local on a Mac

Private and offline. A Mac mini with 32 GB or more of memory is enough.

| Layer | Pick |
|---|---|
| Ears | openWakeWord → Silero VAD + Smart Turn → Parakeet via FluidAudio or mlx-audio |
| Brain | Ollama or MLX LM running a Qwen or gpt-oss model |
| Harness | Pipecat for the voice loop, with a Pydantic AI or smolagents agent inside |
| Memory | Mem0 or Basic Memory |
| Hands | MCP servers: filesystem, Playwright MCP, Home Assistant MCP Server |
| Voice | Kokoro or Pocket TTS |
| Proactivity | A cron job that runs the agent against a checklist every 30 minutes |

For a head start, study [GLaDOS](https://github.com/dnhkng/GLaDOS) and [isair/jarvis](https://github.com/isair/jarvis), which already wire most of this together.

### 2. Home Assistant–Centric

For a Jarvis that lives in the house and talks to everyone in it.

| Layer | Pick |
|---|---|
| Body | Home Assistant + Voice Preview Edition or Satellite1 in each room |
| Ears | microWakeWord on the device → Speech-to-Phrase or faster-whisper via Wyoming |
| Brain | Home Assistant conversation agent backed by Ollama (Home LLM) or a cloud model |
| Eyes | Frigate + LLM Vision; Bermuda or ESPresense for who is in which room |
| Voice | Piper |
| Proactivity | Automations that call Assist to start conversations and AI Task to reason about camera snapshots |
| Screen | View Assist on wall tablets |

### 3. Cloud-First Butler

The best quality right now, if you're willing to trust a provider with your data.

| Layer | Pick |
|---|---|
| Voice loop | OpenAI Realtime API or Gemini Live API (speech-to-speech) through LiveKit Agents or Pipecat |
| Harness | OpenClaw or Hermes Agent for chat channels, memory, skills and heartbeats |
| Hands | Composio or Zapier MCP for SaaS, ha-mcp for the house, browser-use or Claude in Chrome for the web |
| Memory | The harness's own memory files plus Graphiti for a temporal knowledge graph |
| Capture | Screenpipe on the desktop, Omi on your lapel |

## Design Notes

- **Give it a persona, but not someone else's voice.** Voice design from a text prompt (VoxCPM, Qwen3-TTS, OpenAI TTS instructions) can give you a dry British butler without cloning an actor.
- **Separate talking from working.** Keep the voice loop fast. Hand long tasks to background agents and have them report back, which is the pattern Qwen Audio Agent and OpenClaw follow.
- **Set its authority explicitly.** Decide which actions need confirmation, such as sending email, spending money or unlocking doors, and enforce that in the tool layer rather than the prompt.
- **Measure it.** Track end-of-speech-to-first-audio latency, wake word false accepts per day, and task success on your own household tasks. The benchmarks in the main list are a starting point.

# Jarvis Blueprint

A reference architecture for a real-life J.A.R.V.I.S. and three ways to build one. Every component named here is linked from the [main list](README.md).

## The Loop

```
            ┌──────────────────────────── Proactivity ─────────────────────────────┐
            │  heartbeats · schedules · events (doorbell, calendar, inbox)         │
            ▼                                                                      │
 mic ─► Wake word ─► VAD + turn detection ─► Speech-to-text ─┐                      │
                                                            ▼                      │
 camera / presence / screen ────────────────────────►  TALKER (fast) ◄──► Memory   │
                                                            │                      │
                                          delegate · status · cancel               │
                                                            ▼                      │
                              WORKERS: sub-agents · coding agents (ACP) · jobs     │
                                  │                                   │            │
                                  ▼                                   ▼            │
            Tools: MCP · home · browser · computer        approvals · audit log ───┘
                                                                      │
 speaker ◄─ Text-to-speech ◄── talker ──► HUD / orb / avatar ◄────────┘
       (or skip STT and TTS entirely with a speech-to-speech model)
```

The key move is splitting the **talker**, a fast voice loop that never blocks, from the **workers**, slower agents that do the actual work. The talker delegates, reports progress, relays approval requests and lets you cancel. The HUD shows both: what Jarvis is doing (listening, thinking, speaking) and what its staff is doing (working, blocked, waiting for you). This is the Talker-Reasoner pattern from the research section, and it is how Qwen Audio Agent, Paseo, OpenClaw and the Omarchy voice plugins are built.

Tony's Jarvis does seven things that most assistants still don't:

1. **Always listening, rarely interrupting.** A wake word or a speech-to-speech model with good turn detection lets you talk naturally without buttons. Budget about 800 ms from the end of your speech to the start of Jarvis's reply. Past that, a conversation stops feeling like one. The [Voice AI primer](https://voiceaiandvoiceagents.com/) breaks down the budget.
2. **Remembers you.** Long-term memory of preferences, people, and past conversations, kept separate from the chat transcript.
3. **Acts, not just answers.** Tools for your home, calendar, email, browser and computer, with an authority model for what it may do without asking.
4. **Notices things.** Cameras, presence sensors, screen context and event streams feed the brain even when you aren't talking.
5. **Speaks first.** Heartbeats and schedules let it interrupt only when something matters.
6. **Shows its work.** An orb, avatar or HUD makes its state visible at a glance, and a dashboard shows every running task.
7. **Runs a staff.** It hands long work to other agents, watches them, relays their questions, and stops them when you say so.

## Starter Builds

### 1. Fully Local on a Mac

Private and offline. A Mac mini with 32 GB or more of memory is enough.

| Layer | Pick |
|---|---|
| Ears | Silero VAD + Smart Turn → Parakeet through mlx-audio (add openWakeWord in front with a little glue code) |
| Talker | Pipecat voice loop with a Pydantic AI agent inside, on Ollama or MLX LM running a Qwen or gpt-oss model |
| Workers | Claude Code or Codex driven over the Agent Client Protocol, or Pydantic AI sub-agents |
| Memory | Mem0 or Basic Memory |
| Hands | MCP servers: Playwright MCP, Home Assistant MCP Server |
| Voice | Kokoro or Pocket TTS |
| Screen | ElevenLabs UI or LiveKit Agents UI orb in a small always-on-top window, plus Pixel Agents or Claude HUD for the workers |
| Proactivity | A cron job that runs the agent against a checklist every 30 minutes |

For a head start, study [GLaDOS](https://github.com/dnhkng/GLaDOS) and [isair/jarvis](https://github.com/isair/jarvis) for the voice loop, and OpenLive for local voice driving ACP agents. If you want a native macOS app instead of Python, FluidAudio gives you streaming Parakeet, Kokoro and echo cancellation on the Neural Engine.

### 2. Home Assistant–Centric

For a Jarvis that lives in the house and talks to everyone in it.

| Layer | Pick |
|---|---|
| Body | Home Assistant + Voice Preview Edition or Satellite1 in each room |
| Ears | microWakeWord on the device → Speech-to-Phrase or faster-whisper via Wyoming |
| Talker | Home Assistant conversation agent backed by Ollama (Home LLM) or a cloud model |
| Eyes | Frigate + LLM Vision; Bermuda for who is in which room |
| Voice | Piper |
| Screen | View Assist on wall tablets, MagicMirror² in the hallway |
| Workers | Hermes Agent or OpenClaw connected through the Home Assistant MCP Server for anything beyond the house |
| Proactivity | Automations that call Assist start_conversation to speak first and AI Task to reason about camera snapshots |

### 3. Cloud-First Butler

The best quality right now, if you're willing to trust a provider with your data.

| Layer | Pick |
|---|---|
| Talker | OpenClaw's Talk mode, or the OpenAI Realtime API or Gemini Live API through LiveKit Agents or Pipecat with one `delegate` tool that forwards work to the harness |
| Harness | OpenClaw or Hermes Agent for chat channels, memory, skills, heartbeats and sub-agents |
| Workers | Claude Code and Codex over ACP from the harness, overseen from Paseo or Happy on your phone |
| Hands | Composio or Zapier MCP for SaaS, ha-mcp for the house, browser-use or Claude in Chrome for the web |
| Memory | The harness's own memory files plus Graphiti for a temporal knowledge graph |
| Screen | The harness's dashboard or HUD on the desktop, Meta Ray-Ban Display or Even G2 glasses on the go |
| Capture | Screenpipe on the desktop, Omi on your lapel |

Don't want to build? Install a finished one from the [Jarvis Agents](README.md#jarvis-agents) section. On Omarchy, `omarchy plugin add` hey-jarvis or omavoice and you'll be talking to Claude Code within minutes.

## Design Notes

- **Give it a persona, but not someone else's voice.** Voice design from a text prompt (VoxCPM, Qwen3-TTS, OpenAI TTS instructions) can give you a dry British butler without cloning an actor.
- **Separate talking from working.** Keep the voice loop fast and hand long tasks to workers that report back. See Talker-Reasoner and Asynchronous Tool Usage in the research section.
- **Make the staff visible.** Show which workers are running, which are blocked on you, and what they did. A spoken summary plus a glanceable HUD beats a scrolling log.
- **Set its authority explicitly.** Decide which actions need confirmation, such as sending email, spending money, pushing code or unlocking doors. Enforce that in the tool layer rather than the prompt, surface each approval where you are (voice, phone, HUD), and keep an audit log.
- **Close the loop by voice.** The gap in every agent we tested: you can talk to it, but approving, denying or cancelling its workers still needs a click. Route approval requests into the voice conversation ("Claude wants to run `rm -rf build`. Allow?") and accept a spoken yes, no or stop, with a visible card as the fallback.
- **Always have a kill switch.** "Jarvis, stop" should halt speech and cancel running workers, not just end the sentence.
- **Measure it.** Track end-of-speech-to-first-audio latency, wake word false accepts per day, how often workers need you, and task success on your own household tasks. The benchmarks in the main list are a starting point.

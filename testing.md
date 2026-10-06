# Hands-On Testing

I build the [scorecard](README.md#scorecard) in three passes. The [testing methodology](methodology.md) describes them in full so you can test new entries the same way. AI agents (Claude, through Claude Code) did the reviews and ran the lab tests under my direction.

1. **Code review.** A reviewer scored every agent on each pillar from its source code and docs, not its README.
2. **Blind review.** A second, independent reviewer re-scored every agent without seeing the first review's scores. Where the two disagreed, the blind score won.
3. **Hands-on lab.** The agents ran on a Mac mini (M4, 32 GB) in September 2026. A text-to-speech engine spoke each test phrase into a virtual microphone, a virtual speaker captured what the agent said out loud, and Whisper transcribed it. Screenshots captured each agent's visual state, and a reviewer looked at every one.

The September 2026 lab reached models through a Claude subscription on the official Claude Code CLI, plus free local models through Ollama, and used no other paid API keys. When a feature needed one, the result says **BLOCKED** rather than counting against the project. Later candidate follow-ups explicitly record any authorized credentials and service substitutions.

## Environments

| Environment | Used for |
|---|---|
| Docker (Ubuntu and Arch Linux ARM) | Paseo, OpenClaw's gateway, Hermes Agent, and an Omarchy 4 desktop built by Omarchy Mac's own installer |
| macOS 26 virtual machine (Tart) | OpenClaw's Mac app, TapQ, JARVIS for Claude Code, usejarvis and Hermes Agent's desktop app |
| Omarchy virtual machine (QEMU, Omarchy M's ARM64 image) | hey-jarvis on real Omarchy and real Hyprland (software rendered) |
| Android emulator (arm64) | Operit and Happy's web client |
| Local voice server (see below) | Voice apps that expect OpenAI's Realtime API |

## Results

PASS means it worked end to end, PARTIAL means some of the pillar worked, FAIL means it didn't work, and BLOCKED means it needs a paid key or hardware the lab didn't have.

| Agent | Voice | Hands-free | Visual | Oversight | Notes |
|---|---|---|---|---|---|
| OpenClaw (Mac app) | PARTIAL | ◐ | PASS | PASS | The "computer" wake word and spoken commands work on-device. Spoken replies couldn't be captured inside the VM. Launched two sub-agents by voice, approved one and cancelled one. A spoken "allow" or "stop" is treated as chat text. |
| OpenClaw (browser Talk) | PASS | ◐ | PASS | PARTIAL | Pointed at the local voice server by config. Answers aloud and barge-in works. Approvals are buttons only. A spoken cancel was followed by OpenClaw re-sending the request. |
| Hermes Agent | PASS | ◐ | PASS | PASS | Local wake word, speech-to-text and text-to-speech. Barge-in worked in the desktop app but failed in the command-line voice mode. Delegated to Claude Code by voice and showed it live on its kanban board; interrupt worked. Its default "smart" approvals let a local model approve an `rm -rf` of a test folder with no human prompt. |
| usejarvis | PASS | ◐ | PASS | PASS | Wake word, local transcription and spoken replies (slow on a small local model). Delegated a task by voice. The pebble overlay showed a sub-pebble per agent. Its default role runs commands without approval. |
| JARVIS for Claude Code | PARTIAL | ◐ | PASS | PASS | Understands speech (no wake word). Speaking back needs a paid Fish Audio key (BLOCKED). Watched a live Claude Code session and cancelled a run by voice. |
| TapQ | PARTIAL | ◐ | FAIL | PARTIAL | The "hey tapq" wake word and spoken approval prompts work on-device, and a Claude Code action was approved and denied by voice. Conversation needs an OpenAI key (BLOCKED). No UI by design. |
| hey-jarvis | PASS | ◐ | PASS | PASS | On real Omarchy and Hyprland, answered through Claude and spoke the reply, with every conversation phase shown. The consent window opens without keyboard focus and is covered by the conversation window, so approving a command needs a click, and an unattended request turns into a denial after 45 seconds. |
| Paseo | PASS | ◐ | PASS | PASS | By voice, created a Claude Code agent, listed it and killed it; barge-in worked. Its voice agent approved its own child agent's file-write permission, and it always launches Claude with a skip-permissions flag. A second voice turn sometimes returned an empty transcript. |
| Happy | BLOCKED | ◐ | PASS | PASS | From a phone, monitored two Claude Code sessions, approved an edit and a command, and cancelled a run. Free voice (20 minutes a month) was confirmed but couldn't be exercised without an emulator microphone. |
| Operit | BLOCKED | ◐ | PASS | FAIL | Ran on a local model as Android's default assistant with its floating avatar. The small local model never made the sub-agent tool call. Its default wake phrase is "O", matched anywhere in a transcript. |
| omavoice | PASS | ◐ | PASS | BLOCKED | Tested with a one-line URL change against the local voice server. Answered aloud with barge-in and a live trace of each step. Delegation wasn't completed because the lab's Claude login had expired in that VM. |
| omarchy-voice | PARTIAL | ◐ | PARTIAL | FAIL | Tested with a one-line URL change. Answered a desktop question aloud. The local 7B model read tool calls aloud instead of making them, which is a limit of the model, not the app. |

Not run hands-on (scored from code only): Qwen Audio Agent, Sutando and OpenClicky, which need paid voice keys; N.E.K.O, AIRI and Newelle. The commercial assistants were scored from vendor documentation.

## Candidate Follow-ups

### Hey Jev — 2026-10-04; adapted follow-up 2026-10-05

**Deferred; not added to the curated list.** At commit `24e4b378350d999d2b45ff2549ea039c2bc7863d`, two code reviews found partial voice and hands-free support, a native visual dashboard, and no agent oversight. Initial tests in the disposable macOS 26.6.2 VM verified startup, local recognition, wake matching and timer functions; cloud conversation was blocked by missing keys.

The follow-up used an explicitly authorized existing Jev key for the unchanged TypeSafe classifier, the official Claude CLI with subscription authentication for answers, macOS speech synthesis, and local Whisper dictation. In this **adapted build**, wake-and-question, spoken answers, timer creation/query/cancellation, a supported Safari-plus-timer command, and voice-started/stopped dictation with verified paste and saved text all passed. Interruption during a spoken reply failed. Unsupported Calculator was silently skipped in another compound command. Actual dashboard states and dictation UI were inspected. The original Fish Audio/OpenRouter services remain untested; substitutions do not establish that those integrations work.

The clean install needed two missing build dependencies, `setuptools` and `py2app`. The real wake loop also saved unrelated speech as a WAV even though the Privacy screen says it discards speech not addressed to it. The pinned repository has no declared license. Resolve that retention discrepancy and license uncertainty before recommending it for Voice Assistants. See the [initial report](lab/evidence/hey-jev/README.md) and [adapted test notes, patch and evidence](lab/evidence/hey-jev/adapted/README.md).


### OpenDots — 2026-10-05

**Service/integration audit — 2026-10-06:** our shared voice service and OSS adaptation had defects that invalidated the earlier blame assignment. After fixing capacity recovery, playback events, durable history, compute-result handling, bounded media teardown and call receipts, the direct service passed five live scenarios; OpenDots passed nine continuous-voice checks and six fault scenarios (control loss ends the call safely, without automatic reconnect). A real process restart preserved all seven conversation messages, pages and calls exactly. Final validation: 192 application tests, 16 service tests, typecheck, lint and production build. This evaluates phone-like voice communication; physical-device qualification is outside scope. **Remains on the Watch List because this is a custom adaptation, with spoken approval/cancel still absent.** See [patch, recordings, exact coverage and limitations](lab/evidence/opendots/integration-audit/README.md).

**Historical adapted follow-up (superseded by the audit above):** tested real continuous calls using the existing hosted OSS speech stack, with OpenDots and Chromium running in a disposable Bumble VM. Recorded speech, audible interruption, voice-to-compute page creation, mute/hangup, and same-chat text follow-up passed with the disclosed local-runtime/voice patch. The original page request failed when the local model invented a space ID; a default-destination request succeeded. The adapter uses in-memory agent history, and the generated receipt inaccurately claimed an interrupted count completed. No physical phone or spoken approval/cancel pass is claimed. The final adapted suite passed 184 tests, build, typecheck and lint. **Remains on the Watch List.** See [setup, patch, audio, screenshots and limitations](lab/evidence/opendots/adapted/README.md).

The original stock/partial test follows:

**Added to the Watch List.** At commit `71efd82cd883df7b107d663bd36435a1d8a2d12a`, OpenDots implements continuous browser voice calls with configured interruption, a dashboard, and delegation to a specialist compute agent. A tap to begin a phone-browser call is useful even without a wake word. The existing hallmark rubric gives partial voice/hands-free/oversight and full visual credit from code; this is not a claim that live calling passed.

The unchanged production build ran on Apple silicon macOS with Node 26.8.2 and Chrome for Testing 154.0.8037.92. Desktop page creation/save and a 390 × 844 touch-enabled browser's persisted document view and pause/resume controls **passed**. A separate direct-agent probe using real local Ollama answered a question and invoked the page tool to save exact content in SQLite. That probe bypasses the Intelligence transport and does not establish a working browser conversation. No physical phone, iOS background audio or cellular handoff was tested.

Stock conversations and calls returned HTTP 503 for missing service configuration: **BLOCKED**, not failed. CopilotKit Intelligence is a separate dependency that local model access does not replace; stock speech additionally needs OpenAI Realtime. Spoken approval/cancel tools and automatic multi-Dot coordination are absent. Calls cap at 15 minutes and six compute requests. The upstream fixture suite passed all 182 tests with one worker after two timeouts in the initial parallel run. See the [report, source findings, screenshots and reproducible probes](lab/evidence/opendots/README.md) for exact coverage and service requirements.

## Findings

- **No agent is fully hands-free yet.** Every agent tested can hear you and talk back, but approving, denying or cancelling the agents it launched still needs a click or keypress somewhere. TapQ comes closest, with spoken approve and deny.
- **Permission defaults are the biggest risk.** Several leading agents turn off or automate approvals by default: OpenClaw runs shell commands without asking, Hermes auto-approves "low-risk" commands, Paseo's voice agent can approve its own sub-agents, and TapQ and JARVIS for Claude Code start Claude Code with permission checks skipped. Claude Code 2.1.283 itself now defaults to an "auto" mode that approves low-risk actions. Tighten these before giving an agent your machine.
- **Hermes Agent can adopt your Claude Code login.** Its `anthropic` provider reads Claude Code's saved credentials and calls Anthropic while presenting itself as Claude Code. Turn off `auth.adopt_external_logins` and use a different provider if you don't want that.
- **Omarchy runs on Apple Silicon.** [Omarchy M](https://omarchy.org/news/2026/09/introducing-omarchy-m/) installs natively on M1 and M2 Macs and ships ARM64 VM images, which is how the Omarchy tests ran.

## Local Voice Instead of Paid Keys

Many voice agents expect OpenAI's Realtime API. A free stack running locally on Apple silicon can stand in for it:

- [Hugging Face speech-to-speech](https://github.com/huggingface/speech-to-speech) as an OpenAI-compatible Realtime server, with Parakeet for speech recognition, a local model through Ollama, and Kokoro for speech. About 1.1 to 1.5 seconds from the end of your speech to the first spoken word, with barge-in and cancel.
- [mlx-audio](https://github.com/Blaizzy/mlx-audio) for OpenAI-compatible transcription and speech endpoints.

Whether an agent can use it depends on whether its OpenAI address is configurable:

| Agent | Can it point at a local server? |
|---|---|
| OpenClaw | Yes, by config (server-side relay with a custom endpoint) |
| omavoice, omarchy-voice | Not by config: the address is hardcoded. Changing one line works, and both then ran against the local server. |
| TapQ, OpenClicky | Not by config: the address is hardcoded in source |
| usejarvis | Only through its hosted-service setting; its local speech-to-text option works on its own |
| JARVIS for Claude Code, Sutando | No. They use Fish Audio and Gemini Live, not OpenAI's protocol. |

A hardcoded address is a small porting job, not a mark against an agent's voice design.

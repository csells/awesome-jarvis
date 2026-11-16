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

The table below records the September run and its explicitly dated historical follow-ups. The November assessment below supersedes corresponding current-release claims.

PASS means it worked end to end, PARTIAL means some of the pillar worked, FAIL means it didn't work, and BLOCKED means it needs a paid key or hardware the lab didn't have.

| Agent | Voice | Hands-free | Visual | Oversight | Notes |
|---|---|---|---|---|---|
| OpenClaw (Mac app) | PARTIAL | ◐ | PASS | PASS | The "computer" wake word and spoken commands work on-device. Spoken replies couldn't be captured inside the VM. Launched two sub-agents by voice, approved one and cancelled one. A spoken "allow" or "stop" is treated as chat text. |
| OpenClaw (browser Talk) | PASS | ◐ | PASS | PARTIAL | Pointed at the local voice server by config. Answers aloud and barge-in works. Approvals are buttons only. A spoken cancel was followed by OpenClaw re-sending the request. |
| Hermes Agent | PASS | ◐ | PASS | PASS | Local wake word, speech-to-text and text-to-speech. Barge-in worked in the desktop app but failed in the command-line voice mode. Delegated to Claude Code by voice and showed it live on its kanban board; interrupt worked. Its default "smart" approvals let a local model approve an `rm -rf` of a test folder with no human prompt. |
| usejarvis 0.15.0 | PARTIAL | ◐ | PARTIAL | PARTIAL | October re-test: native wake/transcription/reply and Research Analyst delegation worked, but wake-word interruption failed. Local 7B responses took 71–90 seconds and later turns reused stale tasks. Spoken approval/denial/child cancellation and all visual states are not certified in this run. [Exact coverage](lab/evidence/2026-10-06-retest/README.md). |
| JARVIS for Claude Code | PARTIAL | ◐ | PASS | PASS | Understands speech (no wake word). Speaking back needs a paid Fish Audio key (BLOCKED). Watched a live Claude Code session and cancelled a run by voice. |
| TapQ | PARTIAL | ◐ | FAIL | PARTIAL | The "hey tapq" wake word and spoken approval prompts work on-device, and a Claude Code action was approved and denied by voice. Conversation needs an OpenAI key (BLOCKED). No UI by design. |
| hey-jarvis | PASS | ◐ | PASS | PASS | On real Omarchy and Hyprland, answered through Claude and spoke the reply, with every conversation phase shown. The consent window opens without keyboard focus and is covered by the conversation window, so approving a command needs a click, and an unattended request turns into a denial after 45 seconds. |
| Paseo 0.10.3 | PASS | ◐ | PASS | PARTIAL | October re-test: real browser speech round trip, barge-in and a Codex child writing verified content passed. Default Codex permissions repeatedly asked for a click to allow speech; spoken approval failed. A separate stop test interrupted the Codex agent but left its subprocess running. [Exact coverage](lab/evidence/2026-10-06-retest/README.md). |
| Happy | BLOCKED | ◐ | PASS | PASS | From a phone, monitored two Claude Code sessions, approved an edit and a command, and cancelled a run. Free voice (20 minutes a month) was confirmed but couldn't be exercised without an emulator microphone. |
| Operit | BLOCKED | ◐ | PASS | FAIL | Ran on a local model as Android's default assistant with its floating avatar. The small local model never made the sub-agent tool call. Its default wake phrase is "O", matched anywhere in a transcript. |
| omavoice | PASS | ◐ | PASS | BLOCKED | Tested with a one-line URL change against the local voice server. Answered aloud with barge-in and a live trace of each step. Delegation wasn't completed because the lab's Claude login had expired in that VM. |
| omarchy-voice | PARTIAL | ◐ | PARTIAL | FAIL | Tested with a one-line URL change. Answered a desktop question aloud. The local 7B model read tool calls aloud instead of making them, which is a limit of the model, not the app. |

Not run hands-on in the September campaign (later November checks are documented below): Qwen Audio Agent, Sutando and OpenClicky, which need paid voice keys; N.E.K.O, AIRI and Newelle. The commercial assistants were scored from vendor documentation.

## Candidate Follow-ups

### Release re-tests and OpenVision review — 2026-10-06

Paseo 0.10.3 and usejarvis brain 0.15.0 were tested in disposable home-lab VMs using the existing shared model/voice services. No new paid API keys were needed. **These are scoped results, not a blanket full-test pass.** Paseo retains full voice but drops to partial oversight after its Codex stop test left a subprocess running; it moves from Mission Control to Jarvis Agents on its voice/visual scores. usejarvis drops to partial voice because the normal wake-word path did not interrupt playback. Full visual/oversight scores retained in the scorecard still include the earlier source and September lab evidence; untested current-release paths are identified in the [release report](lab/evidence/2026-10-06-retest/README.md).

**OpenVision stays on the Watch List.** Two independent reviews found full voice and conditional Hermes Dashboard hands-free controls, but partial visual/agent oversight. The pinned source built successfully after correcting the VM toolchain setup, then crashed on startup with example Meta configuration. Runtime voice, glasses and remote approvals remain blocked; a working phone-only startup was not established. See the same report for the exact commit, startup error and caveats.

The September usejarvis 0.14.0 results covered delegation and sub-agent orbs. The September Paseo 0.9.2 run used Claude Code, including its then-observed skip-permissions behavior and voice-agent approval of child requests. Those observations do not establish how the current Codex configuration handles permissions.

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
- [mlx-audio](https://github.com/Neywa-Labs/mlx-audio) for OpenAI-compatible transcription and speech endpoints.

Whether an agent can use it depends on whether its OpenAI address is configurable:

| Agent | Can it point at a local server? |
|---|---|
| OpenClaw | Yes, by config (server-side relay with a custom endpoint) |
| omavoice, omarchy-voice | Not by config: the address is hardcoded. Changing one line works, and both then ran against the local server. |
| TapQ, OpenClicky | Not by config: the address is hardcoded in source |
| usejarvis | Local STT supports an OpenAI-compatible endpoint; an authenticated service needs a proxy because the client omits its Authorization header. Generic compatible TTS is not a stock option; this re-test used Edge TTS. |
| JARVIS for Claude Code, Sutando | No. They use Fish Audio and Gemini Live, not OpenAI's protocol. |

A hardcoded address is a small porting job, not a mark against an agent's voice design.


## November13 lab continuation — partial

Continued the November re-verification in disposable Linux/macOS guests using the authorized permanent Pocket and Mac Ollama services plus the authorized Codex login copy. New results include packaged OpenJarvis desktop client chat, native AIRI chat and analytics preference persistence, OpenClaw authenticated Codex chat, and Sutando native menu-bar build/launch. Foreground worker cancellation failed in Paseo with subscription Codex and in Dodaios; the recorded workers were terminated after verification. Newelle's corrected computer wake phrase produced two independently transcribed spoken replies; its spoken-stop behavior remained delayed. Paseo transcribed microphone input but reported its speak tool unavailable, so non-silent interface audio is not counted as a spoken reply or barge-in pass. Dodaios's tested speech adapters were incompatible with Pocket. These are scoped observations, not updated full-release scores. See [versions, evidence, adaptations and limits](lab/evidence/reverification-2026-11-12/README.md) and the [remaining test matrix](specs/plans/0001-november-reverification.md). Phone tests remain separate. DotDial guest ChatGPT sign-in completed November15; native identity and microphone permission verified, but real call attempts failed with HTTP404 during profile lookup before audio connection. See the dated submission evidence; dependent voice/control tests remain blocked.

On November15, Sutando0.13.0's explicitly authorized native Codex core completed real file work and recovered through the menu's restart control. Stop Core CLI stopped the core but left its executing worker writing heartbeats; the harness then terminated that worker. The copied guest Codex credentials were removed afterward. OpenJarvis's actual Bash installer, running backend and official desktop1.0.5 were tested for consent, saved opt-out and native restart behavior with real Mac Ollama replies. Analytics delivery was blocked in the guest throughout; the tests observe attempted connections, not external payloads. See the [case results, setup qualifications and dependency-audit limits](lab/evidence/reverification-2026-11-12/nov15/README.md). No full E2E certification or submission acceptance is implied.

On November16 UTC, Newelle1.6.1's native Run/Skip controls enforced independently checked file effects. Voice Mode cancellation left the real foreground worker running; new manually approved work afterward succeeded. The current official AIRI0.15.4 native build passed local-model chat, saved analytics-off after process restart, and Hearing recognition through Pocket. Both its speech preview and main runtime received Pocket audio but produced silent speaker captures; an independent speaker-route control passed. OpenJarvis desktop1.0.5 also completed its own Linux backend dependency installation/start and visibly answered “Four,” after resolving the guest's Rust and configuration-path prerequisites. See [exact cases, observer qualifications and cleanup](lab/evidence/reverification-2026-11-12/nov16/README.md). These are scoped results; the remaining matrix and full-release score dates are unchanged by a partial result alone.

## November 16 assessment — partial qualification

The six stale releases now have reconciled decisions, using independent source reviews and real lab evidence. Current scorecard records for OpenClaw v2026.11.3, AIRI v0.15.4 and Sutando v0.13.0 carry **Partial** coverage and the assessment date/version. Their full voice scores retain source or earlier provider evidence where current native/paid-provider tests remain blocked or partial; they are not November native voice passes. OpenClaw and Sutando oversight drop to partial.

Newelle1.6.1 moves to Voice Assistants: real manual approvals passed, but native Stop left both direct and managed-subagent workers alive. Paseo0.15.4 and usejarvis0.17.6 move to the Watch List, with their voice/setup and oversight limits preserved. OpenJarvis moves from Mission Control to Agent Frameworks after real Pause failed to stop work. Dodaios and OpenVision remain on the Watch List; Jarvis Vocal's author aliases do not justify promotion.

Paseo's corrected native MCP/turn-detector setup produced an independently transcribed spoken answer in original Auto-review mode without a click. Default permissions required speech approval clicks; current interruption/new answer remained partial. OpenJarvis's packaged desktop also spoke an independently transcribed factual answer with the disclosed one-line TTS URL change; native microphone access remained denied despite a passed independent route control. DotDial's authenticated404 was traced to profile versus conversation-ID handling; a supported configuration workaround connected, but its recorded reply had no speech transcript.

| Current release/configuration | Voice | Hands-free | Visual | Oversight |
|---|---|---|---|---|
| OpenClaw v2026.11.3 | PARTIAL native; full retained from source/prior browser | PARTIAL | PASS UI | PARTIAL; exec safely refused approval binding |
| AIRI v0.15.4 | PARTIAL; Hearing passed, tested Pocket output failed | PARTIAL source | PASS native state/chat | PARTIAL source; no native task pass |
| Sutando v0.13.0 | BLOCKED live: Gemini key | PARTIAL source | PASS native UI | PARTIAL; real core task passed, worker stop failed |
| Newelle1.6.1 | PARTIAL; repeated wake/reply passed, interruption limited | PARTIAL; pending card not resolved by voice | PASS native state/subagent UI | PARTIAL; nested approval worked, worker stop failed |
| Paseo0.15.4/Codex | PARTIAL; original-mode speech passed, barge-in exchange unqualified | PARTIAL; mode-specific speech cards | PASS actual workspace | PARTIAL; file approval effects passed, actual stop failed |
| usejarvis0.17.6/sidecar0.12.1 | BLOCKED current adapter setup; earlier voice partial | PARTIAL source | PARTIAL native onboarding; browser chat passed | PARTIAL source; current runtime not certified |
| OpenJarvis13706f2/desktop1.0.5 | PARTIAL; CLI and native output passed with URL change, native input denied | No wake/full spoken loop established | PASS actual chat/dashboard | PARTIAL; approval effects passed, Pause worker stop failed |

See [decisions, source disagreements, safety/license audit and remaining gaps](lab/evidence/reverification-2026-11-12/assessment.md), [November16 case evidence](lab/evidence/reverification-2026-11-12/nov16/README.md), and [DotDial's sanitized diagnosis](lab/evidence/submissions-2026-11-12/dotdial-nov16-diagnosis.json). PR#3 ibara and PR#4 /call-me remain unaccepted evaluation requests. Supported paired-desktop, ready-phone, physical-device, Windows and enumerated permission/recovery coverage remain visible in the [original test matrix](specs/plans/0001-november-reverification.md); complete cross-repository E2E is still not claimed.

The November 16 no-Tailscale follow-up completed ibara's independent MCP/local-daemon component checks; 573 upstream fixture tests passed across corrective reruns, with 2 platform-assumption failures left unqualified. OpenVision built for the iPad simulator and unsigned iOS devices, but simulator launches and the upstream test host still hit the Meta SDK initialization crash. Physical iPad/voice/glasses coverage is not inferred. See the [component and iPad evidence](lab/evidence/reverification-2026-11-12/nov16/README.md).


## November 16 release follow-up

Qwen Audio Agent 2.1.0 now has two independent source reviews, a verified Linux source build and bounded native testing. Stock WebUI voice through the permanent local Realtime/Pocket service passed France/Paris and acoustic interruption/new answer. Native manual backend approvals enforced deny/approve file effects; a separate task required fresh permission. Native task cancellation nevertheless left the real Codex worker alive while the API reported cancelled. Scores are 2/1/2/1 with Partial coverage; spoken backend approval/cancel and other providers/platforms remain unqualified. An initial silent audio run was discarded after finding Playwright's mute flag, then repeated successfully.

Paseo 0.16.0 fixes the tested native current-turn Codex Stop failure: the actual worker stopped, older intentional background work survived stopping another turn, and dedicated native background stop cleared inventory and killed that worker. The actual0.15.4 baseline failed the same still-running-turn condition. This supersedes the older cancellation finding for the tested0.16 path and supports moving Paseo to Mission Control with Partial coverage (2/1/2/2). Current 0.16 Auto-review voice and barge-in passed with supported MCP injection, permanent Pocket/Alfred and Codex apps disabled; default apps misrouted the voice reply. This does not qualify spoken task approval/cancellation; older 0.15.4 mode evidence remains historical. See [exact release cases and source reviews](lab/evidence/reverification-2026-11-12/nov16/README.md#release-follow-up).


OpenClaw 2026.11.4's native Codex path now passes real manual deny/allow-once file effects, executing-worker Stop, rejection of a stale denied approval and recovery with a new permission. This supersedes the earlier conditional oversight result for this configured path:2/1/2/2, Partial overall coverage. The separate official Codex extension, correct subscription wire adapter, auth-only import and isolated agent home were required setup. Default YOLO/full execution and automatic learned-skill persistence remain safety notes. Native Linux Tauri UI was black in the tested display; browser Control UI worked. Mac11.3 speech and untested11.4 platform/worker/child cases remain separately qualified. See [current cases](lab/evidence/reverification-2026-11-12/nov16/openclaw-114-native-cases.json).

In 0.16 Default permissions, spoken yes/no again became new chat turns and acknowledgement speech waited at a card. Manual Accept produced a verified audible reply; that click is not a hands-free pass. The current configured voice/barge-in result uses Codex apps disabled, while default-apps failure is retained.

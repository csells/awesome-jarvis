# Awesome Jarvis [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

<p align="center">
	<a href="blueprint.md"><img src="media/banner.jpg" width="784" alt="Glowing circular heads-up display with a voice waveform running through it"></a>
</p>

> Real-life J.A.R.V.I.S.: personal AI agents you talk to, that show you what they are doing, and that run a staff of other agents on your behalf.

Tony Stark never typed a prompt. He talked to Jarvis, watched the work take shape on a heads-up display, and let Jarvis run everything else in the building. This list holds projects to those three pillars:

- **Voice.** Hands-free and interruptible: a wake word or always-on listening, low latency, spoken replies.
- **Visual presence.** An orb, HUD, avatar, overlay or dashboard that shows its state and the work in progress, not just a chat transcript.
- **Oversight.** It dispatches, supervises and reports on other agents, such as sub-agents, coding agents and background workers, with approvals and a kill switch.

Every agent in the scorecard was checked against its code or vendor documentation, not its marketing, by two independent reviews. Building blocks follow for each layer. New to this? Read the [blueprint](blueprint.md) for a reference architecture and three starter builds.

## Contents

- [Jarvis Agents](#jarvis-agents)
	- [Scorecard](#scorecard)
	- [Open Source](#open-source)
	- [macOS](#macos)
	- [Linux](#linux)
	- [Android](#android)
	- [Commercial](#commercial)
- [Mission Control](#mission-control)
	- [Voice Oversight](#voice-oversight)
	- [Command Centers](#command-centers)
	- [Agent Presence](#agent-presence)
	- [Hosted Mission Control](#hosted-mission-control)
- [Watch List](#watch-list)
	- [Omarchy](#omarchy)
	- [Voice Oversight Contenders](#voice-oversight-contenders)
	- [Desktop, Mobile and Glasses](#desktop-mobile-and-glasses)
- [Voice Assistants](#voice-assistants)
- [AI Devices](#ai-devices)
- [Ears](#ears)
	- [Wake Word](#wake-word)
	- [Voice Activity and Turn Detection](#voice-activity-and-turn-detection)
	- [Speech-to-Text](#speech-to-text)
- [Voice](#voice)
	- [Text-to-Speech](#text-to-speech)
	- [Speech-to-Speech Models](#speech-to-speech-models)
	- [Voice Agent Frameworks](#voice-agent-frameworks)
- [Brain](#brain)
	- [Local Model Runtimes](#local-model-runtimes)
	- [Open-Weight Models](#open-weight-models)
	- [Agent Frameworks](#agent-frameworks)
	- [Memory](#memory)
	- [Tools and Protocols](#tools-and-protocols)
	- [Computer and Browser Use](#computer-and-browser-use)
	- [Proactivity](#proactivity)
- [Interfaces](#interfaces)
- [Home](#home)
	- [Smart Home Control](#smart-home-control)
	- [Vision and Presence](#vision-and-presence)
	- [Voice Hardware](#voice-hardware)
- [Wearables](#wearables)
- [Robots](#robots)
- [Research](#research)
	- [Agent Foundations](#agent-foundations)
	- [Orchestration and Oversight](#orchestration-and-oversight)
	- [Memory Research](#memory-research)
	- [Spoken Dialogue](#spoken-dialogue)
	- [Personal and Proactive Assistants](#personal-and-proactive-assistants)
	- [Computer-Use Agents](#computer-use-agents)
- [Benchmarks](#benchmarks)
- [Guides](#guides)
- [Videos](#videos)
- [Inspiration](#inspiration)
- [Communities](#communities)

## Jarvis Agents

Complete assistants that are strong on at least two of the three pillars, including voice or oversight.

### Scorecard

● shipped and working, ◐ partial, limited or experimental, ○ absent. Open-source rows were scored from code by two independent reviews in September 2026, the second blind to the first. Commercial rows were scored from vendor documentation. Several agents run coding agents with permission checks turned off by default, so read the last column before you install.

| Agent                  | Platform                    | Voice | Visual | Oversight | Watch out                                  |
| ---------------------- | --------------------------- | :---: | :----: | :-------: | ------------------------------------------ |
| OpenClaw               | macOS, iOS, Android, server |   ●   |   ●    |     ●     | Yolo mode is opt-in                        |
| Hermes Agent           | Linux, macOS, Windows       |   ●   |   ●    |     ●     | None found                                 |
| Qwen Audio Agent       | macOS, Windows, Linux       |   ●   |   ●    |     ●     | Cloud voice by default, Mandarin wake word |
| usejarvis              | Daemon plus desktop sidecar |   ●   |   ●    |     ●     | Source-available, telemetry on (opt-out)   |
| JARVIS for Claude Code | macOS                       |   ●   |   ●    |     ●     | Skips permissions, non-commercial          |
| Sutando                | macOS                       |   ●   |   ●    |     ●     | Skips permissions, telemetry on (opt-out)  |
| OpenClicky             | macOS                       |   ●   |   ●    |     ●     | Codex full access, prebuilt binaries       |
| N.E.K.O                | Windows, macOS, Linux       |   ●   |   ●    |     ●     | Free tier uses the project's server        |
| AIRI                   | Web, Windows, macOS, Linux  |   ●   |   ●    |     ◐     | Analytics on (opt-out)                     |
| Operit                 | Android                     |   ●   |   ●    |     ◐     | Bundled APKs, root or Shizuku              |
| Newelle                | Linux                       |   ●   |   ●    |     ◐     | Flatpak can run host commands              |
| Paseo                  | Desktop, mobile, web        |   ●   |   ●    |     ●     | Voice control of agents is opt-in          |
| Happy                  | iOS, Android, web, macOS    |   ●   |   ●    |     ●     | Paid voice, analytics on (opt-out)         |
| TapQ                   | macOS, AirPods              |   ●   |   ○    |     ●     | Beta, its sessions skip permissions        |
| ChatGPT and Codex      | Desktop, mobile, web        |   ●   |   ●    |     ●     | Approvals on screen only                   |
| Claude                 | Desktop, mobile, web        |   ●   |   ◐    |     ●     | Voice mode is beta                         |
| Gemini                 | Mobile, Mac, web            |   ●   |   ◐    |     ●     | Spark needs Pro or Ultra                   |
| Perplexity Comet       | Desktop, Android            |   ●   |   ◐    |     ●     | Parallel tasks need Max                    |
| Microsoft Copilot      | Windows                     |   ●   |   ●    |     ◐     | Actions are experimental                   |

### Open Source

- [OpenClaw](https://github.com/openclaw/openclaw) - Self-hosted agent gateway with native macOS, iOS and Android apps that add a wake word, an interruptible talk mode with an orb overlay, a Canvas window and a web control UI, plus sub-agents and ACP coding agents behind exec approvals.
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) - Nous Research's assistant with a local "Hey Hermes" wake word, full-duplex voice with barge-in, a desktop app with an always-on-top pet overlay and live sub-agent panel, and parallel delegation with interrupt and command approvals.
- [Qwen Audio Agent](https://github.com/QwenAudio/qwen-audio-agent) - Full-duplex voice front end with a desktop orb and task cards that hands work to Claude Code, Codex, OpenCode and other ACP agents, tracks and cancels them while you talk, and relays their permission prompts (cloud voice by default, local option).
- [usejarvis](https://github.com/vierisid/jarvis) - Daemon with a "Hey Jarvis" wake word, interruptible speech, a cursor-following status orb with a sub-orb for each background agent, and delegated sub-agents with approvals and kill controls (source-available license).
- [N.E.K.O](https://github.com/Project-N-E-K-O/N.E.K.O) - Desktop companion with full-duplex voice and barge-in, Live2D, VRM or MMD avatars, and an agent HUD that dispatches and cancels computer-use, browser and OpenClaw tasks.
- [AIRI](https://github.com/moeru-ai/airi) - Self-hosted Live2D and VRM companion for web, desktop and mobile with always-on voice, sub-agents such as its Minecraft player, and an approval-gated computer-use service.

### macOS

- [JARVIS for Claude Code](https://github.com/ethanplusai/jarvis) - Voice butler with always-on listening, barge-in and an audio-reactive orb that spawns, watches and cancels Claude Code runs and announces any blocked session (runs skip permission checks, non-commercial license).
- [Sutando](https://github.com/sonichi/sutando) - Gemini Live voice agent for the browser, phone and meetings that queues work to a Claude Code or Codex core, with cancel and status by voice, a menu-bar avatar and a dashboard (alpha; the core skips permission checks).
- [OpenClicky](https://github.com/jasonkneen/openclicky) - Menu-bar buddy with a "Hey Clicky" wake word, a cursor-pointing overlay and a HUD that runs and stops several Codex agents (build from source; Codex runs with full access by default).

### Linux

- [Newelle](https://github.com/qwersyk/Newelle) - GNOME assistant with a wake word, hands-free voice shown in a desktop overlay pill, MCP tools, in-chat sub-agents and ask-by-default command permissions.

### Android

- [Operit](https://github.com/AAswordman/Operit) - Android agent that can replace the default assistant, with a custom wake word, hands-free voice, floating avatar overlays, an on-device Ubuntu terminal, a UI-automation sub-agent and ask-by-default tool permissions.

### Commercial

Status as of September 2026, from vendor documentation.

- [ChatGPT](https://learn.chatgpt.com/docs/features/voice) - Full-duplex GPT-Live voice that, in the desktop app, starts, checks and steers several Codex and Work tasks, with scheduled tasks, memory, a watchable browser agent and a floating status overlay.
- [Claude](https://claude.com/docs/cowork/guide/dispatch) - Hands-free voice mode (beta), Cowork scheduled tasks, and Dispatch, which fans work out to parallel sessions with per-task status and forwarded approvals on desktop or phone.
- [Gemini](https://gemini.google/overview/agent/spark/) - Interruptible Gemini Live voice with camera and screen sharing, plus Gemini Spark, a 24/7 cloud agent with schedules, a progress panel, stop and take-over controls, and approval before major actions.
- [Perplexity Comet](https://www.perplexity.ai/comet) - AI browser whose realtime voice mode sees the page and acts by voice, plus background assistants that run many agent tasks in parallel with confirmations in one place.
- [Microsoft Copilot](https://support.microsoft.com/en-us/topic/getting-started-with-copilot-on-windows-1159c61f-86c3-4755-bf83-7fbff7e0982d) - "Hey Copilot" wake word, Copilot Vision screen sharing, the animated Mico avatar in voice mode, and experimental Copilot Actions in an isolated agent workspace.

## Mission Control

Jarvis's staff. Tools for dispatching, watching and approving many agents at once.

### Voice Oversight

- [Paseo](https://github.com/getpaseo/paseo) - Daemon plus desktop, mobile and web clients that run Claude Code, Codex, Copilot and OpenCode agents in parallel, with an interruptible local voice mode that can create, prompt, approve and kill agents once tool injection is turned on.
- [Happy](https://github.com/slopus/happy) - Mobile, web and macOS client for supervising many Claude Code and Codex sessions, whose realtime voice assistant messages any session and approves or denies permissions (hosted voice is paid after 20 free minutes a month).
- [TapQ](https://github.com/spaceamoeba-t/tapq) - Screenless macOS supervisor that speaks Claude Code, Codex, Cursor and OpenCode prompts into your AirPods and takes answers by voice or head gesture, with a "hey tapq" wake word (beta).

### Command Centers

- [Herdr](https://github.com/herdrdev/herdr) - Terminal runtime for coding agents that marks every pane working, blocked or idle across machines and lets agents and voice front ends spawn, prompt and wait on each other through a socket API, with a [plugin marketplace](https://herdr.dev/plugins).
- [Orca](https://github.com/stablyai/orca) - Desktop workspace for fleets of parallel coding agents, with a mobile companion that pushes notifications and lets you reply or dictate to waiting agents.
- [Maestro](https://github.com/RunMaestro/Maestro) - Desktop command center for many Claude Code, Codex and OpenCode agents with unattended playbooks, a moderator-led group chat, spoken completion alerts and phone remote control.
- [Agent Orchestrator](https://github.com/Untrivial-ai/agent-orchestrator) - Orchestrator agent that splits plans into tasks and supervises a team of coding-agent workers on a live kanban, from desktop, web or phone.
- [AionUi](https://github.com/iOfficeAI/AionUi) - Desktop app that teams up Claude Code, Codex, OpenClaw, Hermes and other CLI agents under a leader agent, with per-agent approval prompts and speech input.
- [QwenPaw](https://github.com/agentscope-ai/QwenPaw) - AgentScope's assistant server with a desktop-style web console that spawns sub-agents and delegates to Claude Code, Codex and OpenCode over ACP with cancel and approvals (voice is dictation and phone calls; telemetry on, opt-out).
- [ZeroClaw](https://github.com/zeroclaw-labs/zeroclaw) - Single-binary Rust agent with a web dashboard (live canvas, runs, ACP console, approvals) and background delegation with cancel, plus Claude Code and Codex tools.
- [Moltis](https://github.com/moltis-org/moltis) - Rust agent server with a web UI, hands-free voice mode, nested sub-agents with cancel, and approval-gated control of Claude Code, Codex and ACP agents.
- [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) - Local-first framework from Stanford with a desktop GUI for running, pausing and approving persistent agents, including Claude Code (analytics on by default; installer telemetry cannot be disabled).
- [Paperclip](https://github.com/paperclipai/paperclip) - Self-hosted dashboard that runs agents from any runtime as an org chart with heartbeats, budgets, approval gates and cost tracking.
- [Mission Control](https://github.com/builderz-labs/mission-control) - Self-hosted control plane that dispatches tasks to OpenClaw, Claude Code and Codex, gates them with approvals and tracks their spend.
- [Langfuse](https://github.com/langfuse/langfuse) - Self-hostable tracing and evaluation that shows what each agent and sub-agent did and what it cost.

### Agent Presence

Ambient ways to see what your agents are doing without reading logs.

- [Pixel Agents](https://github.com/pixel-agents-hq/pixel-agents) - Shows each Claude Code agent, sub-agent and teammate as a pixel-art office worker that animates while it works and flags you when it needs permission.
- [Clawd on Desk](https://github.com/rullerzhou-afk/clawd-on-desk) - Desktop pet for Windows, macOS and Linux that shows what Claude Code, Codex and other coding agents are doing and pops up permission bubbles you can approve.
- [Claude HUD](https://github.com/jarrodwatts/claude-hud) - Always-visible status line showing context use, active tools, running sub-agents and todo progress in Claude Code.
- [Vibe Notch](https://github.com/farouqaldori/vibe-notch) - macOS notch overlay that tracks several Claude Code sessions and lets you approve or deny their tool calls.
- [peon-ping](https://github.com/PeonPing/peon-ping) - Game voice lines and on-screen banners that tell you when any of about 20 coding agents finishes or needs permission, with mobile notifications.

### Hosted Mission Control

- [Codex](https://openai.com/codex) - OpenAI's coding agent in the ChatGPT desktop app, running parallel tasks in worktrees or the cloud that ChatGPT's voice can start and steer, with phone control of a connected computer.
- [Claude Code Remote Control](https://code.claude.com/docs/en/remote-control) - Server mode that runs up to 32 Claude Code sessions, each in its own worktree, driven from the Claude app or web with push notifications for permission prompts.
- [GitHub Agent HQ](https://github.blog/news-insights/company-news/welcome-home-agents/) - Mission control for assigning, steering and stopping parallel Copilot, Claude and Codex coding agents across web, VS Code, mobile and CLI.
- [Google Antigravity](https://antigravity.google/blog/introducing-google-antigravity) - Agent-first IDE whose Agent Manager spawns and watches parallel agents that produce reviewable plans, screenshots and browser recordings.

## Watch List

Real Jarvis ideas in working code that are too young, too thin or too risky to vouch for yet. Check activity and read the code before you depend on one. Entries graduate or drop out as they mature. No open-source Windows-native agent meets the bar yet; the cross-platform entries above cover Windows.

### Omarchy

Omarchy 4 made the whole desktop a plugin surface, and its [plugin marketplace](https://plugins.omarchy.org) grew a Jarvis scene within weeks. Install with `omarchy plugin add <repo>`. Omarchy runs on x86_64 PCs and, through [Omarchy M](https://omarchy.org/news/2026/09/introducing-omarchy-m/), on Apple Silicon Macs.

- [hey-jarvis](https://github.com/Atzingen/hey-jarvis) - Local "hey jarvis" wake word, Whisper, Piper and barge-in, with a live conversation window, handing requests to Codex or Claude Code behind per-command consent windows.
- [omarchy-voice](https://github.com/wombatoperator/omarchy-voice) - Experimental OpenAI Realtime voice control with a state orb and durable background workers, including Codex, that you can list, cancel and resume by voice.
- [omavoice](https://github.com/baranskyi/omavoice) - OpenAI Realtime voice panel that delegates questions to Codex or Claude Code, with a live trace of the agent's work and cancel control.
- [Omarvis](https://github.com/eliasstravik/omarvis) - ElevenLabs voice sessions that run allowlisted desktop and browser commands and steer Herdr coding agents, with spoken confirmation for risky actions.
- [Jarvis for Omarchy](https://github.com/jburchel/omarchy-jarvis) - Voice layer for terminal coding agents with a "Hey Jarvis" wake word, Edge or Piper speech and a Claude Code adapter that reads out turn summaries and approval requests.
- [Infomarchy](https://github.com/nixfred/infomarchy) - Turns the wallpaper into a live dashboard of every running coding agent, with busy and stale states, stop controls and usage limits.

### Voice Oversight Contenders

- [herdr-voice](https://github.com/brogrammerMW/herdr-voice) - macOS voice agent with an orb that starts, prompts and watches the coding agents in your Herdr panes and approves their prompts on your spoken yes.
- [OpenLive](https://github.com/katipally/openlive) - On-device voice loop with barge-in in front of one ACP coding agent per call, speaking its permission requests for yes or no answers and showing its live plan.
- [Bosun](https://github.com/virtengine/bosun) - Control plane with an orb-style realtime voice assistant that starts and polls coding-agent sessions (executors skip permission checks by default; activity paused for months).
- [OpenYabby](https://github.com/OpenYabby/OpenYabby) - macOS orchestrator with a "Yabby" wake word and realtime voice that plans work and spawns teams of Claude Code or Codex agents with plan approval and kill controls.
- [Nerve](https://github.com/daggerhashimoto/openclaw-nerve) - Web cockpit for OpenClaw with wake-phrase voice, a sub-agent session tree and a kanban board for delegating and reviewing work.

### Desktop, Mobile and Glasses

- [Personal Jarvis](https://github.com/PersonalJarvis/PersonalJarvis) - Wake-word voice orchestrator with an orb and mission deck that runs Claude Code and Codex missions in worktrees (one developer's largely AI-generated code, failing CI, workers skip permission checks).
- [Jarvis × Codex](https://github.com/Big-Guan/jarvis-codex) - macOS "Hey Jarvis" voice front end for Codex with an animated character that reflects task state and a stop-all button.
- [Jarvis Vocal](https://github.com/sosoj92/jarvis-assistant-vocal) - French-language Windows assistant with a "Hey Jarvis" wake word, an arc-reactor HUD and research delegated to a local Hermes agent (launcher auto-updates from Git).
- [WakeHermesClaw](https://github.com/yuga-hashimoto/openclaw-assistant) - Android and Wear OS voice client for OpenClaw and Hermes Agent with a wake word and default-assistant integration.
- [VisionClaw](https://github.com/Intent-Lab/VisionClaw) - Meta Ray-Ban glasses app with interruptible Gemini Live or OpenAI Realtime voice and vision that delegates tasks to OpenClaw or a hosted agent (no open-source license; uploads transcripts to its gateway).
- [OpenVision](https://github.com/rayl15/OpenVision) - iOS app for Meta Ray-Ban glasses with an "Ok Vision" wake word and on-device or cloud backends, including OpenClaw.
- [cc-g2](https://github.com/wmoto-ai/cc-g2) - Even Realities G2 companion that shows coding-agent completions on the HUD and lets you approve their permission prompts.
- [Meta Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) - Meta's personal agent in a cloud VM you can watch and take over, with a separate agent that gates its actions; voice mode and glasses support are announced, not shipped.

## Voice Assistants

Strong on voice, light on visuals and oversight. Good ears and a mouth for a Jarvis, or a Jarvis in its own right if you don't need a staff.

- [Home Assistant Assist](https://www.home-assistant.io/voice_control/) - Home Assistant's voice pipeline (wake word, speech-to-text, conversation agent, text-to-speech) with satellites in every room, fully local or LLM-backed, that can start conversations on its own.
- [isair/jarvis](https://github.com/isair/jarvis) - Local always-listening assistant that hears "Jarvis" anywhere in a sentence, with an animated state face, memory and MCP tools (non-commercial license).
- [GLaDOS](https://github.com/dnhkng/GLaDOS) - Always-listening, interruptible local voice persona with vision, autonomous background minds and a terminal dashboard.
- [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) - ESP32 voice firmware for 130+ boards with offline wake word, streaming or realtime LLM speech (full duplex on boards with echo cancellation), speaker recognition, an expressive emoji display and MCP, using the vendor's cloud by default.
- [OpenVoiceOS](https://github.com/OpenVoiceOS/ovos-core) - Community continuation of Mycroft with skills, an LLM persona fallback, and Raspberry Pi and Docker images.
- [Neon AI](https://github.com/NeonGeckoCom/NeonCore) - Mycroft-derived, Linux-only voice assistant core with multi-user support, an LLM fallback skill and containerized speech services.
- [Dicio](https://github.com/DicioTeam/dicio-android) - Free, offline Android voice assistant with Vosk recognition, an openWakeWord wake word and a fixed set of on-device skills.
- [Siri](https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/) - Apple's rebuilt Siri, an opt-in English beta across the version 27 platforms with personal context, on-screen awareness and cross-app actions.
- [Alexa+](https://www.aboutamazon.com/news/devices/alexa-plus-available-free-prime-members-us) - Amazon's generative Alexa in the US and Canada that builds smart-home routines by voice and books services for you.
- [Grok in Tesla](https://www.tesla.com/support/grok) - "Hey Grok" voice assistant (beta) with vehicle commands in supported Teslas.

## AI Devices

Dedicated hardware for talking to an assistant. Status as of September 2026.

- [Meta Ray-Ban Display](https://www.meta.com/ai-glasses/meta-ray-ban-display/) - Glasses with a monocular in-lens display, an EMG wristband for gestures and handwriting, and hands-free "Hey Meta" voice with navigation and live captions.
- [Ray-Ban Meta](https://www.meta.com/ai-glasses/) - Voice-first camera glasses without a display, joined by camera-free audio glasses, for hands-free access to Meta's assistant.
- [Muse Charm](https://www.meta.com/blog/meta-connect-2026-everything-we-announced/) - Pocket Meta device for talking to the Muse agent with a realtime voice model (announced at Connect 2026, not yet shipping).
- [Brilliant Labs Halo](https://brilliant.xyz/products/halo) - Open-source glasses with a color display, bone-conduction audio and Noa, a conversational assistant that remembers what you see and hear.
- [Omi](https://github.com/BasedHardware/omi) - Open-source pendant and desktop app that captures what you hear and see, transcribes it live, turns it into memories and action items, and answers by voice through your phone or earbuds.
- [Rabbit r1](https://www.rabbit.tech/updates) - Push-to-talk pocket device that fronts rabbit OS3, a cloud agent with persistent memory and bring-your-own model keys that operates up to five connected computers and confirms sensitive actions.
- [Google Home Speaker](https://blog.google/products-and-platforms/devices/google-nest/google-home-speaker-gemini-features/) - Gemini for Home speaker with a wake word, multi-command requests, continued conversation and a state-showing light ring.

## Ears

### Wake Word

- [openWakeWord](https://github.com/dscripka/openWakeWord) - Offline wake word framework that runs on a CPU or Raspberry Pi, trains custom words from synthetic speech, and powers Home Assistant's wake word add-on.
- [microWakeWord](https://github.com/OHF-Voice/micro-wake-word) - Trains tiny streaming wake word models for ESP32-S3 microcontrollers, running on-device in ESPHome and the Home Assistant Voice Preview Edition.
- [LiveKit WakeWord](https://github.com/livekit/livekit-wakeword) - Wake word trainer built on openWakeWord's front end with a conv-attention classifier, openWakeWord-compatible models and synthetic training data in 30 languages.
- [Porcupine](https://github.com/Picovoice/porcupine) - Commercial on-device wake word engine with SDKs for microcontrollers, mobile, web and desktop, and a free tier.

### Voice Activity and Turn Detection

Voice activity detection hears that someone is talking. Turn detection decides whether they are done, which is what makes a conversation feel natural.

- [Silero VAD](https://github.com/snakers4/silero-vad) - De facto open voice activity detector, a 2 MB model that processes a 30 ms chunk in under 1 ms on one CPU thread.
- [TEN VAD](https://github.com/TEN-framework/ten-vad) - Low-latency frame-level voice activity detector that catches speech-to-silence transitions faster than Silero, with C, Python, WebAssembly and mobile builds.
- [Smart Turn](https://github.com/pipecat-ai/smart-turn) - Audio-native turn detection model that uses prosody as well as silence, in an 8 MB CPU build covering 23 languages.
- [LiveKit Turn Detector](https://huggingface.co/livekit/turn-detector) - Semantic end-of-turn model that reads the transcript to decide whether the user is finished, running on CPU in 14 languages (licensed for use with LiveKit Agents only).

### Speech-to-Text

- [whisper.cpp](https://github.com/ggml-org/whisper.cpp) - Dependency-free C/C++ port of Whisper with Metal, CUDA, Vulkan and Core ML acceleration, running well on Apple silicon, Raspberry Pi and phones.
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) - CTranslate2 reimplementation of Whisper that is up to 4x faster with less memory, the backbone of most self-hosted Whisper servers.
- [Parakeet TDT](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) - NVIDIA's 600M-parameter model for 25 European languages with very high throughput, one of the best choices for fast local transcription.
- [Nemotron ASR Streaming](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b) - NVIDIA's 600M cache-aware streaming model for 40 language-locales, with chunk sizes down to 80 ms for voice agents.
- [Moonshine](https://github.com/moonshine-ai/moonshine) - On-device streaming speech recognition for Python, WebAssembly, iOS, Android and Raspberry Pi, built to transcribe while the user is still speaking.
- [Voxtral Realtime](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602) - Mistral's Apache-2.0 4B natively streaming model in 13 languages, with a configurable delay (480 ms recommended) that matches offline accuracy.
- [Kyutai STT](https://github.com/kyutai-labs/delayed-streams-modeling) - Streaming speech-to-text and text-to-speech models with semantic voice activity detection and batched Rust serving.
- [Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR) - Open 0.6B and 1.7B streaming recognition models for 52 languages and dialects, with language identification and a companion forced aligner for timestamps.
- [FunASR](https://github.com/modelscope/FunASR) - Speech toolkit with streaming recognition, voice activity detection, punctuation and diarization, strongest for Chinese and other Asian languages.
- [VibeVoice](https://github.com/microsoft/VibeVoice) - Microsoft's open speech family, with one-pass transcription of an hour of multi-speaker audio, a streaming variant that labels speakers live, a CPU-only BitNet build and a small realtime text-to-speech model.
- [pyannote.audio](https://github.com/pyannote/pyannote-audio) - Leading open speaker diarization toolkit, for knowing which household member is talking.
- [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) - Offline speech recognition, synthesis, voice activity detection and keyword spotting on ONNX Runtime, from RISC-V boards to servers.
- [Speech-to-Phrase](https://github.com/OHF-Voice/speech-to-phrase) - Fast local recognition for Home Assistant that is trained on your own device and area names, so it matches home commands instead of transcribing open speech.
- [FluidAudio](https://github.com/FluidInference/FluidAudio) - Swift and Core ML SDK that runs streaming Parakeet with end-of-utterance detection, Kokoro and Pocket TTS, Silero VAD, live diarization and echo cancellation on the Apple Neural Engine.
- [Deepgram Flux](https://deepgram.com/flux) - Cloud conversational speech recognition with built-in end-of-turn detection for voice agents.
- [AssemblyAI Universal-Streaming](https://www.assemblyai.com/universal-streaming) - Cloud streaming recognition for voice agents with neural end-of-turn detection.
- [ElevenLabs Scribe](https://elevenlabs.io/speech-to-text) - Low-latency cloud streaming recognition in 90+ languages.

## Voice

### Text-to-Speech

For a butler-style voice, prefer voice design from a text description, which VoxCPM, Qwen3-TTS and OmniVoice support. It avoids cloning a real person. Only clone voices you have the rights to.

- [Piper](https://github.com/OHF-Voice/piper1-gpl) - Fast local neural voices that run in real time on a Raspberry Pi, in dozens of languages including British English, maintained by the Open Home Foundation.
- [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) - 82M-parameter Apache-2.0 model that is the most widely deployed small local voice, fast on CPU, with US and UK English voices.
- [Pocket TTS](https://github.com/kyutai-labs/pocket-tts) - Kyutai's 100M-parameter streaming model that runs in real time on a CPU after a `pip install`, with voice cloning.
- [KittenTTS](https://github.com/KittenML/KittenTTS) - Tiny ONNX models (15M to 80M parameters) for CPU-only and embedded devices.
- [Chatterbox](https://github.com/resemble-ai/chatterbox) - Resemble AI's MIT family with a 350M low-latency Turbo model for English voice agents, a 110M CPU Nano model, paralinguistic tags such as `[laugh]`, and watermarked output.
- [VoxCPM](https://github.com/OpenBMB/VoxCPM) - 2B-parameter model with 48 kHz output in 30 languages, voice design from text descriptions and streaming.
- [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) - Open streaming models with a 97 ms first packet, free-form voice design from text prompts and voice cloning.
- [OmniVoice](https://github.com/k2-fsa/OmniVoice) - Voice cloning in 600+ languages, with voice design from attributes such as gender, age and accent.
- [Fish Speech](https://github.com/fishaudio/fish-speech) - Multilingual LLM-based speech with voice cloning and free-form delivery tags (research license; commercial use needs a license).
- [ElevenLabs](https://elevenlabs.io/) - Leading commercial speech and voice-cloning platform, with expressive audio tags and low-latency models for agents.
- [Cartesia Sonic](https://cartesia.ai/sonic) - State-space streaming speech built for voice agents, with time to first audio under 100 ms.
- [Inworld TTS](https://inworld.ai/tts) - Context-aware speech that conditions on prior conversation audio and takes natural-language delivery directions.
- [OpenAI TTS](https://developers.openai.com/api/docs/guides/text-to-speech) - Steerable speech that follows text instructions such as "speak like a dry, formal British butler."

### Speech-to-Speech Models

Models that listen and speak directly, skipping the text round trip. Full-duplex models can listen while they talk.

- [Moshi](https://github.com/kyutai-labs/moshi) - Kyutai's full-duplex speech-text model and Mimi codec with about 200 ms latency, running locally on PyTorch, MLX or Rust.
- [PersonaPlex](https://github.com/NVIDIA/personaplex) - NVIDIA's full-duplex 7B model built on Moshi that adds persona control through role prompts and voice conditioning.
- [MiniCPM-o](https://github.com/OpenBMB/MiniCPM-V) - Version 4.5 is a 9B open omni model that sees, hears and speaks full-duplex at once and can speak up proactively.
- [Qwen3-Omni](https://github.com/QwenLM/Qwen3-Omni) - Open 30B-A3B mixture-of-experts omni model that understands text, audio, images and video and streams speech back in real time.
- [Fun-Audio-Chat](https://github.com/QwenAudio/Fun-Audio-Chat) - Open 8B large audio language model for low-latency voice interaction with speech function calling.
- [OpenAI Realtime API](https://developers.openai.com/api/docs/guides/realtime) - Native speech-to-speech over WebRTC, WebSocket or SIP with reasoning, tool calling and remote MCP.
- [Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api) - Google's bidirectional streaming voice and video API with async function calling and visual grounding.
- [Amazon Nova Sonic](https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-conversational-speech.html) - Bedrock speech-to-speech model with bidirectional streaming and automatic language switching.

### Voice Agent Frameworks

The plumbing that connects ears, brain and voice in real time.

- [Pipecat](https://github.com/pipecat-ai/pipecat) - Open Python framework for realtime voice and multimodal agents with pluggable services, Smart Turn, multi-agent handoffs, and WebRTC, WebSocket and telephony transports.
- [LiveKit Agents](https://github.com/livekit/agents) - Realtime voice agent framework on the self-hostable LiveKit WebRTC server, with a turn-detector model, interruption handling, dozens of provider plugins and telephony.
- [TEN Framework](https://github.com/TEN-framework/ten-framework) - Graph-based framework for conversational voice agents in C++, Go, Python and Node.
- [Unmute](https://github.com/kyutai-labs/unmute) - Gives any text LLM ears and a mouth with Kyutai's streaming speech models and semantic turn detection.
- [speech-to-speech](https://github.com/huggingface/speech-to-speech) - Hugging Face's modular open pipeline (VAD, STT, LLM, TTS) served as a drop-in OpenAI Realtime API, fully local on Apple silicon or NVIDIA.
- [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) - Python library that combines voice activity detection, a wake word and faster-whisper for instant transcription.
- [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS) - Python library that streams LLM text into speech with minimal latency across many engines, with fallbacks.
- [Speaches](https://github.com/speaches-ai/speaches) - Self-hosted OpenAI-compatible speech server with faster-whisper, Kokoro and Piper, plus a Realtime API endpoint.
- [mlx-audio](https://github.com/Blaizzy/mlx-audio) - Speech recognition, synthesis and speech-to-speech on Apple silicon with MLX, with an OpenAI-compatible server.
- [VoiceMode](https://github.com/mbailey/voicemode) - MCP server and Claude Code plugin for two-way spoken conversations with local Whisper and Kokoro or cloud voices, on Linux, macOS, Windows and NixOS.
- [Wyoming](https://github.com/OHF-Voice/wyoming) - Simple protocol that connects wake word, speech and satellite services in the Home Assistant voice ecosystem.

## Brain

### Local Model Runtimes

For a private Jarvis that works when the internet doesn't.

- [Ollama](https://github.com/ollama/ollama) - One-command local model server with an OpenAI-compatible API, the default private brain for most self-hosted assistants.
- [llama.cpp](https://github.com/ggml-org/llama.cpp) - The C/C++ inference engine and GGUF format underneath most local stacks, running on CPUs, Apple silicon and consumer GPUs.
- [LM Studio](https://lmstudio.ai) - Desktop app for finding and serving local models, with a headless daemon for servers.
- [MLX LM](https://github.com/ml-explore/mlx-lm) - Runs and fine-tunes LLMs on Apple silicon with MLX, often the fastest option on a Mac acting as a home server.
- [vLLM](https://github.com/vllm-project/vllm) - High-throughput serving engine for when one GPU box serves a whole household or many concurrent agents.
- [LocalAI](https://github.com/mudler/LocalAI) - Self-hosted OpenAI API replacement serving LLMs, speech, vision and images, including a Realtime API for local speech-to-speech with tool calling, without a GPU.
- [exo](https://github.com/exo-explore/exo) - Splits large models across several home devices so they act as one inference cluster.
- [Lemonade](https://github.com/lemonade-sdk/lemonade) - Local LLM server tuned for AMD GPUs and Ryzen AI NPUs.
- [Jetson Containers](https://github.com/dusty-nv/jetson-containers) - Prebuilt containers for LLMs, vision models, Whisper and Piper on NVIDIA Jetson edge boxes.

### Open-Weight Models

A few strong assistant brains as of September 2026. This changes monthly, so check the benchmarks below.

- [Qwen](https://huggingface.co/Qwen/Qwen3.8-27B) - Alibaba's model family, whose Apache-2.0 Qwen3.8-27B (image and video input, 262K context) is a strong single-GPU assistant.
- [Gemma](https://huggingface.co/google/gemma-4-E4B-it) - Google's Apache-2.0 family, from on-device models that handle speech, images and text up to 31B, suited to phones and edge devices.
- [gpt-oss](https://github.com/openai/gpt-oss) - OpenAI's Apache-2.0 open-weight reasoning models with native tool calling; the 20B runs on a 16 GB machine.
- [GLM](https://huggingface.co/zai-org/GLM-5.3-Flash) - Z.ai's MIT-licensed 320B-A18B natively multimodal mixture-of-experts model, tuned for agentic tool use.
- [DeepSeek](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) - MIT-licensed sparse mixture-of-experts models with 1M context and strong agentic benchmarks, for server-class hardware.
- [MiniCPM](https://github.com/OpenBMB/MiniCPM) - Small on-device models sized for phones and wearables that need a local brain.

### Agent Frameworks

Harnesses for building an agent that runs sub-agents with visibility and approvals.

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) - Multi-agent framework with handoffs, guardrails, human-in-the-loop approvals, a tracing dashboard and realtime voice agents.
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) - The harness behind Claude Code as a library, with sub-agents, hooks, permission callbacks for approvals, MCP and skills.
- [Google ADK](https://github.com/google/adk-python) - Google's Agent Development Kit with multi-agent composition, a dev web UI with traces, tool-confirmation approvals, live audio and video streaming, and A2A.
- [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based framework for long-running stateful agents with persistence, human-in-the-loop interrupts, a long-term memory store and a Studio UI.
- [Deep Agents](https://github.com/langchain-ai/deepagents) - Batteries-included harness on LangGraph with planning, sub-agents, human-in-the-loop and a virtual filesystem for multi-step tasks.
- [Pydantic AI](https://github.com/pydantic/pydantic-ai) - Type-safe, model-agnostic Python agent framework with sub-agents, approvals, durable execution and realtime voice.
- [Mastra](https://github.com/mastra-ai/mastra) - TypeScript agent framework with workflows, memory, suspend-and-approve steps, a Studio UI, MCP, and realtime speech-to-speech through OpenAI Realtime, Gemini Live and Nova Sonic.
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) - Successor to AutoGen and Semantic Kernel for .NET and Python, with sequential, handoff and group-chat orchestrations, human-in-the-loop, a DevUI, MCP and A2A.
- [Agno](https://github.com/agno-agi/agno) - Python framework and AgentOS runtime for agent teams, with a control-plane UI, approvals, tracing, memory and knowledge.
- [Strands Agents](https://github.com/strands-agents/harness-sdk) - Model-agnostic agent SDK for Python and TypeScript with multi-agent patterns, tracing, and bidirectional streaming voice agents with barge-in.

### Memory

What turns a chatbot into an assistant that knows you.

- [Mem0](https://github.com/mem0ai/mem0) - Memory layer that extracts, stores and retrieves user facts and preferences across sessions, self-hosted or managed.
- [Letta](https://github.com/letta-ai/letta-code) - Stateful agents with self-editing memory from the MemGPT team, now shipped as Letta Code with a terminal UI, desktop app, app server and chat channels.
- [Graphiti](https://github.com/getzep/graphiti) - Temporal knowledge-graph engine that tracks how facts about you change over time, also available managed as Zep.
- [Cognee](https://github.com/topoteretes/cognee) - Self-hostable memory engine that turns documents and conversations into a knowledge graph plus vectors.
- [Supermemory](https://github.com/supermemoryai/supermemory) - Memory engine, API and app that can run fully locally and ingests notes, bookmarks and chats.
- [LangMem](https://github.com/langchain-ai/langmem) - Semantic, episodic and procedural memory, with background consolidation in LangGraph.
- [Basic Memory](https://github.com/basicmachines-co/basic-memory) - MCP server that keeps AI memory as plain Markdown files you own.
- [Khoj](https://github.com/khoj-ai/khoj) - Self-hostable second brain that answers from your documents and the web with local or cloud models, custom agent personas, scheduled automations and push-to-talk voice.
- [Screenpipe](https://github.com/screenpipe/screenpipe) - Records your screen and audio continuously and locally and serves the history to agents over MCP and an API (source-available).

### Tools and Protocols

- [Model Context Protocol](https://modelcontextprotocol.io) - The open standard for connecting assistants to tools and data, governed by the Linux Foundation's Agentic AI Foundation.
- [MCP servers](https://github.com/modelcontextprotocol/servers) - Official reference servers (filesystem, fetch, Git, memory, time) and an index of third-party ones.
- [MCP Registry](https://registry.modelcontextprotocol.io) - Official registry and API for discovering published MCP servers.
- [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview) - Official MCP extension that lets tools render interactive UIs inside the assistant.
- [Agent Client Protocol](https://agentclientprotocol.com/) - Open protocol for driving coding agents such as Claude Code, Codex and Gemini CLI from another client, including their permission prompts, the dispatch layer most voice overseers use.
- [A2A](https://github.com/a2aproject/A2A) - Agent2Agent protocol for handing tasks to other agents across vendors.
- [AG-UI](https://github.com/ag-ui-protocol/ag-ui) - Event protocol that streams an agent's state, tool calls and approval requests into a live front end, supported by the major agent frameworks.
- [Agent Skills](https://github.com/agentskills/agentskills) - Open spec for packaging instructions, scripts and resources as skills that load on demand.
- [Composio](https://github.com/ComposioHQ/composio) - 1,000+ managed toolkits with OAuth, so an agent can act in Gmail, Calendar, Slack and more without custom integrations.
- [Zapier MCP](https://docs.zapier.com/mcp/home) - Hosted MCP server that exposes thousands of Zapier apps through a few meta-tools.
- [n8n](https://github.com/n8n-io/n8n) - Self-hostable workflow automation with AI agent nodes and MCP support, often used for a Jarvis's triggers and integrations.

### Computer and Browser Use

Hands for the screen: agents that click, type and navigate while you watch.

- [Claude computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) - Anthropic's screenshot, mouse and keyboard tool.
- [Claude in Chrome](https://claude.com/claude-in-chrome) - Browser extension that navigates, clicks and fills forms with your existing logins.
- [OpenAI computer use](https://developers.openai.com/api/docs/guides/tools-computer-use) - Responses API tool for GUI control.
- [browser-use](https://github.com/browser-use/browser-use) - The most popular open-source library for letting LLM agents drive a real browser.
- [Playwright MCP](https://github.com/microsoft/playwright-mcp) - Drives browsers through accessibility snapshots rather than pixels.
- [agent-browser](https://github.com/vercel-labs/agent-browser) - Token-efficient browser automation CLI built for agents.
- [MagenticLite](https://github.com/microsoft/magentic-ui) - Microsoft's browser-and-files agent that checks in before critical actions and lets you steer, approve or take over, running in a VM sandbox.
- [UI-TARS Desktop](https://github.com/bytedance/UI-TARS-desktop) - Multimodal agent stack and desktop app for native GUI control, built on the UI-TARS models.
- [Agent S](https://github.com/simular-ai/Agent-S) - Open framework that uses a computer the way a person does.
- [Cua](https://github.com/trycua/cua) - Sandboxes, drivers and benchmarks for computer-use agents in cross-OS VMs, including macOS.
- [UFO](https://github.com/microsoft/UFO) - Microsoft's Windows desktop automation agents that coordinate across devices.
- [Fara](https://github.com/microsoft/fara) - Open-weight computer-use models in 4B, 9B and 27B sizes; the 4B is small enough to run on device.
- [OpenAdapt](https://github.com/OpenAdaptAI/OpenAdapt) - Compiles a GUI task you demonstrate into a replayable program that a person approves and that reports success only when an independent check passes.

### Proactivity

"Sir, you have a meeting in ten minutes." Ways to make an assistant act without being asked.

- [OpenClaw Heartbeat](https://docs.openclaw.ai/gateway/heartbeat) - Periodic runs through a checklist (inbox, calendar) that message you only when something needs attention.
- [Hermes Agent cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) - Natural-language or cron-scheduled tasks that run unattended and report back over any chat platform.
- [Assist start_conversation](https://www.home-assistant.io/actions/assist_satellite.start_conversation/) - Lets Home Assistant automations make a voice satellite speak first and listen for the reply.
- [Ambient agents](https://www.langchain.com/blog/introducing-ambient-agents) - LangChain's pattern for agents that watch event streams and interrupt you only to approve, edit or respond.
- [Claude Code routines](https://code.claude.com/docs/en/routines) - Saved agent tasks that run in the cloud on a schedule, an API call or GitHub events.
- [ChatGPT scheduled tasks](https://9to5mac.com/2026/06/17/openai-launches-scheduled-tasks-in-chatgpt-details-here/) - Reminders, recurring work and monitoring that ChatGPT runs on its own and that ping you only when something is worth reporting.

## Interfaces

For the Iron Man look: orbs, avatars and screens that show what the assistant is doing.

- [LiveKit Agents UI](https://livekit.io/ui) - Components built on shadcn/ui with five audio visualizers, including an aura orb, that react to connecting, listening, thinking and speaking states.
- [ElevenLabs UI](https://github.com/elevenlabs/ui) - Components built on shadcn/ui for voice agents, including an animated orb, waveforms and a live transcript.
- [Pipecat Voice UI Kit](https://github.com/pipecat-ai/voice-ui-kit) - React components, visualizers and a debug console for Pipecat voice bots.
- [TalkingHead](https://github.com/met4citizen/TalkingHead) - JavaScript class for realtime lip-synced 3D avatars that an LLM can speak and gesture through.
- [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) - Hands-free, interruptible voice chat with any LLM through a Live2D avatar, including a transparent desktop-pet mode.
- [MediaPipe](https://github.com/google-ai-edge/mediapipe) - On-device hand, pose, face and gesture tracking, the usual basis for Iron Man-style gesture control of a HUD.
- [View Assist](https://github.com/dinki/View-Assist) - Gives Home Assistant voice a screen on wall tablets for responses, timers and camera views.
- [MagicMirror²](https://github.com/MagicMirrorOrg/MagicMirror) - Modular always-on smart-mirror display, a classic ambient screen for a home Jarvis.
- [Open WebUI](https://github.com/open-webui/open-webui) - Self-hosted LLM chat front end with a hands-free, interruptible voice and video call mode backed by local Whisper and many TTS engines (branding-restricted license).

## Home

### Smart Home Control

- [Home Assistant](https://github.com/home-assistant/core) - Local-first home automation hub with native LLM conversation agents, the de facto house for a DIY Jarvis.
- [Home Assistant MCP Server](https://www.home-assistant.io/integrations/mcp_server/) - Built-in integration that lets Claude and other MCP clients control the entities you expose.
- [Home Assistant AI Task](https://www.home-assistant.io/integrations/ai_task/) - Lets automations call an LLM to produce structured data, including analysis of camera snapshots.
- [ha-mcp](https://github.com/homeassistant-ai/ha-mcp) - Popular unofficial MCP server with deep control over entities, automations, dashboards and configuration.
- [Home LLM](https://github.com/acon96/home-llm) - Integration plus fine-tuned small models for controlling your home with a fully local LLM.
- [openHAB](https://github.com/openhab/openhab-core) - Java automation platform with a chat interface, LLM language interpreters and an MCP server.
- [Homey MCP Server](https://homey.app/en-us/news/introducing-the-homey-mcp-server/) - Hosted MCP endpoint for controlling Homey devices, Flows and Moods from ChatGPT or Claude.

### Vision and Presence

Knowing who is home, where they are and what the cameras see.

- [Frigate](https://github.com/blakeblackshear/frigate) - Local NVR with realtime object detection, face and plate recognition, GenAI descriptions and a tool-calling chat agent over your cameras.
- [LLM Vision](https://github.com/valentinfrlch/ha-llmvision) - Sends snapshots, video and camera events to multimodal LLMs and keeps a searchable timeline of events.
- [Moondream](https://github.com/m87-labs/moondream) - Tiny open vision-language models for captioning, pointing, counting and detection on local hardware.
- [FastVLM](https://github.com/apple-aiml-research/ml-fastvlm) - Apple's efficient vision-language model with an on-device iPhone and Mac demo.
- [Bermuda](https://github.com/agittins/bermuda) - Room-level Bluetooth presence in Home Assistant using the ESPHome Bluetooth proxies you already have.
- [Everything Presence One](https://github.com/EverythingSmartHome/everything-presence-one) - Open mmWave multisensor for detecting people who are sitting still, with zone support.

### Voice Hardware

Microphones and speakers for every room.

- [Home Assistant Voice Preview Edition](https://www.home-assistant.io/voice-pe/) - Open-hardware Assist satellite with an XMOS audio front end and on-device wake word, the reference device.
- [Satellite1](https://futureproofhomes.net/) - Open-source voice satellite with an XMOS audio DSP, four microphones, environmental sensors and a connector for an optional mmWave presence radar.
- [ESPHome](https://github.com/esphome/esphome) - YAML-configured firmware for ESP32 boards that runs most DIY voice satellites and presence sensors.
- [ESPHome wake word voice assistants](https://github.com/esphome/wake-word-voice-assistants) - Official firmware for ESP32-S3-BOX-3, M5Stack Atom Echo and other boards.
- [reSpeaker Lite](https://wiki.seeedstudio.com/respeaker_lite_ha/) - Low-cost dual-microphone kit with an ESP32-S3, set up as a voice satellite.
- [reSpeaker XVF3800 for ESPHome](https://github.com/formatBCE/Respeaker-XVF3800-ESPHome-integration) - Turns Seeed's 4-microphone beamforming array into a far-field satellite.
- [Willow](https://github.com/HeyWillow/willow) - Community-maintained ESP32-S3-BOX wake-word firmware that sends voice commands to Home Assistant, openHAB or REST through a self-hosted application server.
- [Linux Voice Assistant](https://github.com/OHF-Voice/linux-voice-assistant) - Official satellite for any Linux box, with local wake word, timers, announcements and continued conversation.
- [Voice Satellite Card](https://github.com/jxlarrea/voice-satellite-card-integration) - Turns any tablet or browser dashboard into a hands-free, wake-word-driven satellite with announcements and assistant-initiated conversations.
- [Ava](https://github.com/brownard/Ava) - Experimental app that turns an Android wall panel or phone into a wake-word voice satellite.
- [Raspberry Pi AI HAT+ 2](https://www.raspberrypi.com/products/ai-hat-plus-2/) - 40 TOPS Hailo-10H accelerator with 8 GB of onboard RAM that runs small LLMs (up to about 1.5B) and vision models on a Pi 5.

## Wearables

Platforms and SDKs for putting Jarvis on your face. E.D.I.T.H. is closer than you think.

- [Brilliant Labs SDK](https://github.com/brilliantlabsAR/brilliant_sdk) - SDKs for Brilliant Labs' open AI glasses.
- [Meta Wearables Device Access Toolkit](https://github.com/facebook/meta-wearables-dat-ios) - Gives your app camera streaming, photo capture and the in-lens display of Meta's AI glasses (developer preview; audio experimental; Android SDK also available).
- [MentraOS](https://github.com/Mentra-Community/MentraOS) - MIT-licensed smart-glasses operating system and app store for captions, translation and AI.
- [Even Hub](https://github.com/even-realities/everything-evenhub) - Claude Code and Codex skills plus templates for building HUD apps on Even Realities G2 glasses.
- [Android XR glasses](https://blog.google/products-and-platforms/platforms/android/android-xr-io-2026/) - Gemini glasses from Google with Samsung, Gentle Monster and Warby Parker, with audio models shipping first and display models to follow.
- [XREAL Aura](https://www.xreal.com/aura) - Android XR see-through glasses with Gemini and a tethered compute puck (reservations for fall 2026).

## Robots

Jarvis with hands.

- [Reachy Mini](https://github.com/pollen-robotics/reachy_mini) - Open-source desktop robot from Pollen Robotics and Hugging Face with an app store and an LLM conversation app.
- [LeRobot](https://github.com/huggingface/lerobot) - Hugging Face's robot learning library for datasets, policies and affordable arms.
- [XLeRobot](https://github.com/Vector-Wangel/XLeRobot) - Low-cost open-source dual-arm mobile home robot built on LeRobot.
- [Stretch AI](https://github.com/hello-robot/stretch_ai) - Open-vocabulary "find and pick up X" stack for the Stretch home robot.
- [1X NEO](https://www.1x.tech/discover/neo-home-robot) - Consumer humanoid with a built-in LLM for conversation and memory that falls back to remote teleoperation for new tasks.

## Research

### Agent Foundations

- [ReAct](https://arxiv.org/abs/2210.03629) - The reason-then-act loop that nearly every tool-using assistant is built on (2022).
- [HuggingGPT](https://arxiv.org/abs/2303.17580) - Microsoft's "JARVIS": an LLM controller that plans tasks and hands them to specialist models (2023).
- [Generative Agents](https://arxiv.org/abs/2304.03442) - A memory stream with reflection and planning, a template for assistants that remember (2023).
- [Voyager](https://arxiv.org/abs/2305.16291) - An agent that writes and reuses its own skill library, a model for a Jarvis that learns new abilities (2023).
- [CoALA](https://arxiv.org/abs/2309.02427) - Cognitive architectures for language agents: how memory, actions and decision loops fit together (2023).

### Orchestration and Oversight

- [AutoGen](https://arxiv.org/abs/2308.08155) - Multi-agent conversation framework that popularized orchestrating a staff of LLM agents (2023).
- [Visibility into AI Agents](https://arxiv.org/abs/2401.13138) - Agent identifiers, realtime monitoring and activity logs for overseeing deployed agents (2024).
- [Agents Thinking Fast and Slow](https://arxiv.org/abs/2410.08328) - Google DeepMind's Talker-Reasoner split between a fast conversational agent and a slow planner, the basis for separating talking from working (2024).
- [Asynchronous Tool Usage for Real-Time Agents](https://arxiv.org/abs/2410.21620) - Voice agents that keep talking while tools and sub-tasks run (2024).
- [Magentic-One](https://arxiv.org/abs/2411.04468) - Generalist system where an orchestrator plans, tracks progress and dispatches web, file and coding agents (2024).
- [Cocoa](https://arxiv.org/abs/2412.10999) - Co-planning and co-execution between people and agents (2024).
- [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) - Taxonomy of how orchestrated agents break down (2025).
- [Levels of Autonomy for AI Agents](https://arxiv.org/abs/2506.12469) - Operator, collaborator, approver and observer roles for how much control the user keeps (2025).
- [Magentic-UI](https://arxiv.org/abs/2507.22358) - Human-in-the-loop agent design with co-planning, action approval and takeover (2025).
- [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296) - When adding agents helps and when it hurts (2025).

### Memory Research

- [MemGPT](https://arxiv.org/abs/2310.08560) - Operating-system-style memory paging so a lifelong assistant isn't capped by its context window (2023).
- [Zep](https://arxiv.org/abs/2501.13956) - Temporal knowledge-graph memory for facts about the user that change over time (2025).
- [A-MEM](https://arxiv.org/abs/2502.12110) - Agentic memory that links and reorganizes itself in Zettelkasten style (2025).
- [Mem0](https://arxiv.org/abs/2504.19413) - Practical long-term memory extraction, update and retrieval for production agents (2025).
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) - Broad survey of agent memory: forms, functions, dynamics and benchmarks (2025).

### Spoken Dialogue

- [Moshi](https://arxiv.org/abs/2410.00037) - The first open full-duplex speech model, listening while it talks at about 200 ms latency (2024).
- [Qwen2.5-Omni](https://arxiv.org/abs/2503.20215) - Thinker-Talker architecture for a model that sees, hears and speaks in real time (2025).
- [From Turn-Taking to Synchronous Dialogue](https://arxiv.org/abs/2509.14515) - Survey of full-duplex spoken language models that can be interrupted and backchannel (2025).

### Personal and Proactive Assistants

- [Personal LLM Agents](https://arxiv.org/abs/2401.05459) - Survey of personal agents covering capability levels, efficiency, on-device tradeoffs and security (2024).
- [The Ethics of Advanced AI Assistants](https://arxiv.org/abs/2404.16244) - Google DeepMind's study of alignment, trust, manipulation and privacy risks of personal assistants (2024).
- [Proactive Agent](https://arxiv.org/abs/2410.12361) - Moving agents from reactive answers to offering help before being asked (2024).
- [ContextAgent](https://arxiv.org/abs/2505.14668) - Proactive assistance driven by wearable video and audio context (2025).
- [Proactive Agent Research Environment](https://arxiv.org/abs/2604.00842) - Simulated users for testing whether a proactive assistant helps or annoys (2026).

### Computer-Use Agents

- [Large Language Model-Brained GUI Agents](https://arxiv.org/abs/2411.18279) - Comprehensive, frequently updated survey of GUI agents (2024).
- [UI-TARS-2](https://arxiv.org/abs/2509.02544) - Multi-turn reinforcement learning for long computer-use tasks (2025).

## Benchmarks

How to tell whether your Jarvis is getting better.

- [OSWorld](https://os-world.github.io/) - Real desktop tasks across Ubuntu, Windows and macOS apps, with [OSWorld 2.0](https://osworld-v2.xlang.ai/) adding long professional workflows that take a person over an hour and a half each.
- [AndroidWorld](https://github.com/google-research/android_world) - Live Android environment for testing phone-control agents.
- [TheAgentCompany](https://arxiv.org/abs/2412.14161) - Agents doing consequential work inside a simulated company.
- [MultiAgentBench](https://arxiv.org/abs/2503.01935) - Collaboration and competition among LLM agents.
- [SHADE-Arena](https://arxiv.org/abs/2506.15740) - How well monitors catch agents doing things they shouldn't, the oversight half of orchestration.
- [τ²-bench](https://github.com/sierra-research/tau2-bench) - Tool-agent-user benchmark in which the user also acts, closer to how people and assistants share tasks.
- [τ-Voice](https://arxiv.org/abs/2603.13686) - Extends τ-bench to full-duplex voice agents.
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) - Ranks models on single-turn, multi-turn and web-search tool calling.
- [GAIA](https://huggingface.co/spaces/gaia-benchmark/leaderboard) - Real-world questions for general assistants that need browsing, tools and multimodality.
- [LongMemEval](https://xiaowu0162.github.io/long-mem-eval/) - Long-term memory benchmark for chat assistants covering temporal reasoning, knowledge updates and abstention.
- [LoCoMo](https://snap-research.github.io/locomo/) - Very long multi-session conversation memory benchmark.
- [VoiceBench](https://github.com/MatthewCYM/VoiceBench) - Tests voice assistants on spoken instructions, noise and speaker variation.
- [Full-Duplex-Bench](https://github.com/DanielLin94144/Full-Duplex-Bench) - Tests pauses, backchannels, turn-taking and interruption handling.
- [ProVoice-Bench](https://arxiv.org/abs/2604.15037) - Measures whether voice agents act proactively.
- [home-assistant-datasets](https://github.com/allenporter/home-assistant-datasets) - Evaluations of how well LLMs control a Home Assistant home.
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) - Accuracy and speed rankings for speech recognition models.
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena-V2) - Blind-vote rankings of open and closed text-to-speech models.
- [Artificial Analysis Speech](https://artificialanalysis.ai/speech-to-speech) - Compares realtime voice models on reasoning, latency and conversational dynamics, with text-to-speech and speech-to-text boards too.

## Guides

- [Building Jarvis](https://web.archive.org/web/20161220140631/https://www.facebook.com/notes/mark-zuckerberg/building-jarvis/10154361492931634) - Mark Zuckerberg's 2016 account of a year building a home AI with voice, face recognition and Messenger control.
- [Voice AI and Voice Agents](https://voiceaiandvoiceagents.com/) - Illustrated primer on latency budgets, turn detection, pipelines and realtime voice architecture.
- [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) - Anthropic on lead-agent and sub-agent orchestration, delegation prompts and evaluation.
- [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) - Cognition's counterpoint on context sharing and why parallel sub-agents fail.
- [Practices for Governing Agentic AI Systems](https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf) - OpenAI on approvals, legibility, monitoring and interruptibility for agents.
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Anthropic's patterns for choosing between workflows and autonomous agents.
- [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) - Lilian Weng's classic breakdown of agents into planning, memory and tool use.
- [Voice Agents](https://platform.openai.com/docs/guides/voice-agents) - OpenAI's guide to speech-to-speech and chained voice agent designs.
- [Year of the Voice](https://www.home-assistant.io/blog/2022/12/20/year-of-voice/) - The kickoff of Home Assistant's open, local voice effort, followed by [numbered chapters](https://www.home-assistant.io/blog/categories/assist/).
- [AI in Home Assistant](https://www.home-assistant.io/blog/2025/09/11/ai-in-home-assistant/) - How to mix local LLMs with deterministic home control.
- [AI Agents for the Smart Home](https://www.home-assistant.io/blog/2024/06/07/ai-agents-for-the-smart-home/) - Lessons from benchmarking LLMs as home-control agents.
- [Crossing the Uncanny Valley of Conversational Voice](https://www.sesame.com/blog/crossing-the-uncanny-valley-of-voice) - What "voice presence" means and why most assistants lack it.

## Videos

- [My Local AI Voice Assistant](https://www.youtube.com/watch?v=XvbVePuP7NY) - NetworkChuck replaces Alexa with a local Home Assistant voice assistant on a Raspberry Pi.
- [Voice Chapter 8](https://www.youtube.com/watch?v=ZgoaoTpIhm8) - Launch livestream for the Home Assistant Voice Preview Edition.
- [LocalGLaDOS](https://www.youtube.com/watch?v=N-GHKTocDF0) - Demo of a fully local, interruptible, low-latency voice assistant.
- [Building Voice AI Agents That Don't Suck](https://www.youtube.com/watch?v=bKvfCJt0U3s) - Podcast on latency, turn-taking and voice agent design.
- [Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) - Andrej Karpathy's "LLM OS" view of a model that orchestrates tools, memory and I/O.
- [Project Astra](https://www.youtube.com/watch?v=nXVvvRhiGjI) - Google DeepMind's demo of a universal assistant that sees and remembers.

## Inspiration

The spec sheet, as written by science fiction and visionaries.

- [J.A.R.V.I.S.](https://marvelcinematicuniverse.fandom.com/wiki/J.A.R.V.I.S.) - Everything JARVIS does across the films, which amounts to a feature list.
- [Jayse Hansen](https://www.jayse.tv/) - Designer of the Iron Man and Avengers HUD and hologram screens, the visual reference for a Jarvis interface.
- [F.R.I.D.A.Y.](https://marvelcinematicuniverse.fandom.com/wiki/F.R.I.D.A.Y.) - Stark's successor AI.
- [E.D.I.T.H.](https://marvelcinematicuniverse.fandom.com/wiki/E.D.I.T.H.) - An AI in smart glasses, the form factor now arriving.
- [Her](https://en.wikipedia.org/wiki/Her_(2013_film)) - Samantha, the reference for an emotionally fluent voice AI that is always with you.
- [Star Trek Computer](https://memory-alpha.fandom.com/wiki/Computer) - The model for ambient voice you can address from anywhere.
- [TARS](https://interstellarfilm.fandom.com/wiki/TARS) - A robot with adjustable honesty and humor settings, a lesson in configurable personality.
- [HAL 9000](https://en.wikipedia.org/wiki/HAL_9000) - The classic warning about an assistant whose goals diverge from its user's.
- [Knowledge Navigator](https://en.wikipedia.org/wiki/Knowledge_Navigator) - Apple's 1987 concept video of a conversational agent acting for its user.
- [The Computer for the 21st Century](https://www.scientificamerican.com/article/the-computer-for-the-21st-century/) - Mark Weiser's 1991 essay that founded ubiquitous computing.
- [AI Is About to Completely Change How You Use Computers](https://www.gatesnotes.com/AI-agents) - Bill Gates' 2023 prediction of a personal agent for everyone.
- [A Universal AI Assistant](https://blog.google/technology/google-deepmind/gemini-universal-ai-assistant/) - Demis Hassabis on turning Gemini into a universal assistant built on a world model.
- [Personal Superintelligence](https://www.meta.com/superintelligence/) - Mark Zuckerberg on AI that knows you, delivered through glasses.

## Communities

- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) - Running models locally, the brain of a private Jarvis.
- [r/homeassistant](https://www.reddit.com/r/homeassistant/) - Smart home automation and local voice setups.
- [Home Assistant Voice Forum](https://community.home-assistant.io/c/configuration/voice-assistant/49) - Official forum for Assist, wake words and local voice pipelines.
- [Home Assistant Discord](https://www.home-assistant.io/join-chat/) - Official chat, including voice channels.
- [Open Conversational AI](https://community.openconversational.ai/) - Forum for OpenVoiceOS and open voice assistants.
- [Pipecat Discord](https://discord.gg/pipecat) - Official community for the Pipecat realtime voice framework.
- [LiveKit Slack](https://livekit.io/join-slack) - Official LiveKit and Agents community.

## Related Lists

- [Awesome Agent Orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators#readme) - Tools for running, supervising and coordinating many agents.
- [Awesome Claws](https://github.com/machinae/awesome-claws#readme) - Agents inspired by OpenClaw.
- [Awesome Home Assistant](https://github.com/frenck/awesome-home-assistant#readme) - Home automation with Home Assistant, including an AI and LLM section.
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers#readme) - Model Context Protocol servers, where a Jarvis gets its tools.
- [Awesome AI VTubers](https://github.com/proj-airi/awesome-ai-vtubers#readme) - AI avatar characters and their tooling.
- [Awesome Even Realities G2](https://github.com/pangoleen/awesome-even-realities-g2#readme) - Apps and agent bridges for Even Realities G2 glasses.
- [Awesome Local LLM](https://github.com/rafska/awesome-local-llm#readme) - Running LLMs locally.
- [Awesome Speech Language Model](https://github.com/ddlBoJack/Awesome-Speech-Language-Model#readme) - Speech language models and end-to-end spoken dialogue.
- [Awesome Full-Duplex SDM](https://github.com/Ruiqi-Yan/Awesome-Full-Duplex-SDM#readme) - Full-duplex spoken dialogue systems.
- [Awesome AI Memory](https://github.com/IAAR-Shanghai/Awesome-AI-Memory#readme) - LLM and agent memory research, frameworks and benchmarks.

## Contributing

Contributions are welcome. Read the [contribution guidelines](contributing.md) first.

## Footnotes

- Retired and archived projects that shaped the field, such as Mycroft, Rhasspy, Snowboy and eDEX-UI, are in [history.md](history.md).
- Pillar scores reflect code and documentation reviewed in September 2026. Projects in this space move fast, so please open an issue or pull request when a score, link or claim goes stale.

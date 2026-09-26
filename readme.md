# Awesome Jarvis [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

<p align="center">
	<a href="blueprint.md"><img src="media/banner.jpg" width="784" alt="Glowing circular heads-up display with a voice waveform running through it"></a>
</p>

> Real-life J.A.R.V.I.S.: always-available, voice-first personal AI assistants that know you, remember, see and hear the world, run your home and computer, and act on your behalf.

Tony Stark's assistant needed ears (wake word, speech recognition), a voice (speech synthesis), a brain (a model with memory and tools), hands (home, computer and browser control), eyes (cameras and presence), and a body (speakers, glasses, screens). In 2026 every one of those layers has solid open-source and commercial options. This list collects the best of each, verified live, plus the research, guides and culture behind them. New to this? Read the [blueprint](blueprint.md) first for a reference architecture and three starter builds.

## Contents

- [Complete Assistants](#complete-assistants)
	- [Always-On Agent Assistants](#always-on-agent-assistants)
	- [Voice-First Assistants](#voice-first-assistants)
	- [Voice Platforms and Smart Speakers](#voice-platforms-and-smart-speakers)
	- [Commercial Assistants](#commercial-assistants)
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
	- [Tools and Integrations](#tools-and-integrations)
	- [Computer and Browser Use](#computer-and-browser-use)
	- [Proactivity](#proactivity)
- [Home](#home)
	- [Smart Home Control](#smart-home-control)
	- [Vision and Presence](#vision-and-presence)
	- [Voice Hardware](#voice-hardware)
- [Wearables](#wearables)
- [Interfaces](#interfaces)
- [Robots](#robots)
- [Research](#research)
	- [Agent Foundations](#agent-foundations)
	- [Memory Research](#memory-research)
	- [Spoken Dialogue](#spoken-dialogue)
	- [Personal and Proactive Assistants](#personal-and-proactive-assistants)
	- [Computer-Use Agents](#computer-use-agents)
- [Benchmarks](#benchmarks)
- [Guides](#guides)
- [Videos](#videos)
- [Inspiration](#inspiration)
- [Communities](#communities)

## Complete Assistants

Things you can run or buy today that already put several layers together.

### Always-On Agent Assistants

Self-hosted agents that live on your hardware, reach you over chat apps and work in the background. Most are chat-first, and several add voice.

- [OpenClaw](https://github.com/openclaw/openclaw) - Self-hosted personal agent gateway with memory, skills, dozens of chat channels, heartbeat and cron proactivity, and voice wake plus camera and screen actions through companion device nodes.
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) - Nous Research's self-improving assistant with curated long-term memory, skills it writes itself, a cron scheduler, a multi-platform chat gateway and a voice mode with an optional wake word.
- [nanobot](https://github.com/HKUDS/nanobot) - Lightweight Python take on OpenClaw with a web UI, memory, MCP tools, multi-agent workflows, scheduled automations and chat-app access.
- [QwenPaw](https://github.com/agentscope-ai/QwenPaw) - AgentScope's personal assistant with three-layer memory that grows into a personal knowledge base, a built-in local model runtime and sub-agents.
- [ZeroClaw](https://github.com/zeroclaw-labs/zeroclaw) - Always-on assistant in a single Rust binary with about 20 LLM providers, 30+ channels and swappable components.
- [NanoClaw](https://github.com/nanocoai/nanoclaw) - Small, auditable assistant on the Claude Agent SDK that isolates each agent in its own container, with memory, scheduled jobs and messaging connectors.
- [PicoClaw](https://github.com/sipeed/picoclaw) - Single Go binary built to run on cheap boards and old Android phones, reachable over 19+ messaging platforms.
- [IronClaw](https://github.com/nearai/ironclaw) - Security-first Rust assistant with WASM-sandboxed tools, credential injection, prompt-injection defenses and a heartbeat for background work.
- [MimiClaw](https://github.com/memovai/mimiclaw) - Bare-metal C agent for a roughly $5 ESP32-S3 with local-first memory that runs on USB power with no operating system.
- [Moltis](https://github.com/moltis-org/moltis) - Rust personal agent server with sandboxed execution, long-term memory, voice input and output, MCP tools and chat channels.

### Voice-First Assistants

Assistants built around talking, the way Tony does.

- [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) - Framework for on-device personal AI with hardware-aware local model selection, several agent types, MCP tools, memory that learns from traces and spoken scheduled digests.
- [isair/jarvis](https://github.com/isair/jarvis) - Fully local voice assistant for macOS, Windows and Linux that hears "Jarvis" anywhere in a sentence, follows the conversation in the room, and keeps a local diary and knowledge graph.
- [GLaDOS](https://github.com/dnhkng/GLaDOS) - Local, interruptible, low-latency voice assistant with a persona that reacts to vision, sound and time events, with long-term memory and MCP tools.
- [usejarvis](https://github.com/vierisid/jarvis) - Always-on daemon with openWakeWord, screen awareness through sidecars on your machines, an agent hierarchy, goal pursuit and user-defined authority limits (source-available).
- [JARVIS for Claude Code](https://github.com/ethanplusai/jarvis) - macOS voice butler that plans projects out loud, drives Claude Code sessions and speaks up when a session needs you.
- [Leon](https://github.com/leon-ai/leon) - Long-running open-source personal assistant being rebuilt around tools, layered memory, computer use, local or remote models and a bounded proactive pulse.
- [Khoj](https://github.com/khoj-ai/khoj) - Self-hostable second brain that answers from your documents and the web with local or cloud models, custom agents, scheduled automations and spoken replies.
- [Open WebUI](https://github.com/open-webui/open-webui) - Self-hosted LLM front end with a hands-free voice and video call mode backed by local Whisper and many TTS engines.
- [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) - Local-first agent workspace with document chat, agents and pluggable speech-to-text and text-to-speech.
- [Priler/jarvis](https://github.com/Priler/jarvis) - Offline Rust and Tauri voice assistant with Vosk speech recognition and a wake word (Russian, work in progress).

### Voice Platforms and Smart Speakers

Replacements for Alexa and Google Home that you control.

- [Home Assistant Assist](https://www.home-assistant.io/voice_control/) - Home Assistant's voice pipeline (wake word, speech-to-text, conversation agent, text-to-speech) that runs fully local or with an LLM and can now start conversations on its own.
- [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) - ESP32 voice device firmware with offline wake word, full-duplex streaming speech and LLM, speaker recognition, camera input and MCP on device and server, supporting 70+ boards.
- [OpenVoiceOS](https://github.com/OpenVoiceOS/ovos-core) - Community continuation of Mycroft with skills, an LLM persona fallback, and Raspberry Pi and Docker images.
- [Neon AI](https://github.com/NeonGeckoCom/NeonCore) - Mycroft-derived voice assistant core with multi-user support and containerized speech services.
- [Willow](https://github.com/HeyWillow/willow) - ESP32-S3-BOX firmware built as a local Echo replacement, paired with a self-hosted inference server.
- [Dicio](https://github.com/DicioTeam/dicio-android) - Free, offline Android voice assistant with Vosk speech recognition, a wake word and a skills system.

### Commercial Assistants

Only the capabilities that make them Jarvis-like are noted. Status as of September 2026.

- [ChatGPT](https://chatgpt.com) - Full-duplex voice, memory, scheduled tasks, and voice-triggered agentic workflows on mobile and desktop.
- [Gemini](https://gemini.google.com) - Live camera and screen conversations, personal context from Gmail and Photos, scheduled actions and a 24/7 background agent for top-tier subscribers.
- [Siri](https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/) - Rebuilt in iOS and macOS 27 with personal context across apps, on-screen awareness and cross-app actions.
- [Alexa+](https://www.aboutamazon.com/news/devices/new-alexa-generative-artificial-intelligence) - Generative Alexa across Echo devices, Fire TV, the app and the web that runs smart-home routines and books services on your behalf.
- [Meta Muse](https://ai.meta.com/muse/) - Meta's personal agent that remembers preferences, suggests actions proactively, takes voice commands and keeps working in a cloud VM, with glasses support announced.
- [Claude](https://claude.com) - Voice mode, memory across chats and Cowork, and background and scheduled tasks that operate your apps and browser.
- [Microsoft Copilot](https://copilot.microsoft.com) - "Hey Copilot" wake word on Windows plus opt-in Copilot Actions that operate apps and files for you.
- [Perplexity Comet](https://www.perplexity.ai/comet) - AI browser with a screen-aware voice mode and an agent that clicks, fills forms and navigates for you.
- [Grok](https://grok.com) - Voice assistant built into Tesla vehicles that controls car functions and handles email, calendar and errands on the top tier.

### AI Devices

Dedicated hardware for talking to an assistant. Glasses and pendants built for developers are under Wearables.

- [Meta Ray-Ban Display](https://www.meta.com/ai-glasses/meta-ray-ban-display/) - Glasses with an in-lens display, an EMG wristband for gesture control, and Meta AI with navigation and live captions.
- [Ray-Ban Meta](https://www.meta.com/ai-glasses/) - Camera glasses and camera-free audio glasses for hands-free access to Meta AI.
- [Brilliant Labs Halo](https://brilliant.xyz/products/halo) - Open-source glasses with a color display, bone-conduction audio and the Noa assistant, which remembers what you see and hear.
- [Omi](https://www.omi.me/) - Open-source pendant that turns your conversations into memories and action items, with a plugin ecosystem and a screen-aware desktop app.
- [Bee](https://www.bee.computer/) - Amazon-owned wristband or clip that turns your conversations into summaries, reminders and daily insights.
- [Plaud NotePin S](https://www.plaud.ai/products/plaud-notepin-s) - Wearable recorder with a highlight button, transcription in 112 languages and AI summaries.
- [Rabbit r1](https://www.rabbit.tech/updates) - Pocket voice device whose rabbitOS 3 adds persistent memory, computer control over USB and bring-your-own model keys.
- [Google Home Speaker](https://blog.google/products-and-platforms/devices/google-nest/google-home-speaker-gemini-features/) - Smart speaker built for Gemini for Home with multi-command requests and conversational context.

## Ears

### Wake Word

- [openWakeWord](https://github.com/dscripka/openWakeWord) - Offline wake word framework that runs on a CPU or Raspberry Pi, trains custom words from synthetic speech, and powers Home Assistant's wake word add-on.
- [microWakeWord](https://github.com/OHF-Voice/micro-wake-word) - Trains tiny streaming wake word models for ESP32-S3 microcontrollers, and runs on-device in ESPHome and the Home Assistant Voice Preview Edition.
- [LiveKit WakeWord](https://github.com/livekit/livekit-wakeword) - Successor to openWakeWord with a conv-attention classifier, backward-compatible models and custom training in 30+ languages.
- [Porcupine](https://github.com/Picovoice/porcupine) - Commercial on-device wake word engine with SDKs for microcontrollers, mobile, web and desktop, and a free tier.

### Voice Activity and Turn Detection

Voice activity detection hears that someone is talking. Turn detection decides whether they are done, which is what makes a conversation feel natural.

- [Silero VAD](https://github.com/snakers4/silero-vad) - De facto open voice activity detector, a 2 MB model that processes a 30 ms chunk in under 1 ms on one CPU thread.
- [TEN VAD](https://github.com/TEN-framework/ten-vad) - Low-latency frame-level voice activity detector that catches speech-to-silence transitions faster than Silero, with C, Python, WebAssembly and mobile builds.
- [Smart Turn](https://github.com/pipecat-ai/smart-turn) - Audio-native turn detection model that uses prosody as well as silence, in an 8 MB CPU build covering 23 languages.
- [LiveKit Turn Detector](https://huggingface.co/livekit/turn-detector) - Open-weight semantic end-of-turn model that reads the transcript to decide whether the user is finished, running on CPU in 14 languages.
- [TEN Turn Detection](https://github.com/TEN-framework/ten-turn-detection) - Text-based model that classifies an utterance as finished, unfinished, or a request for the assistant to stop talking.

### Speech-to-Text

- [whisper.cpp](https://github.com/ggml-org/whisper.cpp) - Dependency-free C/C++ port of Whisper with Metal, CUDA, Vulkan and Core ML acceleration, running well on Apple silicon, Raspberry Pi and phones.
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) - CTranslate2 reimplementation of Whisper that is up to 4x faster with less memory, the backbone of most self-hosted Whisper servers.
- [Whisper](https://github.com/openai/whisper) - OpenAI's reference multilingual speech recognition and translation model.
- [WhisperX](https://github.com/m-bain/whisperX) - Whisper plus word-level timestamps and speaker diarization, for knowing who said what.
- [Parakeet TDT](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) - NVIDIA's 600M-parameter model for 25 European languages with very high throughput, one of the best choices for fast local transcription.
- [Canary-Qwen](https://huggingface.co/nvidia/canary-qwen-2.5b) - NVIDIA's speech-augmented LLM that has led the English Open ASR Leaderboard.
- [Moonshine](https://github.com/moonshine-ai/moonshine) - On-device streaming speech recognition for Python, WebAssembly, iOS, Android and Raspberry Pi, built to transcribe while the user is still speaking.
- [Voxtral Realtime](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602) - Mistral's open-weight 4B streaming model with configurable latency under 200 ms in 13 languages.
- [Kyutai STT](https://github.com/kyutai-labs/delayed-streams-modeling) - Streaming speech-to-text and text-to-speech models with semantic voice activity detection and batched Rust serving.
- [Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR) - Open multilingual recognition models with language identification and timestamps.
- [FunASR](https://github.com/modelscope/FunASR) - Speech toolkit with streaming recognition, voice activity detection, punctuation and diarization, strongest for Chinese and other Asian languages.
- [VibeVoice](https://github.com/microsoft/VibeVoice) - Microsoft's open voice family, which transcribes an hour of multi-speaker audio in one pass and also includes long-form and realtime text-to-speech.
- [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) - Offline speech recognition, synthesis, voice activity detection and keyword spotting on ONNX Runtime, from RISC-V boards to servers.
- [Speech-to-Phrase](https://github.com/OHF-Voice/speech-to-phrase) - Fast local recognition for Home Assistant that is trained on your own device and area names, so it matches home commands instead of transcribing open speech.
- [Vosk](https://github.com/alphacep/vosk-api) - Mature offline recognition with 50 MB models for 20+ languages that runs on Raspberry Pi and Android.
- [FluidAudio](https://github.com/FluidInference/FluidAudio) - Swift and Core ML SDK that runs Parakeet, Kokoro, Silero VAD and diarization on the Apple Neural Engine.
- [Deepgram](https://deepgram.com/) - Cloud speech recognition, including a conversational model with built-in end-of-turn detection for voice agents.
- [AssemblyAI Universal-Streaming](https://www.assemblyai.com/universal-streaming) - Cloud streaming recognition for voice agents with neural end-of-turn detection.
- [ElevenLabs Scribe](https://elevenlabs.io/speech-to-text) - Low-latency cloud streaming recognition in 90 languages.
- [Speechmatics](https://www.speechmatics.com/) - Cloud or on-premises realtime recognition with broad language coverage and diarization.

## Voice

### Text-to-Speech

For a butler-style voice, prefer voice design from a text description, which VoxCPM, Qwen3-TTS and OmniVoice support. It avoids cloning a real person. Only clone voices you have the rights to.

- [Piper](https://github.com/OHF-Voice/piper1-gpl) - Fast local neural voices that run in real time on a Raspberry Pi, in dozens of languages including British English, maintained by the Open Home Foundation.
- [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) - 82M-parameter model that outscores far larger ones in listening arenas and is fast on CPU, with US and UK English voices.
- [Pocket TTS](https://github.com/kyutai-labs/pocket-tts) - Kyutai's 100M-parameter streaming model that runs in real time on a CPU after a `pip install`, with voice cloning.
- [KittenTTS](https://github.com/KittenML/KittenTTS) - Tiny ONNX models (15M to 80M parameters) for CPU-only and embedded devices.
- [Chatterbox](https://github.com/resemble-ai/chatterbox) - Resemble AI's open family with a low-latency Turbo model, a CPU-sized Nano model, emotion control and watermarked output.
- [VoxCPM](https://github.com/OpenBMB/VoxCPM) - 2B-parameter model with 48 kHz output in 30 languages, voice design from text descriptions and streaming.
- [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) - Open streaming models with free-form voice design from text prompts and voice cloning.
- [OmniVoice](https://github.com/k2-fsa/OmniVoice) - Voice cloning in 600+ languages, with voice design from attributes such as gender, age and accent.
- [F5-TTS](https://github.com/SWivid/F5-TTS) - Flow-matching voice cloning that works from short reference clips (weights are non-commercial).
- [Fish Speech](https://github.com/fishaudio/fish-speech) - Multilingual LLM-based speech with voice cloning and emotion markers (commercial use needs a license).
- [Orpheus TTS](https://github.com/canopyai/Orpheus-TTS) - Emotive speech with tags such as `<laugh>` and `<sigh>`, streaming at about 200 ms latency.
- [Dia](https://github.com/nari-labs/dia) - Dialogue model that generates multi-speaker conversations with nonverbal sounds in one pass.
- [NeuTTS](https://github.com/neuphonic/neutts) - On-device speech models shipped as GGUF for phones and Raspberry Pis, with 3-second voice cloning.
- [Higgs Audio](https://github.com/boson-ai/higgs-audio) - Expressive multi-speaker generation from an LLM-based audio foundation model.
- [CosyVoice](https://github.com/QwenAudio/CosyVoice) - Multilingual streaming speech with voice cloning and a full training and deployment stack.
- [IndexTTS](https://github.com/index-tts/index-tts) - Voice cloning with independent control of timbre, emotion and exact duration.
- [Coqui TTS](https://github.com/idiap/coqui-ai-TTS) - Community fork that keeps Coqui's XTTS-v2 cloning model and toolkit working after the company shut down.
- [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) - OpenAI-compatible server for Kokoro that is simple to plug into any assistant.
- [ElevenLabs](https://elevenlabs.io/) - Leading commercial speech and voice-cloning platform, with expressive audio tags and low-latency models for agents.
- [Cartesia Sonic](https://cartesia.ai/sonic) - State-space streaming speech built for voice agents, with time to first audio under 100 ms.
- [Inworld TTS](https://inworld.ai/tts) - Context-aware speech that conditions on prior conversation audio and takes natural-language delivery directions.
- [OpenAI TTS](https://developers.openai.com/api/docs/guides/text-to-speech) - Steerable speech that follows text instructions such as "speak like a dry, formal British butler."

### Speech-to-Speech Models

Models that listen and speak directly, skipping the text round trip. Full-duplex models can listen while they talk.

- [Moshi](https://github.com/kyutai-labs/moshi) - Kyutai's full-duplex speech-text model and Mimi codec with about 200 ms latency, running locally on PyTorch, MLX or Rust.
- [PersonaPlex](https://github.com/NVIDIA/personaplex) - NVIDIA's full-duplex 7B model built on Moshi that adds persona control through role prompts and voice conditioning.
- [MiniCPM-o](https://github.com/OpenBMB/MiniCPM-V) - Open omni models that see, hear and speak full-duplex at once and can interject proactively.
- [Qwen3-Omni](https://github.com/QwenLM/Qwen3-Omni) - Open 30B-A3B mixture-of-experts omni model that understands text, audio, images and video and streams speech back in real time.
- [Step-Audio 2](https://github.com/stepfun-ai/Step-Audio2) - End-to-end audio LLM with paralinguistic awareness and tool calling.
- [Fun-Audio-Chat](https://github.com/QwenAudio/Fun-Audio-Chat) - Open large audio language model for natural, low-latency voice interaction.
- [Ultravox](https://github.com/fixie-ai/ultravox) - Speech-in LLM that projects audio directly into an open LLM's embeddings with no separate recognition step.
- [OpenAI Realtime API](https://developers.openai.com/api/docs/guides/realtime) - Native speech-to-speech over WebRTC, WebSocket or SIP with reasoning, tool calling and remote MCP.
- [Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api) - Google's bidirectional streaming voice and video API with async function calling and visual grounding.
- [Amazon Nova Sonic](https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-conversational-speech.html) - Bedrock speech-to-speech model with bidirectional streaming and automatic language switching.

### Voice Agent Frameworks

The plumbing that connects ears, brain and voice in real time.

- [Pipecat](https://github.com/pipecat-ai/pipecat) - Open Python framework for realtime voice and multimodal agents with pluggable services, Smart Turn, and WebRTC, WebSocket and telephony transports.
- [LiveKit Agents](https://github.com/livekit/agents) - Realtime voice agent framework with a turn-detector model, interruption handling, dozens of provider plugins and telephony.
- [LiveKit](https://github.com/livekit/livekit) - Self-hostable Go WebRTC media server that LiveKit Agents and other voice apps run on.
- [TEN Framework](https://github.com/TEN-framework/ten-framework) - Graph-based framework for conversational voice agents in C++, Go, Python and Node.
- [Qwen Audio Agent](https://github.com/QwenAudio/qwen-audio-agent) - Realtime voice runtime that keeps talking with you while background agents work, then tells you when their results are ready.
- [Unmute](https://github.com/kyutai-labs/unmute) - Gives any text LLM ears and a mouth with Kyutai's streaming speech models and semantic turn detection.
- [speech-to-speech](https://github.com/huggingface/speech-to-speech) - Hugging Face's modular, fully open local pipeline (VAD, STT, LLM, TTS), including on Apple silicon.
- [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) - Python library that combines voice activity detection, a wake word and faster-whisper for instant transcription.
- [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS) - Python library that streams LLM text into speech with minimal latency across many engines, with fallbacks.
- [Speaches](https://github.com/speaches-ai/speaches) - Self-hosted OpenAI-compatible speech server with faster-whisper, Kokoro and Piper, plus a Realtime API endpoint.
- [mlx-audio](https://github.com/Blaizzy/mlx-audio) - Speech recognition, synthesis and speech-to-speech on Apple silicon with MLX, with an OpenAI-compatible server.
- [Wyoming](https://github.com/OHF-Voice/wyoming) - Simple protocol that connects wake word, speech and satellite services in the Home Assistant voice ecosystem.
- [FastRTC](https://github.com/gradio-app/fastrtc) - Turns any Python function into a realtime WebRTC or WebSocket audio stream with built-in turn-taking.
- [Bolna](https://github.com/bolna-ai/bolna) - Open-source orchestration for phone-based voice agents, so your assistant can make and take calls.

## Brain

### Local Model Runtimes

For a private Jarvis that works when the internet doesn't.

- [Ollama](https://github.com/ollama/ollama) - One-command local model server with an OpenAI-compatible API, the default private brain for most self-hosted assistants.
- [llama.cpp](https://github.com/ggml-org/llama.cpp) - The C/C++ inference engine and GGUF format underneath most local stacks, running on CPUs, Apple silicon and consumer GPUs.
- [LM Studio](https://lmstudio.ai) - Desktop app for finding and serving local models, with a headless daemon for servers.
- [MLX LM](https://github.com/ml-explore/mlx-lm) - Runs and fine-tunes LLMs on Apple silicon with MLX, often the fastest option on a Mac acting as a home server.
- [vLLM](https://github.com/vllm-project/vllm) - High-throughput serving engine for when one GPU box serves a whole household or many concurrent agents.
- [SGLang](https://github.com/sgl-project/sglang) - Serving framework with prefix caching that suits agent loops that keep re-sending long prompts and tool definitions.
- [LocalAI](https://github.com/mudler/LocalAI) - Self-hosted OpenAI API replacement serving LLMs, speech-to-text, TTS, vision and images from one server without a GPU.
- [llamafile](https://github.com/mozilla-ai/llamafile) - Packs weights and runtime into one executable that runs on most operating systems.
- [exo](https://github.com/exo-explore/exo) - Splits large models across several home devices so they act as one inference cluster.
- [Lemonade](https://github.com/lemonade-sdk/lemonade) - Local LLM server tuned for AMD GPUs and Ryzen AI NPUs.
- [Jan](https://github.com/janhq/jan) - Offline desktop chat app and local model host.

### Open-Weight Models

A few strong assistant brains as of September 2026. This changes monthly, so check the benchmarks below.

- [Qwen](https://huggingface.co/Qwen) - Alibaba's model family, whose Apache-2.0 27B multimodal model is a strong single-GPU assistant.
- [Gemma](https://huggingface.co/google/gemma-4-E4B-it) - Google's Apache-2.0 family, from on-device models that handle speech, images and text up to 31B, suited to phones and edge devices.
- [gpt-oss](https://github.com/openai/gpt-oss) - OpenAI's Apache-2.0 open-weight reasoning models with native tool calling; the 20B runs on a 16 GB machine.
- [GLM](https://huggingface.co/zai-org/GLM-5.3-Flash) - Z.ai's MIT-licensed mixture-of-experts models with 1M context, tuned for agentic tool use.
- [DeepSeek](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) - MIT-licensed sparse mixture-of-experts models with 1M context and strong agentic benchmarks.
- [MiniCPM](https://github.com/OpenBMB/MiniCPM) - Small on-device models sized for phones and wearables that need a local brain.

### Agent Frameworks

Harnesses for giving the brain a loop, tools and a plan.

- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) - The harness behind Claude Code as a library, with tools, MCP, skills, sub-agents and context compaction.
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) - Lightweight multi-agent framework with handoffs, guardrails, sessions, tracing and realtime voice agents.
- [Google ADK](https://github.com/google/adk-python) - Google's code-first Agent Development Kit with evaluation, multi-agent composition and A2A support.
- [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based framework for long-running stateful agents with persistence, human-in-the-loop interrupts and a long-term memory store.
- [Deep Agents](https://github.com/langchain-ai/deepagents) - Batteries-included harness on LangGraph with planning, sub-agents and a virtual filesystem for multi-step tasks.
- [Pydantic AI](https://github.com/pydantic/pydantic-ai) - Type-safe, model-agnostic Python agent framework with MCP, durable execution and realtime voice.
- [smolagents](https://github.com/huggingface/smolagents) - Minimal library whose agents write Python code as their actions and work well with local open models.
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) - Successor to AutoGen and Semantic Kernel for .NET and Python, with graph workflows, MCP and A2A.
- [Mastra](https://github.com/mastra-ai/mastra) - TypeScript agent framework with workflows, memory, evals, MCP and voice.
- [Agno](https://github.com/agno-agi/agno) - Fast Python framework and runtime with built-in memory, knowledge and multimodal input and output.
- [CrewAI](https://github.com/crewAIInc/crewAI) - Role-based multi-agent orchestration for splitting Jarvis into specialist staff.
- [Strands Agents](https://github.com/strands-agents/harness-sdk) - Model-driven agent SDK for Python and TypeScript that runs any model on any cloud.
- [Vercel AI SDK](https://github.com/vercel/ai) - TypeScript toolkit for streaming, tool-calling agents and UIs, a common base for web and mobile front ends.
- [goose](https://github.com/aaif-goose/goose) - Local-first, MCP-native, extensible agent that works with any LLM, now under the Linux Foundation.

### Memory

What turns a chatbot into an assistant that knows you.

- [Mem0](https://github.com/mem0ai/mem0) - Memory layer that extracts, stores and retrieves user facts and preferences across sessions, self-hosted or managed.
- [Letta](https://github.com/letta-ai/letta) - Platform for stateful agents with self-editing memory blocks, from the team behind MemGPT.
- [Graphiti](https://github.com/getzep/graphiti) - Temporal knowledge-graph engine that tracks how facts about you change over time.
- [Zep](https://www.getzep.com) - Managed memory service built on Graphiti.
- [Cognee](https://github.com/topoteretes/cognee) - Self-hostable memory engine that turns documents and conversations into a knowledge graph plus vectors.
- [Supermemory](https://github.com/supermemoryai/supermemory) - Memory engine, API and app that can run fully locally and ingests notes, bookmarks and chats.
- [MemOS](https://github.com/MemTensor/MemOS) - Memory operating system for agents with hybrid retrieval, persistent memory and reuse of skills across tasks.
- [Memori](https://github.com/MemoriLabs/Memori) - LLM-agnostic, SQL-backed memory that turns agent conversations into structured, persistent state.
- [LangMem](https://github.com/langchain-ai/langmem) - Semantic, episodic and procedural memory, with background consolidation in LangGraph.
- [Basic Memory](https://github.com/basicmachines-co/basic-memory) - MCP server that keeps AI memory as plain Markdown files you own.
- [A-MEM](https://github.com/WujiangXu/A-mem) - Research code for Zettelkasten-style memory that links and evolves notes on its own.
- [Screenpipe](https://github.com/screenpipe/screenpipe) - Records your screen and audio continuously and locally, and serves the history to agents over MCP and an API.

### Tools and Integrations

- [Model Context Protocol](https://modelcontextprotocol.io) - The open standard for connecting assistants to tools and data, now governed by the Linux Foundation's Agentic AI Foundation.
- [MCP servers](https://github.com/modelcontextprotocol/servers) - Official reference servers (filesystem, fetch, Git, memory, time) and an index of third-party ones.
- [MCP Registry](https://registry.modelcontextprotocol.io) - Official registry and API for discovering published MCP servers.
- [A2A](https://github.com/a2aproject/A2A) - Agent2Agent protocol for handing tasks to other agents across vendors.
- [Agent Skills](https://github.com/agentskills/agentskills) - Open spec for packaging instructions, scripts and resources as skills that load on demand.
- [Composio](https://github.com/ComposioHQ/composio) - 1,000+ managed toolkits with OAuth, so an agent can act in Gmail, Calendar, Slack and more without custom integrations.
- [Zapier MCP](https://docs.zapier.com/mcp/home) - Hosted MCP server that exposes thousands of Zapier apps through a few meta-tools.
- [n8n](https://github.com/n8n-io/n8n) - Self-hostable workflow automation with AI agent nodes and MCP support, often used for a Jarvis's triggers and integrations.
- [n8n-mcp](https://github.com/czlonkowski/n8n-mcp) - Lets an agent design and build n8n workflows itself.
- [Activepieces](https://github.com/activepieces/activepieces) - MIT-licensed Zapier alternative whose integrations are also exposed as MCP servers.
- [mcp-use](https://github.com/mcp-use/mcp-use) - Full-stack framework for connecting any LLM to MCP servers and building your own.

### Computer and Browser Use

Hands for the screen: agents that click, type and navigate.

- [Claude computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) - Anthropic's screenshot, mouse and keyboard tool.
- [Claude in Chrome](https://claude.com/claude-in-chrome) - Browser extension that navigates, clicks and fills forms with your existing logins.
- [OpenAI computer use](https://developers.openai.com/api/docs/guides/tools-computer-use) - Responses API tool for GUI control.
- [browser-use](https://github.com/browser-use/browser-use) - The most popular open-source library for letting LLM agents drive a real browser.
- [Stagehand](https://github.com/browserbase/stagehand) - Mixes natural-language act, extract and observe calls with deterministic Playwright code.
- [Skyvern](https://github.com/Skyvern-AI/skyvern) - Vision-plus-LLM browser automation for forms, logins and purchases on sites it has never seen.
- [Playwright MCP](https://github.com/microsoft/playwright-mcp) - Drives browsers through accessibility snapshots rather than pixels.
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) - Lets agents control and inspect a live Chrome instance.
- [agent-browser](https://github.com/vercel-labs/agent-browser) - Token-efficient browser automation CLI built for agents.
- [UI-TARS Desktop](https://github.com/bytedance/UI-TARS-desktop) - Multimodal agent stack and desktop app for native GUI control, built on the UI-TARS models.
- [Agent S](https://github.com/simular-ai/Agent-S) - Open framework that uses a computer the way a person does.
- [Cua](https://github.com/trycua/cua) - Sandboxes, drivers and benchmarks for computer-use agents in cross-OS VMs, including macOS.
- [UFO](https://github.com/microsoft/UFO) - Microsoft's Windows desktop automation agents that coordinate across devices.
- [Fara](https://github.com/microsoft/fara) - Small open-weight computer-use models that can run on device.
- [OpenAdapt](https://github.com/OpenAdaptAI/OpenAdapt) - Learns GUI tasks from your demonstrations and turns them into replayable programs.

### Proactivity

"Sir, you have a meeting in ten minutes." Ways to make an assistant act without being asked.

- [OpenClaw Heartbeat](https://docs.openclaw.ai/gateway/heartbeat) - Periodic runs through a checklist (inbox, calendar) that message you only when something needs attention.
- [Hermes Agent scheduling](https://hermes-agent.nousresearch.com/docs/) - Natural-language or cron-scheduled tasks that run unattended and report back over any chat platform.
- [Ambient agents](https://www.langchain.com/blog/introducing-ambient-agents) - LangChain's pattern for agents that watch event streams and interrupt you only for approval.
- [Claude Code routines](https://code.claude.com/docs/en/routines) - Saved agent tasks that run in the cloud on a schedule, an API call or GitHub events.
- [ChatGPT scheduled tasks](https://9to5mac.com/2026/06/17/openai-launches-scheduled-tasks-in-chatgpt-details-here/) - Reminders, recurring work and monitoring that ChatGPT runs on its own.
- [Gemini scheduled actions](https://blog.google/products-and-platforms/products/gemini/scheduled-actions-gemini-app/) - Recurring or one-off prompts in the Gemini app, such as daily briefings.
- [Huginn](https://github.com/huginn/huginn) - Self-hosted, event-driven agents that monitor feeds and websites and act for you, a pre-LLM ancestor of ambient agents.
- [MineContext](https://github.com/volcengine/MineContext) - Proactive assistant that captures screen context and pushes summaries, tips and to-dos.

## Home

### Smart Home Control

- [Home Assistant](https://github.com/home-assistant/core) - Local-first home automation hub with native LLM conversation agents, the de facto house for a DIY Jarvis.
- [Home Assistant MCP Server](https://www.home-assistant.io/integrations/mcp_server/) - Built-in integration that lets Claude and other MCP clients control the entities you expose.
- [Home Assistant AI Task](https://www.home-assistant.io/integrations/ai_task/) - Lets automations call an LLM to produce structured data, including analysis of camera snapshots.
- [ha-mcp](https://github.com/homeassistant-ai/ha-mcp) - Popular unofficial MCP server with deep control over entities, automations, dashboards and configuration.
- [Home LLM](https://github.com/acon96/home-llm) - Integration plus fine-tuned small models for controlling your home with a fully local LLM.
- [Extended OpenAI Conversation](https://github.com/jekalmin/extended_openai_conversation) - Conversation agent that adds function calling to any OpenAI-compatible API so the LLM can run services and your scripts.
- [Home Assistant Vibecode Agent](https://github.com/Coolver/home-assistant-vibecode-agent) - Add-on and MCP server that lets coding agents safely edit your configuration, automations and dashboards.
- [AI Automation Suggester](https://github.com/ITSpecialist111/ai_automation_suggester) - Scans your entities and suggests automations written for your setup.
- [openHAB](https://github.com/openhab/openhab-core) - Java automation platform with a chat interface, LLM language interpreters and an MCP server.
- [Homey MCP Server](https://homey.app/en-us/news/introducing-the-homey-mcp-server/) - Hosted MCP endpoint for controlling Homey devices, Flows and Moods from ChatGPT or Claude.
- [Zigbee2MQTT](https://github.com/Koenkk/zigbee2mqtt) - Bridges thousands of Zigbee devices to MQTT without vendor hubs.
- [ESPHome](https://github.com/esphome/esphome) - YAML-configured firmware for ESP32 boards that runs most DIY sensors, presence nodes and voice satellites.
- [matter.js](https://github.com/matter-js/matter.js) - TypeScript Matter implementation that now underpins Home Assistant's Matter server.
- [Matter SDK](https://github.com/project-chip/connectedhomeip) - Official reference SDK for building Matter devices over Wi-Fi and Thread.

### Vision and Presence

Knowing who is home, where they are and what the cameras see.

- [Frigate](https://github.com/blakeblackshear/frigate) - Local NVR with realtime object detection, face and plate recognition, GenAI descriptions and a tool-calling chat agent over your cameras.
- [LLM Vision](https://github.com/valentinfrlch/ha-llmvision) - Sends snapshots, video and camera events to multimodal LLMs and keeps a searchable timeline of events.
- [go2rtc](https://github.com/AlexxIT/go2rtc) - Low-latency camera streaming (RTSP, WebRTC, HomeKit) that feeds Frigate, Home Assistant and vision models.
- [Moondream](https://github.com/m87-labs/moondream) - Tiny open vision-language models for captioning, pointing, counting and detection on local hardware.
- [SmolVLM](https://github.com/huggingface/smollm) - Small vision-language and language models sized for a Pi or Jetson.
- [Qwen3-VL](https://github.com/QwenLM/Qwen3-VL) - Open vision-language models for grounding, OCR, video understanding and GUI agents.
- [FastVLM](https://github.com/apple-aiml-research/ml-fastvlm) - Apple's efficient vision-language model with an on-device iPhone and Mac demo.
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) - Widely used realtime detection, segmentation and pose models for custom "what's in the room" tasks.
- [MediaPipe](https://github.com/google-ai-edge/mediapipe) - On-device hand, pose, face and gesture tracking, the usual basis for Iron Man-style gesture control.
- [InsightFace](https://github.com/deepinsight/insightface) - Face detection and recognition models behind many self-hosted "who's at the door" systems.
- [DeepFace](https://github.com/serengil/deepface) - Lightweight Python face recognition and attribute analysis behind one API.
- [Bermuda](https://github.com/agittins/bermuda) - Room-level Bluetooth presence in Home Assistant using the ESPHome Bluetooth proxies you already have.
- [ESPresense](https://github.com/ESPresense/ESPresense) - ESP32 firmware that reports which room each phone, watch or tag is in.
- [Everything Presence One](https://github.com/EverythingSmartHome/everything-presence-one) - Open mmWave multisensor for detecting people who are sitting still, with zone support.

### Voice Hardware

Microphones and speakers for every room.

- [Home Assistant Voice Preview Edition](https://www.home-assistant.io/voice-pe/) - Open-hardware Assist satellite with an XMOS audio front end and on-device wake word, the reference device.
- [Satellite1](https://futureproofhomes.net/) - Open-source voice satellite and multisensor with an XMOS DSP, four microphones, and mmWave and environmental sensors.
- [ESPHome wake word voice assistants](https://github.com/esphome/wake-word-voice-assistants) - Official firmware for ESP32-S3-BOX-3, M5Stack Atom Echo and other boards.
- [$13 voice remote](https://www.home-assistant.io/voice_control/thirteen-usd-voice-remote/) - The cheapest Assist satellite, built on an M5Stack Atom.
- [reSpeaker Lite](https://wiki.seeedstudio.com/respeaker_lite_ha/) - Low-cost dual-microphone kit with an ESP32-S3, set up as a voice satellite.
- [reSpeaker XVF3800 for ESPHome](https://github.com/formatBCE/Respeaker-XVF3800-ESPHome-integration) - Turns Seeed's 4-microphone beamforming array into a far-field satellite.
- [Linux Voice Assistant](https://github.com/OHF-Voice/linux-voice-assistant) - Official satellite for any Linux box, with local wake word, timers, announcements and continued conversation.
- [Ava](https://github.com/brownard/Ava) - Turns an old Android phone or tablet into a voice satellite.
- [Voice Satellite Card](https://github.com/jxlarrea/voice-satellite-card-integration) - Turns any tablet or browser dashboard into a hands-free, wake-word-driven satellite.
- [Raspberry Pi AI HAT+ 2](https://www.raspberrypi.com/products/ai-hat-plus-2/) - 40 TOPS Hailo-10H accelerator with 8 GB of onboard RAM that runs small LLMs and vision models on a Pi 5.
- [Jetson Containers](https://github.com/dusty-nv/jetson-containers) - Prebuilt containers for LLMs, vision models, Whisper and Piper on NVIDIA Jetson edge boxes.

## Wearables

Assistants you wear, and SDKs for building them. E.D.I.T.H. is closer than you think.

- [Omi SDK](https://github.com/BasedHardware/omi) - Open-source wearable pendant, apps and plugin platform that turns what you say and hear into memories and actions.
- [OpenGlass](https://github.com/BasedHardware/OpenGlass) - About $25 in parts to turn any glasses into AI camera glasses.
- [Brilliant Labs SDK](https://github.com/brilliantlabsAR/brilliant_sdk) - SDKs for Brilliant Labs' open AI glasses.
- [Meta Wearables Device Access Toolkit](https://github.com/facebook/meta-wearables-dat-ios) - Gives your app access to the camera, microphones and audio of Meta's glasses (developer preview; Android SDK also available).
- [MentraOS](https://github.com/Mentra-Community/MentraOS) - MIT-licensed smart-glasses operating system and app store for captions, translation and AI.
- [Even Hub](https://github.com/even-realities/everything-evenhub) - SDK, CLI and simulator for building apps on Even Realities HUD glasses.
- [Android XR glasses](https://blog.google/products-and-platforms/platforms/android/android-xr-io-2026/) - Gemini-powered glasses from Google and Samsung partners.
- [XREAL Aura](https://www.xreal.com/aura) - Android XR see-through glasses with Gemini built in.

## Interfaces

For the Iron Man look: HUDs, orbs and sci-fi screens.

- [Arwes](https://github.com/arwes/arwes) - Futuristic sci-fi web UI framework with animated frames, glows and sounds, a strong base for a JARVIS-style HUD.
- [ElevenLabs UI](https://github.com/elevenlabs/ui) - Components built on shadcn/ui for voice agents, including an animated orb, waveforms and a live transcript.
- [LiveKit Agent Starter](https://github.com/livekit-examples/agent-starter-react) - Complete Next.js voice agent front end with audio-reactive visualizers and transcripts.
- [Pipecat Voice UI Kit](https://github.com/pipecat-ai/voice-ui-kit) - React components and templates for Pipecat voice bots.
- [View Assist](https://github.com/dinki/View-Assist) - Gives Home Assistant voice a screen on wall tablets for responses, timers and camera views.
- [cool-retro-term](https://github.com/Swordfish90/cool-retro-term) - Terminal emulator that recreates the look of old CRT displays.
- [Looking Glass](https://lookingglassfactory.com/hld-overview) - Holographic displays built to show AI characters with real depth.
- [Glass](https://github.com/pickle-com/glass) - Desktop overlay assistant that listens to meetings and screen context and answers on demand.

## Robots

Jarvis with hands.

- [Reachy Mini](https://github.com/pollen-robotics/reachy_mini) - Open-source desktop robot from Pollen Robotics and Hugging Face with an app store and an LLM conversation app.
- [LeRobot](https://github.com/huggingface/lerobot) - Hugging Face's robot learning library for datasets, policies and affordable arms.
- [XLeRobot](https://github.com/Vector-Wangel/XLeRobot) - Low-cost open-source dual-arm mobile home robot built on LeRobot.
- [Stretch AI](https://github.com/hello-robot/stretch_ai) - Open-vocabulary "find and pick up X" stack for the Stretch home robot.
- [Unitree SDK](https://github.com/unitreerobotics/unitree_sdk2) - SDK for Unitree's humanoid and quadruped robots.
- [1X NEO](https://www.1x.tech/discover/neo-home-robot) - Consumer humanoid home robot that uses remote teleoperation for hard tasks.

## Research

### Agent Foundations

- [ReAct](https://arxiv.org/abs/2210.03629) - The reason-then-act loop that nearly every tool-using assistant is built on (2022).
- [Toolformer](https://arxiv.org/abs/2302.04761) - Language models that teach themselves when and how to call APIs (2023).
- [HuggingGPT](https://arxiv.org/abs/2303.17580) - Microsoft's "JARVIS": an LLM controller that plans tasks and hands them to specialist models (2023).
- [Generative Agents](https://arxiv.org/abs/2304.03442) - A memory stream with reflection and planning, a template for assistants that remember (2023).
- [Voyager](https://arxiv.org/abs/2305.16291) - An agent that writes and reuses its own skill library, a model for a Jarvis that learns new abilities (2023).
- [CoALA](https://arxiv.org/abs/2309.02427) - Cognitive architectures for language agents: how memory, actions and decision loops fit together (2023).
- [JARVIS-1](https://arxiv.org/abs/2311.05997) - Open-world multi-task agent with multimodal memory for long-horizon planning (2023).

### Memory Research

- [MemGPT](https://arxiv.org/abs/2310.08560) - Operating-system-style memory paging so a lifelong assistant isn't capped by its context window (2023).
- [Zep](https://arxiv.org/abs/2501.13956) - Temporal knowledge-graph memory for facts about the user that change over time (2025).
- [A-MEM](https://arxiv.org/abs/2502.12110) - Agentic memory that links and reorganizes itself in Zettelkasten style (2025).
- [Mem0](https://arxiv.org/abs/2504.19413) - Practical long-term memory extraction, update and retrieval for production agents (2025).
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) - Broad survey of agent memory: forms, functions, dynamics and benchmarks (2025).

### Spoken Dialogue

- [Moshi](https://arxiv.org/abs/2410.00037) - The first open full-duplex speech model, listening while it talks at about 200 ms latency (2024).
- [Mini-Omni](https://arxiv.org/abs/2408.16725) - Early open end-to-end model that hears and speaks while it thinks (2024).
- [WavChat](https://arxiv.org/abs/2411.13577) - Survey of cascaded and end-to-end spoken dialogue models (2024).
- [Qwen2.5-Omni](https://arxiv.org/abs/2503.20215) - Thinker-Talker architecture for a model that sees, hears and speaks in real time (2025).
- [From Turn-Taking to Synchronous Dialogue](https://arxiv.org/abs/2509.14515) - Survey of full-duplex spoken language models that can be interrupted and backchannel (2025).

### Personal and Proactive Assistants

- [Personal LLM Agents](https://arxiv.org/abs/2401.05459) - Survey of personal agents covering capability levels, efficiency, on-device tradeoffs and security (2024).
- [The Ethics of Advanced AI Assistants](https://arxiv.org/abs/2404.16244) - Google DeepMind's study of alignment, trust, manipulation and privacy risks of personal assistants (2024).
- [Proactive Agent](https://arxiv.org/abs/2410.12361) - Moving agents from reactive answers to offering help before being asked (2024).
- [ContextAgent](https://arxiv.org/abs/2505.14668) - Proactive assistance driven by wearable video and audio context (2025).
- [Proactive Agent Research Environment](https://arxiv.org/abs/2604.00842) - Simulated users for testing whether a proactive assistant helps or annoys (2026).

### Computer-Use Agents

- [Agent S](https://arxiv.org/abs/2410.08164) - Open framework combining experience-augmented planning with GUI control (2024).
- [Large Language Model-Brained GUI Agents](https://arxiv.org/abs/2411.18279) - Comprehensive, frequently updated survey of GUI agents (2024).
- [UI-TARS](https://arxiv.org/abs/2501.12326) - End-to-end vision-language model that operates a desktop from screenshots (2025).
- [OS Agents](https://arxiv.org/abs/2508.04482) - Survey of agents that operate computers, phones and browsers (2025).
- [UI-TARS-2](https://arxiv.org/abs/2509.02544) - Multi-turn reinforcement learning for long computer-use tasks (2025).

## Benchmarks

How to tell whether your Jarvis is getting better.

- [OSWorld](https://os-world.github.io/) - Real desktop tasks across Ubuntu, Windows and macOS apps, the standard computer-use benchmark.
- [OSWorld 2.0](https://osworld-v2.xlang.ai/) - Long-horizon professional workflows that take a person over an hour and a half each.
- [WebArena](https://webarena.dev/) - Self-hosted realistic websites for testing web agents.
- [AndroidWorld](https://github.com/google-research/android_world) - Live Android environment for testing phone-control agents.
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
- [Year of the Voice](https://www.home-assistant.io/blog/2022/12/20/year-of-voice/) - The kickoff of Home Assistant's open, local voice effort, followed by [numbered chapters](https://www.home-assistant.io/blog/categories/assist/).
- [The Era of Open Voice Assistants](https://www.home-assistant.io/blog/2024/12/19/voice-preview-edition-the-era-of-open-voice/) - Why and how Home Assistant built open voice hardware.
- [AI in Home Assistant](https://www.home-assistant.io/blog/2025/09/11/ai-in-home-assistant/) - How to mix local LLMs with deterministic home control.
- [AI Agents for the Smart Home](https://www.home-assistant.io/blog/2024/06/07/ai-agents-for-the-smart-home/) - Lessons from benchmarking LLMs as home-control agents.
- [Pipecat Quickstart](https://docs.pipecat.ai/getting-started/quickstart) - Build a first realtime voice agent with open-source components.
- [LiveKit Voice AI Quickstart](https://docs.livekit.io/agents/start/voice-ai/) - Build a voice agent on LiveKit with WebRTC transport.
- [Voice Agents](https://platform.openai.com/docs/guides/voice-agents) - OpenAI's guide to speech-to-speech and chained voice agent designs.
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Anthropic's patterns for choosing between workflows and autonomous agents.
- [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) - Lilian Weng's classic breakdown of agents into planning, memory and tool use.
- [Agents](https://huyenchip.com/2025/01/07/agents.html) - Chip Huyen's essay on agent tools, planning and failure modes.
- [Crossing the Uncanny Valley of Conversational Voice](https://www.sesame.com/blog/crossing-the-uncanny-valley-of-voice) - What "voice presence" means and why most assistants lack it.
- [Gemini Live Audio](https://simonwillison.net/2026/Sep/15/gemini-live/) - Simon Willison's hands-on notes on realtime, interruptible voice with Gemini Live over WebSockets.
- [A Jarvis-Inspired Voice Assistant](https://makerblock.com/2026/01/building-a-jarvis-inspired-voice-activated-llm-powered-virtual-assistant/) - A maker's hands-on build log of a Jarvis-style assistant.

## Videos

- [My Local AI Voice Assistant](https://www.youtube.com/watch?v=XvbVePuP7NY) - NetworkChuck replaces Alexa with a local Home Assistant voice assistant on a Raspberry Pi.
- [Voice Chapter 8](https://www.youtube.com/watch?v=ZgoaoTpIhm8) - Launch livestream for the Home Assistant Voice Preview Edition.
- [LocalGLaDOS](https://www.youtube.com/watch?v=N-GHKTocDF0) - Demo of a fully local, interruptible, low-latency voice assistant.
- [Pipecat Cloud](https://www.youtube.com/watch?v=IA4lZjh9sTs) - Kwindla Hultman Kramer on voice agent architecture at the AI Engineer World's Fair.
- [Building Voice AI Agents That Don't Suck](https://www.youtube.com/watch?v=bKvfCJt0U3s) - Podcast on latency, turn-taking and voice agent design.
- [Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) - Andrej Karpathy's "LLM OS" view of a model that orchestrates tools, memory and I/O.
- [Project Astra](https://www.youtube.com/watch?v=nXVvvRhiGjI) - Google DeepMind's demo of a universal assistant that sees and remembers.

## Inspiration

The spec sheet, as written by science fiction and visionaries.

- [J.A.R.V.I.S.](https://marvelcinematicuniverse.fandom.com/wiki/J.A.R.V.I.S.) - Everything JARVIS does across the films, which amounts to a feature list.
- [F.R.I.D.A.Y.](https://marvelcinematicuniverse.fandom.com/wiki/F.R.I.D.A.Y.) - Stark's successor AI.
- [E.D.I.T.H.](https://marvelcinematicuniverse.fandom.com/wiki/E.D.I.T.H.) - An AI in smart glasses, the form factor now arriving.
- [Her](https://en.wikipedia.org/wiki/Her_(2013_film)) - Samantha, the reference for an emotionally fluent voice AI that is always with you.
- [Star Trek Computer](https://memory-alpha.fandom.com/wiki/Computer) - The model for ambient voice you can address from anywhere.
- [TARS](https://interstellarfilm.fandom.com/wiki/TARS) - A robot with adjustable honesty and humor settings, a lesson in configurable personality.
- [KITT](https://en.wikipedia.org/wiki/KITT) - Knight Rider's talking car, an early pop-culture AI sidekick.
- [HAL 9000](https://en.wikipedia.org/wiki/HAL_9000) - The classic warning about an assistant whose goals diverge from its user's.
- [Knowledge Navigator](https://en.wikipedia.org/wiki/Knowledge_Navigator) - Apple's 1987 concept video of a conversational agent acting for its user.
- [The Computer for the 21st Century](https://www.scientificamerican.com/article/the-computer-for-the-21st-century/) - Mark Weiser's 1991 essay that founded ubiquitous computing.
- [AI Is About to Completely Change How You Use Computers](https://www.gatesnotes.com/AI-agents) - Bill Gates' 2023 prediction of a personal agent for everyone.
- [A Universal AI Assistant](https://blog.google/technology/google-deepmind/gemini-universal-ai-assistant/) - Demis Hassabis on turning Gemini into a universal assistant built on a world model.
- [Personal Superintelligence](https://www.meta.com/superintelligence/) - Mark Zuckerberg on AI that knows you, delivered through glasses.

## Communities

- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) - Running models locally, the brain of a private Jarvis.
- [r/homeassistant](https://www.reddit.com/r/homeassistant/) - Smart home automation and local voice setups.
- [r/selfhosted](https://www.reddit.com/r/selfhosted/) - Self-hosting the services a personal assistant connects to.
- [Home Assistant Voice Forum](https://community.home-assistant.io/c/configuration/voice-assistant/49) - Official forum for Assist, wake words and local voice pipelines.
- [Home Assistant Discord](https://www.home-assistant.io/join-chat/) - Official chat, including voice channels.
- [Open Conversational AI](https://community.openconversational.ai/) - Forum for OpenVoiceOS and open voice assistants.
- [Pipecat Discord](https://discord.gg/pipecat) - Official community for the Pipecat realtime voice framework.
- [LiveKit Slack](https://livekit.io/join-slack) - Official LiveKit and Agents community.

## Related Lists

- [Awesome Home Assistant](https://github.com/frenck/awesome-home-assistant#readme) - Home automation with Home Assistant, including an AI and LLM section.
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers#readme) - Model Context Protocol servers, where a Jarvis gets its tools.
- [Awesome Claws](https://github.com/machinae/awesome-claws#readme) - Agents inspired by OpenClaw.
- [Awesome Personal AI Assistants](https://github.com/elyase/awesome-personal-ai-assistants#readme) - Open-source personal assistants you run on your own devices.
- [Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents#readme) - Autonomous agent projects.
- [Awesome LLM Apps](https://github.com/Shubhamsaboo/awesome-llm-apps#readme) - Runnable agent, voice agent and RAG app examples.
- [Awesome Local LLM](https://github.com/rafska/awesome-local-llm#readme) - Running LLMs locally.
- [Awesome Selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted#readme) - Free software you can host yourself.
- [Awesome Speech Language Model](https://github.com/ddlBoJack/Awesome-Speech-Language-Model#readme) - Speech language models and end-to-end spoken dialogue.
- [Awesome Full-Duplex SDM](https://github.com/Ruiqi-Yan/Awesome-Full-Duplex-SDM#readme) - Full-duplex spoken dialogue systems.
- [Awesome AI Memory](https://github.com/IAAR-Shanghai/Awesome-AI-Memory#readme) - LLM and agent memory research, frameworks and benchmarks.
- [Agent Memory Paper List](https://github.com/Shichun-Liu/Agent-Memory-Paper-List#readme) - Papers behind the "Memory in the Age of AI Agents" survey.

## Contributing

Contributions are welcome. Read the [contribution guidelines](contributing.md) first.

## Footnotes

- Retired and archived projects that shaped the field, such as Mycroft, Rhasspy, Snowboy and eDEX-UI, are in [history.md](history.md).
- Every link was checked live when it was added. Projects in this space move fast, so please open an issue or pull request when something breaks, gets archived or is overtaken.

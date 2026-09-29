# The Jarvis Lab

Scripts, images and configs for testing voice agents hands-on, the practical companion to the [testing methodology](../methodology.md). It is the lab behind the September 2026 results in [testing.md](../testing.md), cleaned up so it runs from any checkout. Follow the [lab rules](RULES.md) when you use it.

The lab feeds speech into a **virtual microphone**, records what the agent says from a **virtual speaker**, transcribes it, and screenshots the agent's visual state. Nothing needs a physical mic, speaker or display, so an AI agent can drive most of it.

It was built on an Apple silicon Mac mini (M4, 32 GB, macOS 26). The Docker images are arm64; the VM tracks need Apple silicon.

```
lab/
  README.md, RULES.md
  lab.sh               Docker driver: build / up / test / shell / down
  login-claude.sh      Claude subscription login into the shared lab volume (prints only the URL)
  login-codex.sh       Codex CLI device-code login into the shared lab volume
  base/                jarvis-lab-base: Ubuntu 24.04 + audio graph + displays + STT/TTS + Codex and Claude Code CLIs
  hey-jarvis/          jarvis-lab-omarchy: Arch Linux ARM "Omarchy-like" image for the hey-jarvis plugin
  omarchy-m/           jarvis-lab-omarchy-m: real Omarchy 4 installed by Omarchy Mac's own installer
  paseo/ hermes/ openclaw/ happy/   one image per agent, built on base or on the agent's official image
  drivers/             long-lived browser driver (pw-driver) and multi-step voice-turn scripts
  omarchy-vm/          Omarchy M's ARM64 VM image under QEMU + HVF: real Hyprland
  macos/               disposable macOS VM (Tart) + guest tools (audio, TCC, screenshots)
  android/             Android emulator drivers (UI, audio over gRPC, Chrome DevTools)
  voice-server/        free local stand-in for OpenAI's Realtime and audio APIs (MLX)
  patches/             one-line URL patches and the TapQ build patch, with what each changes
  evidence/            curated transcripts, logs and screenshots behind testing.md
```

Everything the lab creates locally (evidence in `out/`, SSH keys, VM disks, venvs, model caches, sockets) is git-ignored. Set `LAB_OUT` to put evidence somewhere else.

## Tracks: Which One to Use

| Track | Use it for | Real display stack | Notes |
|---|---|---|---|
| **Docker** (`lab.sh`) | Linux agents, servers and web UIs: Paseo, Hermes Agent, OpenClaw's gateway, Happy's CLI, hey-jarvis's pipeline | Xvfb (X11) and headless sway (Wayland) | Fastest to rebuild. No GPU, so no Hyprland. |
| **Omarchy VM** (`omarchy-vm/`) | Omarchy and Hyprland plugins: hey-jarvis, omavoice, omarchy-voice | Real Hyprland on a virtio GPU, software rendered | The only way to see Hyprland-specific behaviour (focus, layer stacking, idle lock). |
| **macOS VM** (`macos/`) | Mac apps: OpenClaw's Mac app, TapQ, usejarvis, JARVIS for Claude Code, Hermes desktop | The guest's real GUI session | Grants privacy permissions by writing TCC databases; only in a throwaway VM. |
| **Android** (`android/`) | Android apps and mobile web clients: Operit, Happy | Emulator (swiftshader) | Microphone input was not solved in the reference lab; see the pitfalls. |
| **Local voice server** (`voice-server/`) | Any agent that expects OpenAI's Realtime or speech APIs | n/a | Runs natively on the Mac; reachable from every other track. |

iOS apps would use Xcode's iOS Simulator; the reference lab couldn't get it running (see the pitfalls).

## Prerequisites

On the host Mac, with [Homebrew](https://brew.sh):

| For | Install |
|---|---|
| Docker track | [Docker Desktop](https://www.docker.com/products/docker-desktop/), with about 8 GB of memory for its VM and 60 GB of disk for all images |
| macOS VM | `brew install cirruslabs/cli/tart expect` (and about 60 GB of disk for the Cirrus Labs base image) |
| Omarchy VM | `brew install qemu` (provides `qemu-system-aarch64` and the UEFI firmware) |
| Android | `brew install --cask android-commandlinetools` and `brew install openjdk@17`, then Python 3.12 with `grpcio grpcio-tools protobuf faster-whisper websocket-client` |
| Local models | [Ollama](https://ollama.com) (the app or `brew install ollama`), then `ollama pull qwen2.5:7b-instruct-q4_K_M` and a small model such as `qwen3:4b-instruct-2507-q4_K_M` |
| Local voice server | `brew install uv` and Python 3.12 (`brew install python@3.12`) |

Run VM, emulator and voice-server commands from a normal terminal, not from inside an agent's sandbox: Tart and QEMU need the Virtualization and Hypervisor frameworks, MLX needs Metal, and the scripts use `launchctl`.

## The Shared Tooling

Every environment gets the same small toolkit, so a test script reads the same everywhere.

| Command | Docker (`/lab/bin`) and Omarchy VM (`~/.local/share/jarvis-lab/bin`) | macOS VM (`~/lab/bin`) |
|---|---|---|
| Speak into the mic | `say [--speaker] [--keep f.wav] "text"` (Piper `en_US-lessac-medium`, 0.3 s lead-in) | `say-mic "text"`, `play-mic f.wav`; or from the host `macos/speak.sh "text"` |
| Record the agent | `record-out <seconds> <f.wav>` (what the agent plays) | `record-out <seconds> <f.wav>` |
| Record the mic | `record-mic <seconds> <f.wav>` (what the agent hears) | `record-mic <seconds> <f.wav>` |
| Transcribe | `transcribe f.wav` (faster-whisper `base.en`, CPU int8) | `transcribe f.wav` (whisper.cpp `base.en`) |
| Screenshot | `shot [--x11\|--wayland] f.png` (grim or ffmpeg x11grab) | `macos/vm.sh shot NAME` from the host |
| Prove the loop | `lab-selftest [dir]` | `lab-selftest [dir]` |

**The audio graph (Linux).** PulseAudio in the Ubuntu images, PipeWire with pipewire-pulse on Arch and in the Omarchy VM, built the same way with `pactl`:

```
speaker   null sink, the default sink      -> speaker.monitor         (record-out)
vmic_in   null sink that `say` plays into  -> vmic_in.monitor -> vmic  (the default source: "the microphone")
```

ALSA is routed to Pulse, so PortAudio and `sounddevice` apps and Chromium all open `vmic` as their microphone. `lab-selftest` checks three things with no model: a phrase spoken into the mic transcribes exactly, a phrase played to the speaker transcribes exactly, and the mic stays silent while the speaker plays.

**The audio graph (macOS).** [BlackHole](https://existential.audio/blackhole/) 2ch is the default input (the mic) and BlackHole 16ch the default output (the speaker); `sox -t coreaudio` plays into one and records from the other. `audio-route` sets the routing and `lab-selftest` proves it.

**Android.** `android/emu_audio.py` streams the emulator's audio output over its gRPC API and can inject audio into its mic; see the Android pitfalls before relying on injection.

Look at every screenshot you cite. Name evidence by agent and step, for example `paseo/step2-agent-speech.txt`.

## Model Access

The rules are in [RULES.md](RULES.md#model-access); this is how the lab implements them.

- **Subscription through the official CLI, one login for the whole lab.** `login-claude.sh` signs the official Claude Code CLI in to your Claude subscription inside a lab container. The login lives only in the Docker volume `jarvis-lab-claude` (mounted at `/lab-claude` with `CLAUDE_CONFIG_DIR=/lab-claude`) and never touches the host's `~/.claude` or Keychain. Containers that mount the volume share it, one at a time. `login-codex.sh` does the same for the Codex CLI with the volume `jarvis-lab-codex`.
- **Sharing the login into VMs.** `macos/share-claude-login.sh` and `omarchy-vm/share-claude-login-vm.sh` copy it from the volume into a VM over SSH stdin without printing it. See their headers for exactly what they copy. If you'd rather not share, `macos/login-claude-macos.sh` and `omarchy-vm/login-claude-vm.sh` start a separate login in the guest and print only the sign-in URL; feed the one-time code with `--code-file FILE`.
- **Local models.** Ollama on the host, reached from Docker at `http://host.docker.internal:11434/v1`, from the Omarchy VM at `http://10.0.2.2:11434/v1`, from the Android emulator at `http://10.0.2.2:11434/v1` and from the macOS VM at the host's address on Tart's network (`macos/vm.sh host-ip`). Ollama inside a VM is much slower than on the host.
- **BLOCKED.** When a hallmark needs a paid key the tester doesn't have, the lab records BLOCKED and scores that hallmark from code.
- **Local OpenAI-compatible voice.** For agents that expect OpenAI's Realtime or speech APIs, run the [local voice stack](#local-openai-compatible-voice-stack) and give the agent the dummy key `sk-local-dummy` (it is not a real key; the local servers ignore it).

### Security Trade-offs of the Shared Login

Be clear about what you're accepting before you use the credential helpers:

- The OAuth credentials sit in plaintext in the `jarvis-lab-claude` volume, readable by root in any container that mounts it. Agents under test run in those containers.
- The macOS helper copies only the access token (about eight hours), but exports it with `launchctl setenv`, so every app started in the guest's GUI session can read it. Start agents that shouldn't see it with `env -u CLAUDE_CODE_OAUTH_TOKEN`.
- The Omarchy VM helper copies the full credential, including the refresh token. Two copies that both refresh can invalidate each other; re-share or log the guest in on its own when that happens.
- Anyone with a copy can use your subscription until it expires. Use disposable VMs, keep one container on the volume at a time, and sign out (`claude auth logout` in a lab container) when you're finished.
- Some agents will adopt a Claude Code login they can see and call Anthropic's API directly while presenting themselves as Claude Code. The Hermes image prevents that by running Claude Code as a separate user that alone can read the volume ([hermes/claude-isolation](hermes/claude-isolation/)). Check each new agent for the same behaviour.

## Quick Start: Docker

```bash
cd lab
./lab.sh build base            # then: ./lab.sh build all (NO_CACHE=1 for a clean build)
./lab.sh up base && ./lab.sh test base          # model-free self-test
./lab.sh up paseo && ./lab.sh test paseo        # first start downloads ~1 GB of speech models into a volume
./lab.sh shell paseo                            # a shell inside jl-paseo
./lab.sh down paseo                             # removes the container, keeps images and volumes
```

Targets: `base`, `omarchy` (hey-jarvis on an Omarchy-like Arch image), `omarchy-m` (real Omarchy 4, 12.8 GB, about 9 minutes to build), `paseo`, `hermes`, `openclaw`. Happy has its own driver: `./happy/lab-happy.sh build|up|auth|sessions|show|down`. Run one target at a time on an 8 GB Docker VM. Inside a container, `eval "$(lab-env)"` sets up `DISPLAY`, `WAYLAND_DISPLAY` and the Pulse socket for `docker exec` shells.

Then sign in once, from any running container:

```bash
./login-claude.sh jl-paseo                         # prints the sign-in URL; approve it in a browser
./login-claude.sh jl-paseo root --code-file code.txt   # the one-time code, read from a file
```

### Driving Agents with Claude Code

The `test` targets are model-free smoke tests. The full hands-on runs used Claude Code through the shared login; these are the settings that made each agent use it:

- **Paseo.** `paseo daemon config set features.voiceMode.llm.provider claude`, `daemon.mcp.injectIntoAgents true` (so the voice agent can create, list and kill agents), and `agents.providers '{"claude":{"env":{"IS_SANDBOX":"1","CLAUDE_CONFIG_DIR":"/lab-claude"}}}'`, then `paseo restart`. `IS_SANDBOX=1` is needed because Paseo always launches Claude Code with a skip-permissions flag, which Claude Code refuses as root; the agent still runs in the mode you pick. Start a voice host with `paseo run --provider claude --mode default --title voice-host "Reply with exactly: ready"`.
- **OpenClaw.** Set `agents.defaults.model.primary` to an `anthropic/` model with `agentRuntime.id` `claude-cli` (OpenClaw then runs the Claude Code executable and never reads the tokens), run `openclaw models auth login --provider anthropic --method cli`, and `openclaw exec-policy preset cautious` (the default runs shell commands with no approval). Restart the container afterwards.
- **Hermes Agent.** Keep its brain local (Ollama through a `custom` provider), set `auth.adopt_external_logins false` and `approvals.mode manual`, and let it reach Claude Code only through the `claude` wrapper. `hermes/bin/hermes-lab-voice-setup` configures local speech, Piper and the "hey hermes" wake word.

`drivers/pw-driver.mjs` keeps a headed Chromium open (Xvfb, with the virtual mic) behind a tiny local HTTP API, so a test can speak, click and screenshot across many steps while a voice session stays open. Copy it and `drivers/pw` into a container, start `node pw-driver.mjs <url>` with `docker exec -d`, then call `pw goto p=/`, `pw click name=REGEX`, `pw shot f=/lab/out/x.png`, `pw buttons`, `pw text`. `drivers/paseo-bargein.sh` and `drivers/hermes-voice-turn.sh` are complete multi-step voice turns built on it.

## Quick Start: Omarchy VM

Omarchy M's generic ARM64 image ([riverscn/omarchy-aarch64-image](https://github.com/riverscn/omarchy-aarch64-image) v4.0.3-virt.1) under Homebrew QEMU with Apple's hypervisor, headless. Hyprland runs on a virtio GPU with Mesa llvmpipe: real Hyprland, software rendered.

```bash
cd lab/omarchy-vm
./vmctl fetch        # ~3.7 GB, checks the release's pinned SHA-256s, extracts the disk
./vmctl start        # boots headless; QMP and the guest agent on sockets in run/
```

First boot runs Omarchy's owner wizard on the console. Drive it with `./vmctl shot now.png` (look at it), `./vmctl type 'text'` and `./vmctl key ret`. Pick an owner name (the scripts default to `lab`; set `OMARCHY_VM_USER` otherwise) and a password, and save that password on the first line of `ssh/lab-password` (git-ignored; `OMARCHY_VM_PASSWORD_FILE` to move it). Then:

```bash
./vmctl provision    # sshd on, port 22 open in Omarchy's firewall, lab SSH key, guest tools + audio graph
./vmctl login        # types the password into the SDDM greeter, waits for Hyprland
./vmctl ssh 'omarchy toggle idle stay-awake'     # keep the idle lock from blanking the display
./vmctl ssh '~/.local/share/jarvis-lab/bin/lab-selftest ~/lab-out'
./vmctl ssh '~/.local/share/jarvis-lab/bin/jarvis-vm-e2e ~/e2e "what is the capital of France" 60'
./vmctl pull e2e ../out/omarchy-vm/
./vmctl stop
```

Install plugins the way a user would, for example `omarchy plugin add https://github.com/Atzingen/hey-jarvis --enable`. The guest reaches the host's Ollama and voice server at `10.0.2.2`. Use `./share-claude-login-vm.sh` or `./login-claude-vm.sh` for Claude. `./vmctl utm` builds a UTM bundle from the same verified release if you want GPU-accelerated Hyprland (virtio-gpu-gl) from a session that can drive UTM.

## Quick Start: macOS VM

A throwaway VM from Cirrus Labs' [macOS base images](https://github.com/cirruslabs/macos-image-templates): SIP disabled, passwordless sudo, and SSH granted Full Disk Access, which is what lets the lab write privacy grants.

```bash
cd lab/macos
./vm.sh create                              # clone + 4 CPU / 8 GB / 100 GB (LAB_MACOS_IMAGE to pin a digest)
./vm.sh start                               # headless; installs a lab SSH key using the image's default password
./vm.sh ssh 'mkdir -p ~/lab' && ./vm.sh put guest-bin lab/bin && ./vm.sh put guest-setup.sh guest-setup.sh
./vm.sh ssh 'bash guest-setup.sh'           # Homebrew tools, BlackHole, whisper.cpp + model, Claude Code (pinned)
./vm.sh ssh 'source ~/lab/bin/lab-env; lab-selftest "/Volumes/My Shared Files/out/selftest"'
./speak.sh "hey openclaw what time is it" utt1   # host TTS -> guest mic
./vm.sh shot NAME                           # -> out/macos/NAME.png
./vm.sh stop                                # keeps the VM
```

`../login-claude.sh` a container first, then `./share-claude-login.sh` gives the guest's `claude` CLI the lab login (see the trade-offs above), and `guest-bin/claude-lab-wrapper` covers apps that strip `CLAUDE_CODE_*` from child processes. Don't run interactive `claude` in the guest (it starts onboarding); use `claude -p`. Configs used in the reference run are in [configs/](macos/configs/): `hermes.yaml` restricts Hermes desktop to a local model, `usejarvis.yaml` uses only keyless providers.

**Privacy permissions (TCC).** Voice apps need Microphone, Speech Recognition, Accessibility and Screen Recording:

1. `tcc-grant <App.app|bundle id|path> Microphone SpeechRecognition Accessibility ScreenCapture ...` writes rows into both TCC databases with the app's code-signing requirement, then restarts `tccd`. It's the technique Cirrus Labs uses to build its images; it works because sshd has Full Disk Access. MDM profiles can't grant Microphone or Screen Recording.
2. The macOS 15+ **replayd** alert ("X is requesting to bypass the system private window picker and directly access your screen and audio") is not a TCC row. `screencap-approve <bundle id or executable path>` pre-seeds `ScreenCaptureApprovals.plist` (replayd is stopped first, because it rewrites the file from memory). A pre-seed only sticks if replayd hasn't cached the client yet; otherwise `approve-prompts` clicks Allow once and it persists.
3. Anything else (Local Network prompts, first-run dialogs): `approve-prompts` clicks Allow or OK through System Events and prints what it approved.

Launch GUI apps with `open` (or `gui open ...`), not from the SSH shell, so TCC attributes them to their own bundle instead of `sshd-session`. `vm.sh shot` goes through the Tart guest agent because approvals for `sshd-session` never persist. Enable Dictation (`defaults write com.apple.assistant.support "Dictation Enabled" -bool true`) before testing apps that use `SFSpeechRecognizer`, and grant `AppleEvents:com.google.Chrome` before scripting Chrome. `chrome-lab URL` starts Chrome with remote debugging on port 9222 and mic prompts auto-accepted; `cdp 'python'` runs a Playwright snippet against it.

## Quick Start: Android

```bash
cd lab/android && . ./env.sh
sdkmanager "platform-tools" "emulator" "system-images;android-35;google_apis;arm64-v8a"
avdmanager create avd -n jarvis-android -k "system-images;android-35;google_apis;arm64-v8a" -d pixel_7
mkdir -p grpc && python3 -m grpc_tools.protoc -I "$ANDROID_SDK_ROOT/emulator/lib" --python_out=grpc \
  --grpc_python_out=grpc "$ANDROID_SDK_ROOT/emulator/lib/emulator_controller.proto"   # stubs for emu_audio.py
./emu-start.sh          # headless, gRPC on 8600, blocks until booted
python3 ui.py dump      # also: ui.py tap "Text", ui.py type "text", ui.py wait "Text", ui.py shot out.png
python3 emu_audio.py record 30 out.wav && python3 emu_audio.py transcribe out.wav
./emu-stop.sh           # keeps the AVD
```

The reference AVD used 4 GB, 4 cores, 720x1600 at 320 dpi and swiftshader. `anr-waiter.sh` answers "Wait" on ANR dialogs while a starved emulator catches up. For web clients (Happy's is `https://app.happy.engineering`), `adb forward tcp:9333 localabstract:chrome_devtools_remote`, then `cdp.py text` or `cdp.py eval '<js>'`. Install APKs from the project's GitHub releases and check the published digest before `adb install`.

## Local OpenAI-Compatible Voice Stack

Many voice agents speak OpenAI's Realtime API. `voice-server/` runs a free replacement natively on the Mac with MLX:

| Server | Endpoints | Behind it |
|---|---|---|
| **realtime**: [Hugging Face speech-to-speech](https://github.com/huggingface/speech-to-speech) at `87725778` | `ws://HOST:8765/v1/realtime` (Realtime GA), `POST /v1/realtime/calls` (WebRTC) | Silero VAD + Smart Turn, Parakeet TDT 0.6B v3, an Ollama model (default `qwen2.5:7b-instruct-q4_K_M`), Kokoro-82M |
| **audio**: [mlx-audio](https://github.com/Blaizzy/mlx-audio) 0.5.6 + `bin/audio_serve.py` | `POST http://HOST:8766/v1/audio/transcriptions`, `POST /v1/audio/speech`, `GET /health` | Parakeet (speech-to-text), Kokoro (speech); ffmpeg from the pinned `imageio-ffmpeg` 0.6.0 wheel |

```bash
cd lab/voice-server
./voicectl setup        # two Python 3.12 venvs from requirements-*.lock.txt (exact versions of the reference run)
./voicectl start        # both servers; first start downloads ~3 GB of models into local/hf
./voicectl status ; ./voicectl logs realtime 80 ; ./voicectl stop
```

The servers run as transient launchd jobs (nothing is installed in `~/Library/LaunchAgents`), bind `127.0.0.1` and have **no authentication**. Docker reaches them at `host.docker.internal`, the Omarchy VM at `10.0.2.2`; for the macOS VM set `VOICE_HOST` to the host's address on Tart's network. Options: `VOICE_LLM_MODEL`, `VOICE_DEFAULT_VOICE`, `VOICE_RT_ARGS="--no_smart_turn"`, `VOICE_OFFLINE=1`. Memory: about 3.6 GB for realtime, 1 GB for audio, plus the Ollama model.

`bin/s2s_serve.py` wraps the stock server with seven lab patches, each for a gap a real client hit:

1. OpenAI voice names (`marin`, `cedar`, ...) are mapped to Kokoro voices (`bin/voicemap.py`).
2. Long speech inputs are split into sentences, so the first audio doesn't wait for the whole paragraph (4.5 s down to 1.8 s).
3. `turn_detection.create_response=false` is honoured, for clients that send `response.create` themselves.
4. One extra prompt rule: an acknowledgement must be followed by the tool call. Small local models otherwise say "one sec" and stop (tool calls went from 6 of 9 to 9 of 9 with the 7B model).
5. `input_audio_buffer.clear` and `conversation.item.delete` are accepted instead of rejected.
6. Client-chosen item ids are accepted.
7. The model request timeout is 90 s instead of 20 s (`VOICE_LLM_TIMEOUT`), for clients with very large prompts.

`bin/audio_serve.py` maps OpenAI model and voice names, defaults to OpenAI's response formats and adds `pcm`, `opus`, `aac` and `flac` output. `bin/rest_probe.py` (stock `openai` SDK) and `bin/realtime_probe.py` (raw Realtime client that paces a mic in real time; scenarios `turn`, `bargein`, `cancel`) produced the results in [evidence/voice-server](evidence/voice-server/). Its utterances are 24 kHz mono WAVs, for example `say -o q1.wav --data-format=LEI16@24000 "What is the capital of France?"`.

Example, OpenClaw's browser Talk through its gateway relay (inside `jl-openclaw`; undo with `openclaw config unset talk.realtime`):

```bash
openclaw config set talk.realtime '{"provider":"openai","transport":"gateway-relay","model":"gpt-realtime-2.1",
  "providers":{"openai":{"apiKey":"sk-local-dummy","azureEndpoint":"http://host.docker.internal:8765"}}}' --strict-json
```

Reference results: about 1.1 to 1.5 s from the end of speech to the first audio (1.0 s without Smart Turn), barge-in and `response.cancel` both pass. Whether an agent can use it depends on whether its OpenAI address is configurable; the table is in [testing.md](../testing.md#local-voice-instead-of-paid-keys), and the one-line patches are in [patches/](patches/).

## Adding a Test for a New Agent

1. **Pick the track** from the table above by the platform the agent targets.
2. **Add the environment.** For Docker, create `lab/<agent>/Dockerfile` `FROM jarvis-lab-base:latest` (or the agent's official image plus the lab's `base/bin` and `base/etc`, as `hermes/` and `openclaw/` do). Pin the agent's version or digest, add a start script to `<agent>/bin/`, then add the target to the `dockerfile`, `up` and `test_target` functions in `lab.sh`. For the VMs, install it inside the guest the way its README says and record the commit or version.
3. **Prove the loop first.** Run `lab-selftest` in the environment before involving any model.
4. **Wire model access** through the official CLI with the shared login, or a local model. Check whether the agent reads other tools' logins, and turn that off.
5. **Script each step of the [hands-on test script](../methodology.md#hands-on-test-script).** A typical voice step is: start `record-out` in the background, `say` the wake word and the request, wait for the agent's turn to end, screenshot, then `transcribe` the recording. `hey-jarvis/bin/jarvis-smoketest`, `omarchy-vm/guest/jarvis-vm-e2e` and `drivers/hermes-voice-turn.sh` are good templates.
6. **Save evidence** under `out/<agent>/`, named by step, and look at every screenshot.
7. **Record the result** as described in [methodology.md](../methodology.md#recording-results). Stop what you started.

## Pins

| Thing | Pin |
|---|---|
| Ubuntu / Arch Linux ARM base images | `ubuntu:24.04@sha256:008173c2…`, `menci/archlinuxarm:base-20260926.36223892169@sha256:30546b37…` |
| Node / uv | 22.23.3 (SHA-256 checked) / 0.12.19 |
| Codex CLI / Claude Code | 0.157.1 / 2.1.283 |
| piper-tts / faster-whisper | 1.8.0 / 1.2.1; Piper voice `en_US-lessac-medium` at rhasspy/piper-voices `39ab474b…` (SHA-256 checked) |
| hey-jarvis | `d6ebaa6ca0097082480d9486d8219c7a98be041f` (stable, manifest 2.4.0) |
| Omarchy (quattro) / Omarchy Mac | `c5b4db77…` / `ba546a61…` (4.0.3rc4) |
| Paseo / Playwright | `@getpaseo/cli@0.9.2` / 1.63.0 |
| Hermes Agent image | `nousresearch/hermes-agent:v2026.9.24@sha256:fca358f1…` |
| OpenClaw image | `openclaw/openclaw:2026.9.6-browser@sha256:62832668…` |
| Happy CLI | `happy@1.2.5` |
| Omarchy VM image | riverscn/omarchy-aarch64-image v4.0.3-virt.1 (SHA-256s in `omarchy-vm/vmctl`) |
| macOS VM image | `ghcr.io/cirruslabs/macos-tahoe-base@sha256:1b093499…` (macOS 26.6.2) |
| Android | emulator 37.1.11, `system-images;android-35;google_apis;arm64-v8a` r9 |
| Voice server | speech-to-speech `87725778`, mlx-audio 0.5.6, full lock files in `voice-server/` |

The full digests are in the Dockerfiles and scripts. Rolling package repositories (Arch, Omarchy's) can't be pinned; `omarchy-m` records what it installed in `/usr/share/omarchy-m-lab/packages.txt`.

## Known Pitfalls

**Host**
- **VMs started from an agent's shell can run about 20 times slower.** They inherit background CPU priority and land on efficiency cores. `vmctl` and `voicectl` start their processes as transient launchd jobs with `ProcessType Interactive` for this reason.
- **Oversubscription kills guests.** With every VM, the emulator and Docker running at once, the reference host swapped 10 to 12 GB and Android's watchdog killed `system_server` repeatedly. Run one heavy track at a time.

**Docker**
- **Hyprland needs a GPU device.** Docker Desktop's VM has no DRM device and no vkms, and Hyprland has no software-only backend, so it can't start (`evidence/lab-selftest/hyprland-in-docker-probe.txt`). The images fall back to headless sway, which speaks the same layer-shell protocol, so Quickshell windows and bars still render. Use the Omarchy VM for anything Hyprland-specific.
- Arch Linux ARM in Docker needs pacman's `DisableSandbox*` options, `ldconfig` after installs, and `setcap -r /usr/bin/sway` (sway's `cap_sys_nice` makes exec fail in a container).
- There's no systemd user session, so small shims stand in for `systemctl --user`, `systemd-run`, `journalctl`, `notify-send`, `uwsm-app` and friends (`hey-jarvis/shims`, `omarchy-m/shims`). A recreated OpenClaw container may report "Another Gateway owner lease is still active" for up to five minutes.

**Omarchy VM**
- **Omarchy's idle lock** blanks the display after five minutes and makes `grim` hang. Turn on stay-awake while testing.
- Only the first boot auto-logs in; later boots stop at the SDDM greeter (`vmctl login`). Omarchy's firewall drops the forwarded SSH port until `ufw allow 22/tcp` (`vmctl provision` does it).
- An echo canceller on a null-sink graph can deliver pure silence. For full-duplex barge-in tests, add a null sink with `device.form_factor=headphone` and record its monitor.

**macOS VM**
- **VPIO returns silence from BlackHole.** Apps that capture with voice processing (AVAudioEngine `setVoiceProcessingEnabled`) can't be voice-tested with a virtual mic; `guest-bin/live-stt.swift vp` reproduces it.
- replayd approvals for `sshd-session` never persist; screenshot through `tart exec`. The display is 1024x768 points regardless of `tart set --display`.
- An `osascript` that drives another app hangs on a hidden Automation prompt until you grant `AppleEvents:<bundle id>` with `tcc-grant`.

**Android**
- **The emulator's microphone** needs the host's microphone permission, which an agent-launched emulator doesn't have ("coreaudio: Could not initialize record"). The gRPC `injectAudio` path then crashed the emulator as soon as an app held the mic. To test voice: launch the emulator once from Terminal and grant it the mic, install BlackHole as the default input and play into it, or use a physical phone.
- `-no-window -gpu host` renders only black frames; use swiftshader.

**iOS**
- Xcode 27's `simctl` required a newer CoreSimulator than the system had, so every call tried `xcodebuild -runFirstLaunch`, which needs an admin. Run `sudo xcodebuild -runFirstLaunch` yourself first.

**Models and agents**
- **Small local models** often narrate tool calls instead of making them. Use a 7B or larger instruction-tuned model before blaming the agent.
- **Shared logins expire.** Access tokens last about eight hours; refresh the shared login before a long run. An expired login in one VM blocked a delegation test in the reference run.
- Several agents default to skipped or automated approvals (see [testing.md](../testing.md#findings)). Claude Code 2.1.283 itself defaults to an "auto" mode that approves low-risk actions, so a missing approval prompt isn't always the agent's doing.

## Cleanup

```bash
./lab.sh down all
docker volume rm jarvis-lab-paseo-models jarvis-lab-hermes-data jarvis-lab-openclaw-data jarvis-lab-happy-home
docker volume rm jarvis-lab-claude jarvis-lab-codex        # after signing out; this deletes the shared logins
docker rmi jarvis-lab-openclaw jarvis-lab-hermes jarvis-lab-paseo jarvis-lab-happy jarvis-lab-omarchy-m jarvis-lab-omarchy jarvis-lab-base
tart delete jarvis-macos
rm -rf omarchy-vm/qemu omarchy-vm/dl omarchy-vm/run voice-server/local out
```

The lab is released under the repository's [CC0 license](../license).

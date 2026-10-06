# Shared voice service

Persistent, authenticated access to the lab's existing Apple MLX speech stack. Application tests reserve the service, use their short-lived key, and release it. They must not stop its processes. This is shared infrastructure, not a Jarvis application or a phone UI.

## Orca deployment

Installed 2026-10-05 on Orca (M4, 32 GB). Private endpoint:

`https://chriss-mac-mini.tail3127c0.ts.net:8443`

Tailscale Serve terminates HTTPS; it is available inside the tailnet, not through Funnel. Backends bind only to loopback: gateway 18800, realtime 18765, STT/TTS 18766, dedicated Ollama 18768. The dedicated model process shares the existing model cache but does not own the host's other Ollama process.

The installation lives in `~/Library/Application Support/JarvisVoice`, outside thread storage. It has versioned releases, copied pinned Python environments/model cache, a `current` symlink, private credentials, and bounded rotating logs. The existing lock files pin the speech dependencies; the realtime source pin is `87725778a0eb736306e8b8ccdfd3ac4ab82c1503`. Hugging Face model downloads are disabled; the existing durable home-directory Torch and NLTK caches are also reused. Model: `qwen2.5:7b-instruct-q4_K_M`; STT: Parakeet TDT 0.6B v3; TTS: Kokoro 82M.

**Startup limitation:** `com.jarvislab.voice-service` is a user LaunchAgent with RunAtLoad and KeepAlive. It starts at user login and recovers process crashes. Startup before login, a host reboot, and recovery after power loss have not been verified. A system LaunchDaemon needs Orca administrator access; the installer does not silently enable autologin or change host security. Orca currently has automatic restart after power failure disabled.

## Reserve, use, release

Run the administrative client on Orca. Its master credential is `~/Library/Application Support/JarvisVoice/admin.key` (0600). Never give that credential to an application under test. Only the reservation key belongs in the test's OpenAI-compatible API-key setting.

```sh
VOICE_HOME="$HOME/Library/Application Support/JarvisVoice"
CLIENT="$VOICE_HOME/current/managed/client.py"
python3 "$CLIENT" status
python3 "$CLIENT" --base https://chriss-mac-mini.tail3127c0.ts.net:8443 \
  reserve --owner project-thread --ttl 900 --out /private/tmp/project-voice-session.json
python3 "$CLIENT" renew --session /private/tmp/project-voice-session.json --ttl 900
python3 "$CLIENT" release --session /private/tmp/project-voice-session.json
```

The session JSON is created exclusively with mode 0600 and contains `api_key` and `base_url`. Read it inside the client process; do not print it or put the key in command-line arguments. Renew/release use its saved endpoint unless `--base` overrides it. A remote lab VM can receive only this session file through authenticated SSH; alternatively, forward the gateway through SSH. Do not expose the raw backend ports to the LAN. Remove the private session file after release.

Supported endpoints, authenticated with `Authorization: Bearer <reservation key>`:

- `POST /v1/audio/transcriptions`: multipart OpenAI audio request.
- `POST /v1/audio/speech`: OpenAI speech request.
- `wss://…/v1/realtime`: Realtime WebSocket, including browser `realtime` / `openai-insecure-api-key.<key>` subprotocols.
- `GET /v1/realtime/calls/{id}`: authenticated status for an owned call; 200 while active, 404 after the backend releases it. Applications can reconcile an abandoned local call before retrying.
- `POST /v1/realtime/calls`: raw `application/sdp`; configure the session over its data channel. Hang up with `DELETE` on the returned relative Location, or `POST <Location>/hangup`.

Cross-origin browser fetches are not enabled. An application should proxy SDP requests through its own authenticated backend and keep the master credential off the browser. WebRTC media needs peer network reachability; HTTPS signaling alone does not provide a TURN relay.

Capacity is one reservation and one realtime session. REST audio runs serially and is rejected while realtime is active or its cleanup is uncertain. Lease lifetime is 30–900 seconds and can be renewed. Expiry closes the call and reclaims the worker. Before admitting another call or REST audio operation, the gateway reconciles an uncertain setup and clears stale call bookkeeping only after the backend reports idle. A failed cleanup retains capacity and returns an error; it never silently assigns a busy worker. Another reservation gets HTTP 409; missing, revoked, or expired keys get 401. A gateway restart invalidates leases and reconciles orphaned calls before admitting work. Reacquire a reservation after restart.

Requests are bounded to 8 MiB; speech input to 4,000 characters; model IDs to the installed speech models and documented aliases. Reserve roughly 12 GiB of host memory for warmed voice/model workloads; this is an operational budget, not a macOS hard memory limit. The service admits only one caller and one loaded LLM. Other host model processes can independently consume memory. Do not co-schedule memory-heavy VMs without checking host pressure.

## Operations

`GET /healthz` returns only `{ "ok": true }` or HTTP 503. `client.py status` gives authenticated component health and reservation ownership. Administrative recovery of an abandoned reservation is `client.py force-release`; it terminates that caller's audio.

The supervisor restarts failed children, probes health every 30 seconds after a 150-second warmup allowance, and restarts a child after three failed probes. launchd restarts a failed supervisor. Logs are in `$VOICE_HOME/logs`, at most four 5 MiB files per logger. They can contain speech transcripts; the installation directory and log files are private. Access logs at the gateway are disabled, and keys are never deliberately logged.

To update after releasing active calls, run `install.py` from the checkout with the copied runtime's Python. It creates a versioned release and reloads the owned LaunchAgent. Existing reservations are invalidated. Keep prior releases for investigation; each release's `pins.json` hashes its requirements. Copy the previous release's source into a checkout and run the installer to roll back; do not repoint `current` alone because the process configuration contains release paths.

Initial installation requires `runtime/s2s-venv`, `runtime/mlx-audio-venv` and `runtime/hf`, prepared by `../voicectl setup` and warmed with the pinned models, then copied to the durable service directory. Invoke the copied `bin/python` directly because copied venv console scripts can retain old shebangs. The base Homebrew Python and Ollama binary must remain installed. Back up configuration, deployment source/locks and the private credential separately; model caches can be recreated.

```sh
"$VOICE_HOME/runtime/s2s-venv/bin/python" lab/voice-server/managed/install.py
# Private TLS, persistent across tailscaled restarts:
tailscale serve --bg --https=8443 http://127.0.0.1:18800
# Maintenance only, after checking reservations:
launchctl bootout "gui/$(id -u)/com.jarvislab.voice-service"
# Restore the installed job:
launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.jarvislab.voice-service.plist"
```

For tests, set `VOICE_SESSION_FILE` to the private session JSON when running `../bin/rest_probe.py` or `../bin/realtime_probe.py`. Set `VOICE_AUDIO_BASE` for REST and pass the WebSocket URL explicitly. These probes retain dummy-key support for a separately owned transient server.

Deployment validation and limitations: [2026-10-05 evidence](../../evidence/voice-service/README.md).

The WebRTC wrapper emits `output_audio_buffer.started`, `cleared`, and `stopped` from response-owned PCM buffers and track drain. Generation completion alone does not mean playback finished. Reliability fixes and live integration evidence: [2026-10-06 audit](../../evidence/opendots/integration-audit/README.md).

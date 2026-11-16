# November 16 continuation — remaining runtime checks

This continuation runs in the disposable Linux guest on Otter against the authorized Mac Ollama and permanent Pocket services. Failed tests are completed observations; they are not left waiting for an upstream fix. The broader campaign remains governed by the remaining-test matrix.

## Newelle 1.6.1 permission and task controls

Official Flathub artifact, commit `1757d6512b513a8ee521d0db42311db57087ef004e45beaf1c0fe7423f9e3d81`; upstream release source `902809fb8dc8ec484687fc57f81ca17e431841fb`. Actual GTK application ran under Xvfb/Openbox and DBus with separate PulseAudio microphone and speaker sinks. Its supported Ollama and compatible speech adapters used the real lab services, with Qwen3 and Alfred. Declared Ollama and GUI API runtime dependencies were installed into the app's normal pip directory; source was unchanged. File access was scoped to the task workspace/output, and auto-run stayed false.

| Check | Observed result |
|---|---|
| Pending file-write request | File independently absent while the native Run/Skip card waited |
| Native Skip | PASS: actual command result says skipped and the file remained absent |
| Native Run | PASS: the requested file appeared with exact expected contents only after Run |
| Voice Mode task request | Real microphone input was transcribed and the model requested `execute_command`, action `start`, command `python3 worker.py`. Native permission card appeared; worker remained absent |
| Spoken choices at the waiting card | Inputs did not resolve the card. There were no application microphone streams in this waiting state. Separate yes/no fixture transcriptions were correct; the combined actual microphone control only transcribed the denial, so it does not independently establish the full yes input. No spoken-approval pass is claimed |
| Spoken Stop after explicit manual Run | Worker remained alive and heartbeat bytes grew15→195 |
| Native Voice Mode cancel while worker ran | FAIL for task cancellation: same independently identified guest worker survived at0,1,3,5seconds; heartbeat bytes grew195→345, without a natural-completion marker. Harness then terminated that exact worker |
| New work after cancellation | PASS for continued use: another native Run approval produced the exact recovery file |

See [manual permission effects](newelle-manual-permissions.json), [voice/control observations and qualifications](newelle-voice-controls.json), and [verified cleanup](newelle-cleanup.json). The fixture was bounded to90seconds and refused duplicate execution. Its container PID was not used for verification or cleanup: the observer matched the actual guest PID, command and workspace directory. A stopped surface alone was not accepted as task cancellation.

These results are scoped to the tested native Voice Mode and manual controls. Earlier classic wake/STT/reply and delayed acoustic-stop observations remain separately documented; this does not certify every voice route. The minimal guest also emitted document-portal, hardware ALSA, realtime-service and GTK markup warnings. The actual command and microphone paths were exercised despite those warnings; they are not treated as candidate-wide failures.

Afterward the app, worker and two owned audio sinks were absent; the original settings were restored and read back. Task API/lease credential files were removed, the Pocket lease was released, and the private evidence archive was copied outside the VM. Stable services were unchanged. No full-test scorecard date is refreshed from this scoped result alone.

## AIRI 0.15.4 native qualification

The current official amd64 Debian release was installed and checksum verified (`5859a23585e524acd4215277b17967efe78e02d3b11b68585a17c0d40963173b`). These results belong to0.15.4, separately from the earlier0.15.2 observations. The unmodified Electron app ran with its normal sandbox under Xvfb/Openbox and SwiftShader. The avatar rendered with ghosting in this virtual graphics setup. A task microphone used a PulseAudio remapped source, separate from the captured speaker sink.

| Check | Observed result |
|---|---|
| Native onboarding/model discovery | PASS: stock Ollama setup discovered six actual cached models; selected Qwen2.5 7B |
| Analytics default and saved choice | Default was on. Switched the actual combined analytics/error-report control off; off persisted after native process restart |
| Native chat after restart | PASS: prior chat persisted and a new question visibly answered “Two plus two is four.” First visible answer after46.08seconds; actual streaming local model request returned200 |
| Native speech preview with Pocket/Alfred | HTTP200 audio/pcm, but the actual HTML audio element reported demuxer error4. Isolated16.35-second speaker recording was silent |
| Main Speech module and real chat reply | Selected the stock compatible provider in the actual module. A new visible answer generated a real Pocket speech request, HTTP200 audio/pcm. The separate64.39-second speaker recording was silent, with an empty independent transcript |
| Hearing module | PASS: actual native microphone streams, volume-based detection and stock compatible STT produced “Computer, what is the capital of France?” in the Hearing screen. Independent microphone recording transcribed the same words |
| Always-on/automatic-send attempt | No new local STT/model request or new chat message observed within120seconds after opening floating chat and injecting the question. This separate attempt lacked a simultaneous microphone control recording; no full-loop or universal voice-failure claim |
| Computer-use request | Native Use computer control was selected. Model replied “Let's see what we can find out!” but no actual tool result, AUV process or computer-use store was observed. No desktop-task, approval or worker-cancellation pass |
| Independent speaker-route control | PASS: speech injected into the same speaker sink recorded peak18823/RMS1957.46 and independently transcribed the intended control phrase. The silent application recording is distinct from a failed observer route |

See [sanitized native case results](airi-native-cases.json). Both preview and runtime requested Pocket without a `response_format`; this is compatibility evidence for these stock adapters, not a claim about all AIRI voice providers. No CORS proxy or application-source change was used for the native tests. Barge-in cannot pass from silent playback.

New external flows by the guest application user were blocked while testing the default privacy setting; model and speech used the real services through loopback SSH forwards. A blocked vendor feature-flags request was observed. Firewall counters are not attributed solely to analytics, and neither vendor delivery nor payload contents are certified. Sentry IPC events alone do not establish external delivery. The first pre-restart question had no observed answer for several minutes; the cause remains unresolved. A small direct endpoint control answered quickly, but its prompt was substantially smaller than AIRI's39,720-byte native request, so those latencies are not equivalent workloads.

Native processes and all three task audio modules were verified absent afterward. The task profile, including cached leased API keys, and guest/local lease files were removed; the Pocket lease was released. The exact AIRI firewall table was removed while preserving the existing OpenJarvis privacy guard. The13.3MB private evidence archive was exported outside the VM and hashed. No shared service configuration changed.

## OpenJarvis desktop-managed Linux backend

Official desktop1.0.5 now exercised its own backend installation/start path with port8000 initially empty. The source checkout was pinned to `13706f2b5b5ba6cac9ad31bc575d9e115213784f`. Native onboarding selected its custom OpenAI-compatible server option against the real Mac Ollama endpoint and cached Qwen2.5 model, without starting a guest Ollama daemon.

The first attempt correctly reported missing Rust `cargo`. Installed the official checksum-verified Rustup bootstrap and declared Rust1.89.0 inside the guest, then retried. The desktop actually ran `uv sync` with its desktop/cloud/native dependency groups and compiled the native Rust extension. A second setup attempt exposed a path mismatch introduced by the harness's isolated `XDG_DATA_HOME`: the desktop wrote `~/.openjarvis/config.toml`, while the backend resolved its config through the XDG directory. Explicitly aligning them with supported `OPENJARVIS_HOME` resolved that attempt; no application source was changed.

The desktop then launched its own actual API child (`uv run jarvis serve`), with process ancestry independently verified, and `/health` returned200. Selected Qwen2.5 through the actual model menu and submitted a factual question through the visible Send button; the native chat answered “Four.” The UI reported1.5seconds and engine Ollama. This establishes desktop-managed Linux installation, startup and native conversation; it does not qualify a real LM Studio server, Windows installer, or native frontend speech. Stock speech health reported faster-whisper available and TTS unavailable; those probes do not establish microphone capture or audible playback.

Chose **Continue without sharing** at the actual giveaway/analytics dialog. The real analytics destination remained guest-firewall blocked; no external delivery is claimed. Native app/Openbox stopped, the prior guest config was restored, and three owned XDG profiles/password files were removed. The managed API children survived external native-process SIGTERM; the harness independently matched and terminated those exact children, then verified port8000 closed. This external termination is separate from a native Stop Backend control test.

See [startup, setup qualifications, observed reply and cleanup](openjarvis-managed-desktop.json). The private10.5MB evidence archive is retained outside the VM with a SHA256 manifest. Shared services were unchanged.

## Newelle managed subagent follow-up

A separate native test created a configured subagent through Newelle's supported API, then requested it from the actual chat UI. The model invoked `run_subagent`; the native widget showed the named subagent and its nested command approval. The actual worker and heartbeat were absent while that card waited. Clicking Run started the independently identified worker. Native Stop left it alive at0,1,3,5seconds, with heartbeat bytes growing2→23 and no natural-completion marker. The harness then terminated that exact worker. Thus the direct-command cancellation failure also reproduces in a real managed subagent; cooperative source cancellation does not establish termination of this running command. See [independent observations](newelle-subagent-controls.json). Original settings were restored/read back, the app and task sinks were absent afterward, and raw evidence was exported outside the guest.

## Paseo 0.15.4 native voice correction

Official npm Paseo0.15.4 and official Codex0.167.2 ran in the disposable Linux guest with subscription authentication explicitly authorized by Chris. The actual Chromium UI used GPT-5.6-Sol and real PulseAudio microphone/speaker routes, with permanent Pocket/Alfred through the stock compatible providers. A typed reply and chat persistence after restart passed.

The earlier missing-speak-tool observation was configuration-specific: enabling supported MCP injection exposed the real speak tool. Local turn detection with remote speech also required the supported local models-directory setting. Browser microphone permission grants proved connection-scoped; corrected tests kept one continuous debugger connection and confirmed an actual Chromium capture stream before injecting speech. Attempts with no active stream are inconclusive observer failures.

In the original **Auto-review** mode, the independent microphone recording transcribed “Computer, what is the capital of France?” and the speaker recording transcribed “The capital of France is Paris.” No approval click was needed. Auto-review persisted after native restart. A subsequent count-and-interrupt attempt independently captured the complete interruption/new question, but the speaker transcript contained counting only and no new native question/answer appeared within25seconds. This does not establish a complete barge-in exchange.

In stricter **Default permissions**, the actual speak tool required an Accept/Deny card. Recognized spoken yes/no became new chat turns instead of resolving that card. Manually accepting speech produced a recorded spoken acknowledgement; that click is explicit in the evidence. During a separate manually accepted count, acoustic interruption led to a native Four speech request, but another card blocked playback. These mode-specific results do not mean all speech requires clicks. Earlier independently verified manual file approve/deny effects and surviving Codex subprocess after Stop remain valid.

See [sanitized setup, mode-specific cases and independent transcripts](paseo-native-voice.json). Owned processes, ports6767/9224 and three audio modules were absent afterward. The copied guest Codex authentication, task browser profile, password and lease copies were removed; the Pocket lease was released. Host authentication was unchanged. Raw recordings/screenshots/logs were exported outside the guest with a SHA256 manifest.

## OpenJarvis packaged desktop speech

Official desktop1.0.5 used the pinned backend13706f2 and real Mac Ollama/Pocket. Supported speech config and short-lived lease enabled stock OpenAI STT; the only backend source adaptation changed the hardcoded TTS URL to Pocket, as allowed by the methodology. Actual Speech settings initially had dictation, read-aloud and autoplay off; enabled them through the native UI.

The native microphone button displayed **Microphone access denied** without creating an application capture stream. Installed and verified the guest's real GStreamer PulseAudio source plugin, then retried: same visible result. A separate recording from that exact virtual microphone route independently transcribed the full injected France question, so the input route worked; native microphone access remains unqualified in this environment. No security-disable flag or application permission bypass was used.

After a confirmed typed question and actual Send click, native chat visibly answered “The capital of France is Paris.” The real speech route returned200; the64.15-second speaker recording independently transcribed the same sentence (peak18677/RMS354.76). Simultaneous microphone capture was silent, verifying no speaker leakage. The selected UI model was Qwen3 4B through real Ollama's compatible API, despite the setup screen's retained Qwen2.5 default and LM Studio adapter label. A prior typing/focus attempt never submitted a chat request; its silent capture is an observer failure, not an application playback failure.

See [actual settings, transcripts, route controls and cleanup](openjarvis-native-speech.json). Original TTS source bytes and prior config were restored; candidate git status was clean. Owned native/backend roots, API port and three audio modules were absent; task keyring/password/guest lease copies were removed and the Pocket lease released. Raw evidence was exported and hashed outside the guest. This establishes typed-question→native spoken output with the disclosed URL change; it does not establish native microphone conversation, wake, spoken interruption or Windows support.

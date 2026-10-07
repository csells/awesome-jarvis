# Release re-tests — 2026-10-06

These are scoped release re-tests, not a claim that every provider, device or hallmark passed. The September results remain historical evidence; the coverage below is the current run.

## Environment

Paseo 0.10.3 (`b4af508e2a9e5a34a8b0ffb8dfaff6fd679da6c7`) ran in a disposable Debian 13 VM on the Bumble home-lab worker, with Node 24.8.0, Chromium/Playwright, PulseAudio virtual microphone/speaker and the official Codex CLI 0.156.1 using existing subscription authentication. The model was the provider's default GPT-6-Astra. Default permissions stayed enabled.

usejarvis brain 0.15.0 (`cd52a5eafd777287088461bc3bcbd2e84d9dacbe`) and published sidecar 0.9.7 ran in a disposable macOS 26.6.2 Tart VM on Orca. BlackHole provided the microphone/speaker. The shared Ollama model was `qwen2.5:7b-instruct-q4_K_M`; speech output used free Microsoft Edge TTS. Telemetry and brain awareness were disabled for the test; their default policy was not changed upstream. The project's insecure setup option was enabled in the disposable guest. Clients used an SSH loopback forward, but the brain listener bound all guest interfaces; this is not a hardened deployment configuration.

Chris explicitly authorized using the existing shared host model and voice runtimes. Apps, state and test workspaces stayed inside the disposable VMs. The shared service was reserved with its lease protocol; its installation was not modified. No new paid API key was required.

## Integration details that matter

- Paseo's supported `daemon.mcp.injectIntoAgents` setting had to be enabled. Without it, the transcript reached Codex but `speak` was unavailable.
- Selecting local turn detection alone did not construct Paseo's local-provider configuration. Setting `PASEO_LOCAL_MODELS_DIR` enabled its bundled Silero detector. STT/TTS used the shared authenticated OpenAI-compatible endpoints, with `whisper-1`, `tts-1`, `alloy` and 24 kHz PCM output.
- usejarvis's local STT client does not send an Authorization header. A small, VM-local loopback proxy added the leased service credential. It did not change the app or shared service. Its generic local STT option works independently of the hosted Usejarvis AI service; generic OpenAI-compatible TTS was not substituted.
- The repository's sidecar npm manifests still say 0.1.0. That old published binary lacks the native pebble capability. The current independently released 0.9.7 package contains `Jarvis.app`; launching that bundle and accepting macOS microphone consent was necessary.

## Paseo results

| Check | Result | Evidence / limit |
|---|---|---|
| Real agent task | PASS | Official Codex created a session and answered the initial task. |
| Spoken question → agent → speaker | PASS | Browser microphone input was transcribed; after clicking the Codex MCP approval, captured speaker audio independently transcribed as “Seven plus five is twelve.” |
| Interruption and follow-up | PASS | A distinct eSpeak input voice interrupted counting at 21; the captured reply then said “stopped.” The first attempt used the same synthesized voice as output and was not detected during playback. Browser echo cancellation is a plausible explanation, not a proven project defect. |
| Spoken delegation | PASS | A real Codex child created the file `proof` containing exactly `ready`. Its card and the sub-agent count appeared in the UI. An earlier spoken filename was mistranscribed; the child faithfully wrote the wrong filename/content. |
| Spoken approval | FAIL in this configuration | “Yeah, approve the pending request” became a new user message. The agent replied that it could not see a pending approval, and another `speak` approval card remained. |
| Process cancellation | FAIL with Codex | Two real stop probes returned `INTERRUPTED` while the Python subprocess remained alive. In the first, it wrote `cancel-test-finished` five seconds after the stop response. The second remained alive three seconds after stop and wrote its completion file about 36 seconds after stop. An agent becoming idle is not proof its work stopped. |
| Other permission/cancellation paths | Not certified | This run does not establish spoken denial or spoken cancellation of a running child. Repeated `speak` approvals already prevent a fully hands-free default-Codex workflow. The September Claude results do not establish current Codex behavior. |

Only expected speech requests were approved by the test driver. Those clicks are disclosed assistance, not a hands-free pass. The child's workspace write was allowed by Codex's configured workspace permissions. One overlapping-client run was invalidated when an older test's cleanup interrupted its child; the successful artifact check was repeated after the earlier client closed.

Paseo's oversight score is reduced to partial. It moves from Mission Control to Jarvis Agents because voice and visual remain full; the current tested Codex cancellation path does not meet the full oversight bar. This is a result for this app/provider pairing, not an attribution of the underlying defect to one codebase.

## usejarvis results

| Check | Result | Evidence / limit |
|---|---|---|
| Wake, transcription, spoken reply | PASS | Native sidecar recognized the wake phrase; local STT reached the brain; the answer to seven plus five was spoken through the native playback device. A separate long-reply speaker recording was independently transcribed. |
| Response latency | Poor in this setup | Observed first-audio delays were about 71–90 seconds, dominated by local-model processing. STT took roughly 0.1–0.4 seconds; first TTS synthesis roughly 0.6–1.0 seconds. This is an app/model configuration result, not a speech-service latency claim. |
| Wake-word interruption during speech | FAIL | A timed wake phrase and stop/new-question input were played after the long reply was queued. Playback continued. The normal wake handler exits while `pendingSummons` owns a response, and that response holds the slot through estimated playback completion. Keyboard/manual interruption and the separate realtime mode are different paths and are not certified here. |
| Spoken delegation | PASS, with model errors | The request spawned a real Research Analyst and returned its comparison. The model first omitted a required tool parameter, then corrected it. |
| Later turns / permission and cancel workflow | Not certified | The 7B model repeatedly reused the earlier delegation request, made malformed tool calls and gave stale responses to later questions. No successful spoken approval, denial or child cancellation is claimed. Its default command-execution policy still does not ask for approval. |
| Visual | Partial re-verification | Native pebble state changes were observed. Full per-agent progress and every state were not re-certified in this release run. |

The voice score is reduced to partial because the observed normal wake-word pipeline did not interrupt speech. The earlier visual/oversight scores remain supported by the historical lab and source; this re-test does not relabel those old results as new passes.

## OpenVision promotion review

Pinned source: `1d5d9203a36f76040947425a603eba57757eac75`. Two independent source reviews, followed by the actual simulator build/launch attempt, support keeping it on the Watch List.

Source rubric: voice 2, hands-free 2 **conditionally through the Hermes Dashboard bridge**, visual 1, oversight 1. Its orb/transcript/tool status is not a multi-agent work dashboard; a single remote agent is not fleet supervision. Hermes API-key mode does not supply the Dashboard approval bridge. Interruption depends on the wake phrase. The license is MIT. No iPhone-camera fallback implementation was found despite the setup documentation's claim; phone microphone/speaker fallback is separate.

The unchanged source built with Xcode 27.0 and the iPhone 18 Pro / iOS 27 Simulator. Two lab setup issues were corrected first: use a concrete simulator destination without forcing `-sdk iphonesimulator` onto host macros, and install Xcode's MetalToolchain component. No source patch or dependency exclusion was used.

Launch with the repository's example configuration failed twice. Unbuffered output records:

```text
[OpenVisionApp] Failed to configure Wearables SDK: WearablesError(rawValue: 0)
[OpenVisionApp] Initialized
MWDATCore/Wearables.swift:236: Fatal error: Call `configure()` before attempting to access Wearables!
```

The app catches configuration failure and then unconditionally constructs `GlassesManager` with `Wearables.shared`. A working phone-only startup path was not established. This is an observed launch failure with example settings, not proof that valid Meta credentials would fix the simulator, and not a voice-quality failure. Conversation, physical glasses, remote Hermes approval/cancel and on-device model inference remain BLOCKED by startup.

Other source caveats: optional telemetry is off by default; Keychain write failure can retain secrets in the JSON settings file; the OpenClaw transport permits plaintext HTTP/WebSocket and puts a bearer token in a query parameter; voice-confirmed `/yolo` and `/approvals` commands can change remote policy. The repository does not commit its resolved Swift dependency versions.

**Decision: remain on the Watch List.** Maintainer activity alone does not satisfy the hallmark or runtime bar. Revisit after phone-only startup and camera documentation are corrected and a configured end-to-end run is available.

## Evidence and validation

Raw recordings, screenshots, runtime logs and process timing records are retained in private thread storage. They are not included in this public repository.

Audio fixtures were synthetic and routed through virtual devices. These checks exercise actual microphone capture, agent execution and speaker playback in the VMs; they do not establish physical-room acoustics, mobile hardware or glasses behavior. Full build logs and uncompressed recordings were exported before guest teardown.

The second Paseo cancellation probe ran a foreground Python process that slept 45 seconds before writing a completion file. The stop returned successfully while that process was alive. It remained alive three seconds later and wrote the completion file approximately 36 seconds after the stop response. The first independent probe also wrote its completion file after stopping the agent.

Repository validation ran in the disposable Linux VM: all 47 unit tests and Awesome lint passed. No application source was changed.

The successful OpenVision build command (after `xcodegen generate` and installing MetalToolchain) was:

```sh
xcodebuild -project OpenVision.xcodeproj -scheme OpenVision \
  -configuration Debug \
  -destination 'platform=iOS Simulator,id=5EF59E63-5AE2-427E-B280-B1D3438E25C0' \
  -derivedDataPath build/DerivedData \
  -skipPackagePluginValidation -skipMacroValidation CODE_SIGNING_ALLOWED=NO build
```

The package plugin was inspected before allowing execution. This simulator build does not validate device signing or physical Meta hardware.

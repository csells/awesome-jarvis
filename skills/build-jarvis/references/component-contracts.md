# Component and provider contracts

## Verify the intersection

Record exact versions of the application, provider plugin, agent CLI/adapter, speech endpoint, model, device OS and artifact. Compare engine/runtime requirements with the actual installation. Pin immutable source and checksummed binaries where available; preserve lockfiles. An upstream `@latest` launcher can change underneath a pinned parent application.

Use current official documentation and the actual native request path to build an interface matrix:

| Boundary | Required observations |
|---|---|
| Capture → recognition | PCM/container, sample rate, channels, byte order, chunk duration, buffering, authentication, request-size limit |
| Recognition → talker | Partial/final transcript semantics, turn ID, language, cancellation and timeout behavior |
| Talker → synthesis | Model/voice identifiers, text limits, requested format, streaming or buffered response, cancellation |
| Synthesis → player | MIME/container/codec, sample rate, browser/native decoder, routing, queue drain and completion callback |
| Realtime socket | Protocol generation, event names, audio input/output formats, VAD, tools/results, error/terminal events, authorization |
| Talker → worker | MCP/ACP/app-server or job API, cwd, environment, process ownership, streaming status, approvals and cancellation |
| Tool → real service | Correct endpoint/account, least-privilege identity, rate limits, idempotency, response schema and evidence |

“OpenAI-compatible” is a starting hypothesis. Separate chat completions, Responses, HTTP transcription, HTTP speech, Realtime WebSocket and WebRTC. Separate HTTP STT/TTS do not by themselves supply a Realtime conversation service. A working text model says nothing about microphone transport or playable synthesis. A Realtime adapter's model label may describe its wire format rather than the actual local backend.

Probe the actual client-produced audio container through the native adapter before claiming input compatibility. A WAV fixture can pass while the browser's WebM/Opus upload fails. Preserve the original payload class and sanitized upstream status, then test any bounded conversion with the same real input; repeat the actual microphone flow afterward.

Validate base-URL composition through observed requests: duplicate `/v1`, an omitted path prefix, a wrong route or a content-type mismatch can produce confusing failures. HTTP 200 with raw PCM can still fail a player expecting a WAV/MP3 container. Match both parties deliberately. First run a small direct endpoint control, then the actual application adapter; retain the distinction if only the control passes.

## Authentication and installed providers

Prefer a native provider CLI, supported OAuth/app-server/ACP integration, or an approved local model service. Subscription login is not automatically an API subscription. CLI authentication does not sign a browser into a website, and a website session does not configure a CLI. Verify a real bounded request through the selected official client instead of treating “logged in” status as sufficient.

A parent app may require a separately installed provider extension. Inspect provider enumeration, executable path, CLI version, adapter mode and configuration home. Correctly select the subscription-specific wire adapter and isolate the candidate's home. A default probe can pick an unconfigured model; capture the actual provider used before declaring credentials broken.

Preserve credentials as opaque secrets. An authorized copy of a vendor login remains limited to the specified client/environment. Use supported import or native CLI execution; an ad-hoc raw-token HTTP client pretending to be that CLI is a different authority path. Remove imported stores, browser profiles and generated secret-bearing state at cleanup, not just the original copied file.

Check environment projection: variables set in a launch shell may be filtered before reaching a child adapter. Use a supported configuration or a documented operational launcher and verify the resulting native permission mode. Keep wrappers explicit; they should configure the real executable, not simulate backend results.

## Model capability and tools

Test the exact native workload: structured tool calls, correct arguments, cwd/path handling, multi-step status and interruption. Text that narrates a shell command is not a tool invocation. A simple completion probe is not comparable to a large native system prompt with tool definitions and history.

Use a stronger or better-matched available model when supported by the user's constraints, record the changed condition and compare like-for-like prompts. Hardware capacity, context length, quantization, parallel requests and cold model loading affect behavior. Avoid universal parameter-count rules; task-level evidence decides fitness.

Keep conversation speech tools available only in the relevant active context. Verify tool registration/injection, local VAD assets and provider/mode-specific approvals. Unrelated connector tools can distract the voice agent or expose more authority than intended; inspect actual selection. If disabling an optional app/plugin feature improves a repeat, preserve the original failure and the new configuration explicitly.

## Configuration, adaptation and compatibility results

Prefer supported endpoints, explicit device selection and normal permission mechanisms. If a source adaptation is justified and authorized, preserve its exact patch and label all dependent results adapted. An application passing with a URL change does not qualify its original hosted provider. Testing a frontend control does not qualify a backend path bypassed by a probe.

Write a compact compatibility record: source/version, components, interface settings without secrets, actual request route, tested operation, observation, workaround, untested variants and upstream verification URL. Recheck it after component upgrades; never silently carry a workaround across versions.

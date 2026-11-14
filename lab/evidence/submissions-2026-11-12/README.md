# Submission triage — November 12, 2026

Issue [#1](https://github.com/csells/awesome-jarvis/issues/1), PR [#3](https://github.com/csells/awesome-jarvis/pull/3) and PR [#4](https://github.com/csells/awesome-jarvis/pull/4) are evaluation requests. No merge, listing, scorecard change or external response is authorized by these findings. All remain pending. No application was installed or run in this pass.

This pass inspected submission text, current upstream metadata and selected source files, and commissioned one blind source reviewer per project using the methodology's hallmark rubric. It is preliminary triage, not completion of the full two-review/reconciliation/hands-on pipeline. Source and metadata snapshots are in ignored `lab/out/submission-review-2026-11-12/`. Evidence links below pin the reviewed commits; upstream binaries may represent different commits.

| Request | Current source reviewed | Preliminary fit | Acceptance still needed |
|---|---|---|---|
| #1 DotDial | `dc001d646d51a893b8e60b4cc75a46690136ff5c` | Desktop voice client; Watch List or voice building-block consideration | Real entitled ChatGPT dot call, wake, barge-in, voice controls, recording/privacy and platform tests |
| #3 ibara | `8fe5a674cbcfa68244d603e148ff1760e1786369` | Computer and Browser Use component | Fresh supported install, real MCP desktop tasks, pairing, approval/deny, takeover, revocation and cleanup |
| #4 /call-me | `b1bb4fde0f7b064c18de96b9ebc44a71893e8a41` | Phone transport for an existing agent; Voice Oversight Contenders consideration | Real subscribed phone, spoken yes/no, no-answer behavior, session routing, lock-screen delivery and actual task cancellation |

## Current progress beyond initial triage

Second independent source reviews are now complete for all four requested projects; they are retained separately and do not certify live behavior. DotDial is installed in its disposable macOS guest and audio isolation/capture has been repaired and independently verified; account sign-in remains pending. /call-me has one genuine blue-seven spoken-response success, plus earlier empty/timeout results; permission enforcement and cancellation remain unverified. No further phone calls were made during the subsequent testing. OpenJarvis's pinned source/native extension and frontend installed in the Linux guest; the model-dependent API remains gated by the requested Dragon endpoint. ibara still requires its supported paired desktop/tailnet setup. See the dated runtime observations and service discovery in [re-verification evidence](../reverification-2026-11-12/README.md). Earlier unchecked lists below preserve the original acceptance scope, not a claim that completed installation/review steps have never occurred.

## DotDial

[Call adapter](https://github.com/aaamosh/DotDial/blob/dc001d646d51a893b8e60b4cc75a46690136ff5c/src/dot_voice.mjs) uses internal ChatGPT web routes and requires an already entitled account. [Local commands](https://github.com/aaamosh/DotDial/blob/dc001d646d51a893b8e60b4cc75a46690136ff5c/src/voice_commands.cjs) implement microphone/speaker controls, hangup and saved-reply playback; they do not implement delegated-task approvals or cancellation. Call hangup is not proof that agent work stops.

The blind review scored Voice/Hands-free/Visual/Oversight **1/1/1/0** on the 0–2 scale. Its Voice finding is narrower than the submission's ● claim: wake and bidirectional calls have code, but barge-in remains unverified. The panel shows call state rather than agent work. These are source-review leads, not hands-on results.

[Privacy/defaults](https://github.com/aaamosh/DotDial/blob/dc001d646d51a893b8e60b4cc75a46690136ff5c/docs/PRIVACY.md): wake/commands default off; wake listening continues locally during transmission mute and can unmute the call. Saved replies are local; recording defaults on, capped at 200 MiB. Session profiles need protection. macOS previews are ad-hoc signed and unnotarized. Core MIT; service dependency and unsupported routes remain material caveats.

Test gates:

- [ ] Complete a second independent review and reconcile before publishing scores.
- [ ] Install a pinned artifact/source in a disposable supported environment; record artifact/source identity.
- [ ] Human signs in inside the guest with an account entitled to an existing dot. Never copy host browser sessions.
- [ ] Prove isolated virtual audio; wake, ask a factual question, record/transcribe reply, interrupt a long answer and measure latency.
- [ ] Exercise mute, unmute, hangup during dialing/call, replay interruption, wake while muted and accidental speaker activation.
- [ ] Inspect actual idle/listening/call/error UI; verify archive retention/deletion and network behavior.

Account-dependent call tests are pending account availability, not FAIL. Synthetic demo/screenshots cannot substitute for a real call.

## ibara

[Tool contract](https://github.com/MayberryDT/ibara/blob/8fe5a674cbcfa68244d603e148ff1760e1786369/src/contract/tools.rs) implements desktop actions. [Control settlement](https://github.com/MayberryDT/ibara/blob/8fe5a674cbcfa68244d603e148ff1760e1786369/src/controller/control.rs) and [console](https://github.com/MayberryDT/ibara/blob/8fe5a674cbcfa68244d603e148ff1760e1786369/console-plugin/ComputerView.qml) supply task leases, viewing and intervention. No voice path is established. These are useful component capabilities.

The blind review scored **0/0/2/2**, with an explicit qualification: oversight means controlling externally supplied agents' access through ibara. That does not establish our full Oversight ● requirement of dispatching agents with visibility, approvals and cancel. Keep placement at building-block consideration; do not promote to Mission Control based on this score.

Current supported setup calls for two x86_64 Omarchy machines with Hyprland, Tailscale pairing and an MCP client. Existing ARM Omarchy lab recipes do not establish compatibility. [Access boundaries](https://github.com/MayberryDT/ibara/blob/8fe5a674cbcfa68244d603e148ff1760e1786369/docs/security-and-access.md) disclose incomplete effect detection and broad Administer capabilities. Agent access is not a sandbox. Own-account pairing can convey broad permissions. [Cua wrapper](https://github.com/MayberryDT/ibara/blob/8fe5a674cbcfa68244d603e148ff1760e1786369/src/desktop/cua.rs) checks environment-disabled telemetry before worker start; network privacy remains untested. Core MIT does not describe every bundled component's license.

Test gates:

- [ ] Complete a second independent review; resolve dispatch/process-cancel scope explicitly.
- [ ] Reserve and provision supported disposable x86_64 environments via the registry; verify live worker capacity first. No installs on a personal desktop or unrelated worker host.
- [ ] Inspect pinned signed installer and package verification; record service/account/compositor changes.
- [ ] Pair task-owned environments using staging access; verify default grants and deliberate denial.
- [ ] Run real MCP native-editor and browser tasks; save/reopen and independently inspect exact file content.
- [ ] Exercise approve, deny, takeover, pause/resume, disconnect, expired lease and revoked pairing; inspect actual job and external agent state separately.
- [ ] Capture and inspect console screenshots; inspect diagnostic/network behavior and remove task-owned pairing/credentials after evidence export.

No supported environment was provisioned in this triage pass. The registry was queried for machine capabilities; its cached inventory is not a live capacity check.

## /call-me

[Claude hooks](https://github.com/radres/call-me/blob/b1bb4fde0f7b064c18de96b9ebc44a71893e8a41/claude-code/hooks/hooks.json) and [answer waiter](https://github.com/radres/call-me/blob/b1bb4fde0f7b064c18de96b9ebc44a71893e8a41/claude-code/monitors/answer-waiter.mjs) support reaching an absent human. [Codex entry](https://github.com/radres/call-me/blob/b1bb4fde0f7b064c18de96b9ebc44a71893e8a41/codex/mcp.mjs) imports the local MCP bundle; equivalent automatic inbound delivery requires separate verification.

The blind review scored **1/1/1/1**. Mobile UI, speech services and backend are absent from the public client source; claimed phone visuals and audio need direct tests. Passing a spoken answer back as text does not establish permission enforcement, agent dispatch or cancellation. Core MIT covers the client, not unrestricted access to the hosted service. A phone app and subscription are prerequisites; do not buy or start a trial implicitly.

The recipient number is sensitive because knowing it permits contacting the phone. Questions/audio travel through the hosted service; backend retention/telemetry are unverified. [Config helper](https://github.com/radres/call-me/blob/b1bb4fde0f7b064c18de96b9ebc44a71893e8a41/claude-code/lib/callme-config.mjs) hardens local state permissions. Hooks can wake the agent; persistent instruction changes and dynamically fetched tool definitions deserve inspection.

Test gates:

- [ ] Complete second independent review; inspect hosted tool schema and compare with pinned client.
- [ ] Obtain an existing subscribed phone's pairing through a private configuration flow. Never publish its number or session token.
- [ ] Run a real call: record/transcribe prompt and spoken response, measure latency, test keep-open and interruption.
- [ ] Connect approval responses to a harmless guest file-write action: yes permits it once, no/unclear/timeout never permits it. Inspect the file independently.
- [ ] Replace the sample workflow's demo number, which is documented to auto-answer yes; the sample approved action is a no-op and proves no enforcement.
- [ ] Start a genuine long-running task, request cancel by voice and check the process stops; hanging up is insufficient.
- [ ] Exercise concurrent sessions, stale answers, disconnection/reconnect and locked-phone notification; confirm responses reach only the intended session.
- [ ] Verify no-answer escalation and session-end cleanup; audit outgoing content, local token permissions and documented data retention.

Phone/subscription-dependent tests are pending availability, not FAIL. No phone messages or calls were sent.

## OpenJarvis — existing-entry re-evaluation

Requested directly on November 12. [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) already appears under Persistent Agents in the list; this is a re-test request rather than a proposed new entry. Source reviewed at [`13706f2b5b5ba6cac9ad31bc575d9e115213784f`](https://github.com/open-jarvis/OpenJarvis/tree/13706f2b5b5ba6cac9ad31bc575d9e115213784f), committed November 12, 2026. GitHub reports an active, unarchived repository, created February 15, 2026, Apache-2.0 license. Metadata is triage evidence, not runtime proof.

Concrete source findings:

- [CLI voice input](https://github.com/open-jarvis/OpenJarvis/blob/13706f2b5b5ba6cac9ad31bc575d9e115213784f/src/openjarvis/cli/_voice_chat.py) explicitly asks the user to press Enter to speak. [Audio helpers](https://github.com/open-jarvis/OpenJarvis/blob/13706f2b5b5ba6cac9ad31bc575d9e115213784f/src/openjarvis/speech/voice_io.py) record until silence and block through playback. This establishes speech plumbing, not wake-word/full hands-free/barge-in coverage.
- [Approval routes](https://github.com/open-jarvis/OpenJarvis/blob/13706f2b5b5ba6cac9ad31bc575d9e115213784f/src/openjarvis/server/approval_routes.py) expose approve/deny operations over persisted pending actions. The [frontend bell](https://github.com/open-jarvis/OpenJarvis/blob/13706f2b5b5ba6cac9ad31bc575d9e115213784f/frontend/src/components/ApprovalBell.tsx) supplies graphical access. Need end-to-end proof that denied, expired or cancelled actions cannot execute, and examination of API authentication wiring.
- The [orchestrator](https://github.com/open-jarvis/OpenJarvis/blob/13706f2b5b5ba6cac9ad31bc575d9e115213784f/src/openjarvis/agents/orchestrator.py) has tool execution and a governance callback. Its name does not establish delegated-agent oversight; dispatch, visibility and process cancellation must be traced and exercised separately.
- Our old README caveat that analytics defaults on and installer telemetry cannot be disabled is outdated for current source. The [Bash installer](https://github.com/open-jarvis/OpenJarvis/blob/13706f2b5b5ba6cac9ad31bc575d9e115213784f/scripts/install/install.sh#L267) accepts `--no-analytics`, leaves unattended/EOF runs off, and treats Enter or Y at the interactive prompt as consent. [Frontend code](https://github.com/open-jarvis/OpenJarvis/blob/13706f2b5b5ba6cac9ad31bc575d9e115213784f/frontend/src/lib/analytics.ts) provides a preference flow; [current documentation](https://github.com/open-jarvis/OpenJarvis/blob/13706f2b5b5ba6cac9ad31bc575d9e115213784f/docs/telemetry.md) distinguishes external analytics from local performance telemetry and leaderboard participation. README caveat corrected on source evidence. This does not certify every distributed installer or absence of network traffic.

Test gates:

- [ ] Complete independent reviews and reconcile hallmark scores against wired execution paths, including desktop and web interfaces.
- [ ] Install pinned source in a registry-reserved disposable VM; use an existing supported local inference backend through its normal interface. Never deploy over stable lab services.
- [ ] Fresh-install privacy tests: explicit decline, unattended mode, EOF and consent; restart server/reload frontend; verify preference persistence and observe actual outbound traffic. Inspect Windows/desktop installer behavior separately before generalizing the Bash finding.
- [ ] Prove virtual microphone/speaker isolation; transcribe actual speech input/output, test interruption and determine whether any interface offers a continuous voice loop.
- [ ] Spawn a real agent on a harmless file task, inspect live state, approve/deny, pause/resume and cancel; independently verify artifacts and process state.
- [ ] Attempt stale/expired approvals and confirm API authorization protects approval mutations. Check permission defaults and the Claude Code subprocess configuration.
- [ ] Inspect screenshots and save logs, transcripts, source/artifact identities and platform-specific caveats before changing placement or publishing scores.

No OpenJarvis installation or hands-on test was performed in this triage pass. Pending runtime checks are not passes or failures. Source snapshots live in ignored `lab/out/submission-review-2026-11-12/OpenJarvis/`.

Blind-review result: Voice/Hands-free/Visual/Oversight **1/0/2/1** (0–2 source rubric). The reviewer independently found click/Enter-triggered speech, graphical approvals, implemented state/tool feedback and partial supervision. Not a published scorecard result.

A priority test lead is that [`agent_spawn` and `agent_kill`](https://github.com/open-jarvis/OpenJarvis/blob/13706f2b5b5ba6cac9ad31bc575d9e115213784f/src/openjarvis/tools/agent_tools.py) update an in-memory registry rather than proving real worker dispatch/termination. Separate managed-agent execution routes exist; exercise the actual route used by the UI before drawing a general conclusion. Stopping a client stream also does not prove downstream work stops.

Further source-review risks: speech discovery can fall through to cloud providers, so pin local STT/TTS for local-only tests. External analytics defaults off while local telemetry/traces default on. Security config enables several checks but leaves RBAC and container sandbox disabled by default, with unrestricted file directories unless configured. Verify actual enforcement with narrowly scoped test directories. These are review findings, not observed runtime failures.

README validation: `awesome-lint@2.3.0` and `git diff --check` passed. Lint used a task-specific temporary npm cache because the default cache was not writable; no global cache permissions were changed.

## Live setup — November 12

Task-owned macOS VM `orca-automation-dotdial-69yhhw5bmr` is registered as `test-dotdial-69yhhw5bmr`, with owner/expiry and authenticated console access. DotDial beta.4 macOS preview1 Apple Silicon ZIP was downloaded from its official release; SHA-256 matched `c40cc1da9c3bb57ca66235ed6506b4cf9c607c8e1042a6e58fc0782c45feee9c`. Installed in guest only; app launch and Settings UI were viewed. Dot configuration is prepared; account sign-in and all audio/hallmark tests remain pending. The review endpoint rejected an unauthenticated request with HTTP401. Private session and console data are outside the repo.

One real /call-me `/ring` request returned `declined` after 12.9 seconds, with no transcript. Chris confirmed he deliberately declined because it was 6:20 AM and his wife was sleeping. This is neither a product failure nor a completed speech test. **Do not send further calls or phone notifications until Chris explicitly says he is ready.** The one-off call helper is guarded against accidental rerun. Recipient and response/session data are task-private and omitted from evidence. No approval or execution action was attached to the call.

Console correction: the initial noVNC page imported a nonexistent `package/core/rfb.js` from the npm distribution and never connected. Replaced the client with official noVNC v1.6.0 browser sources and added UTF-8 metadata. A task-owned headless browser then reached RFB state `connected` with a 2048-pixel canvas; its captured rendered desktop was inspected, and the browser was closed. The earlier HTTP200 check alone had not verified browser operation.

Relay lifetime correction: BB Connect later reported ECONNREFUSED because the shell-owned websockify process had exited. The task relay now runs under temporary user launchd job `app.getbb.dotdial-console.thr69yhhw5bmr`, using task-local `relay-venv` and `console-relay.plist` in private storage. Verified running with no exits, HTTP200 across separate tool calls, and browser RFB `connected`. Cleanup must boot out this exact job, unexpose18943 and remove the task-local environment after testing. No phone tests resumed.

## Phone retry and audio setup — November 12

Chris explicitly authorized calls again. First `/ring` attempt returned completed after33.1s but an empty transcript; Chris confirmed answering and speaking. A session-based `/aiphone/calls` attempt timed out after56.2s with no transcript. Chris reported poor app behavior in the car and requested one further try. That retry completed after22.9s with a28-character transcript containing the requested “blue seven.” This establishes one real spoken-response transport success, not reliable operation or general approval/cancel enforcement. Durations are total request/call times, not speech latency. No approval or action was attached. Private responses and session tokens are excluded from this report.

Guest audio tools and official BlackHole2ch/16ch installed successfully; installer required a guest restart. An initial pre-restart recording returned zero RMS for both injected-mic and isolation recordings, and the independent STT result was empty. Therefore the audio self-test has NOT passed. Earlier progress text suggesting injected audio was captured was incorrect. Guest restart and retest underway. The shared voice service reservation used for transcription was released; its processes were left running. Public voice client access returned HTTP403/1010; the documented native loopback interface worked, so this is not evidence of backend downtime.

Audio follow-up: guest reboot verified via kern.boottime; repeating the loopback test still captured silence. The generated speech source WAV had RMS0.104491 and peak about0.74, so the source is non-silent. Granting the recording tool guest-only microphone permission, including its resolved executable path, did not resolve capture silence. Both loopback and isolation RMS remained0. DotDial speech tests remain BLOCKED by the lab audio path, independently of its pending ChatGPT sign-in; this is not an application voice failure. The console relay remains available. No further phone calls were placed after the successful blue-seven retry.

## Phone approval attempt — November 14

Chris authorized one further call and was available to answer. A fresh session and `/aiphone/calls` request followed the published client request format, with a 55-second server timeout and an 85-second HTTP budget. The service returned `timeout` after 56.7 seconds with an empty transcript; Chris confirmed the phone **did not ring**. A read-only check of this test session returned one `missed_call` event with status `timeout`, without a delivery error or explanation. This is a failed call-delivery observation; its cause remains unresolved. It is not a refusal, a successful no-answer notification, or a spoken-approval pass.

The prompt requested yes/no permission to create one harmless scratch file in the isolated Linux guest. The test harness required a completed call and an explicit affirmative transcript before execution. No approval was received, and an independent guest check confirmed that the file was absent. This verifies only that the harness withheld this action when the call failed; it does not establish product-level permission enforcement. Spoken yes/no/unclear, actual cancellation, repeatability and session/reconnect tests remain incomplete. No retry was placed. The one-call helper is guarded against accidental rerun. Recipient, session token and call/session identifiers remain private; session termination/revocation is unverified.

## Call delivery diagnosis — November 14

Chris confirmed the configured recipient still matches the number displayed in his app. Session registration succeeded, the missed-call event targets that same number, and the initial request received a terminal server response rather than a local HTTP timeout. Hosted MCP `poll_result` also returned `timeout` for that call, without a delivery error. The published client format remains unchanged at the reviewed source commit. No call was attached to a task action during the following diagnostic comparisons.

After Chris opened the phone app, the following controlled calls completed:

| Transport | Session | Phone state | Observed result |
|---|---|---|---|
| Hosted MCP | Original | App open as requested |16.9s, transcript “Okay.” Chris confirmed ringing and hearing the requested prompt. Harness requested hang-up; subsequent read-only MCP polling verified `ended` with `open:false` |
| Published HTTP | Original | App open as requested |16.7s, “blue seven” transcript |
| Published HTTP | Original | Chris explicitly confirmed Home screen, app in background without force-quitting, phone unlocked |14.6s, “blue seven” transcript |
| Published HTTP | Freshly registered | Same background/unlocked condition |17.0s, “blue seven” transcript |

These are total request durations, not speech latency. The HTTP comparisons retained the same recipient, prompt, 55-second server timeout and 85-second HTTP budget; the background and fresh-session comparisons changed one condition at a time. Each helper is guarded against accidental rerun; no automatic retries are scheduled.

Those four comparisons did not reproduce the original failure. They show that the HTTP route, background/unlocked operation and fresh-session creation can all deliver the call. Chris then identified an Android Pixel 11 Pro Fold, with the app unused for days. DND was off at report time but had been enabled a few minutes earlier; the exact setting at the original failed-call time remains unverified.

Pixel notification settings provide separate People and Apps filters for DND, including a repeat-caller exception. See [Google’s Pixel Modes/DND documentation](https://support.google.com/pixelphone/answer/6111295?hl=en). To test suppression, Chris explicitly enabled DND with the app in the background and phone unlocked. A fresh-caller HTTP comparison, with caller identity verified different from the original session, returned `timeout` after 57.0s with an empty transcript. This reproduces the original API failure pattern and makes DND suppression the leading explanation. Phone-side observation and a same-session DND-off confirmation are pending; the confirmation call will wait for Chris to report readiness.

Provider push/device-registration diagnostics are unavailable through the public interfaces. The DND-on result does not establish that DND was active at the exact original failure time or rule out another transient cause for that historical call. None of these comparisons completes spoken approval/denial, action enforcement, cancellation or locked-phone qualification.

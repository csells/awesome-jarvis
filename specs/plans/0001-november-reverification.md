# November re-verification — incomplete

Scope: the November staleness report, DotDial issue #1, ibara PR #3, /call-me PR #4, and OpenJarvis. PRs are evaluation requests; no acceptance or merge is implied. Independent source reviews are complete, but the hands-on pipeline and final reconciliation are not.

## Completed

- Added all open PRs, including drafts, to staleness reports and related-reference findings.
- Corrected repository moves, stale links and archived/inactive entries.
- Fixed contributor counting: renamed Git authors sharing an email do not establish independent maintainers.
- Verified permanent Pocket speech/transcription and Mac Ollama access from the disposable Linux worker. Chris explicitly authorized both Mac services; Dragon is no longer a prerequisite.
- Captured scoped runtime results for Newelle, OpenJarvis, Paseo, AIRI, usejarvis, OpenClaw, Sutando and Dodaios. See [re-verification evidence](../../lab/evidence/reverification-2026-11-12/README.md) and [submission evidence](../../lab/evidence/submissions-2026-11-12/README.md).
- Last validation:52 offline tests, Awesome lint and whitespace checks passed. No new scorecard test dates or submission acceptance claims.

## Remaining end-to-end tests

| Project | Remaining work | External prerequisite |
|---|---|---|
| DotDial (#1) | Real dot call; recorded reply, wake, barge-in, mute/unmute/hangup, recording/privacy and error recovery | Human ChatGPT sign-in inside the prepared guest |
| ibara (#3) | Supported two-desktop installation/pairing; real browser/editor MCP tasks; approve/deny/takeover, expiry/revocation and cleanup | Supported x86 Omarchy pair and authorized Tailscale pairing |
| /call-me (#4) | Repeatable spoken yes/no/unclear/no-answer; enforce a real harmless action; actual task cancellation; session isolation, locked-phone and reconnect tests | Four delivery diagnostics completed after app opening; three blue-seven transcripts. DND-on/background timed out 57.0s with confirmed silent phone; DND-off/same-session control also timed out 56.4s. Explicit retry timed out 56.5s despite Chris answering/hearing prompt/saying blue seven; no got-it acknowledgement. Late poll empty; matched missed-call event cannot establish an unanswered call. Investigate microphone/uplink/recognition/result return; audio-route/permission observations requested |
| OpenJarvis | Wake/other frontend voice paths, actual cancellation beyond Pause, installer consent variants and observed privacy traffic. Managed CLI shell deny/approve and file effects verified; Pause left the bounded worker running. CLI microphone/reply verified with Pocket using a disclosed one-line URL change; spoken stop did not interrupt that CLI reply | Packaged desktop1.0.5 client/API reply now verified after guest prerequisites; fresh backend installer remains untested. Stock CLI TTS endpoint is hardcoded |
| Newelle | Repeated classic secondary-STT wake and recorded spoken replies now verified with the phrase computer. One-shot barge-in failed; classic wake stop was recognized but delayed while counting continued. Spoken approvals/denial and genuine delegated-task cancellation remain unverified | None for configured local paths |
| AIRI | Diagnose source-web loading and model-switch latency; complete real voice loop, barge-in and supported task/control tests. Native Qwen2.5 chat answer and analytics-off persistence across restart now verified | None for supported local paths; distinguish virtual graphics limits |
| OpenClaw | Authenticated native Codex text reply verified; exec safely rejected by approval-binding review with both CLI versions, so no approve/deny or worker-cancel pass. Native Mac connection, microphone/model turn and Pocket playback callbacks now verified, plus gateway-generated TTS. Actual native speaker recordings remain silent/near-silent; resolve playback capture/routing and the observed speech-permission crash before wake/barge-in qualification | Guest microphone/speech permissions where required |
| Paseo | Voice mode transcribes speech but session reports no speak tool; output recordings have empty transcripts, so reply/barge-in remain unverified. Spoken approve/deny and failure recovery remain. Foreground stop failure now reproduced with subscription Codex | Authenticated subscription Codex available; speech-tool session integration remains unresolved |
| usejarvis | Native onboarding authentication failure; Pocket speech compatibility; wake, reply/barge-in, safe approvals, real worker stop versus audio-only stop. Browser setup and text reply now verified with Qwen3 4B; default awareness errors recorded and task-sidecar capture capabilities disabled | Local speech option has no Pocket lease-key field; no paid provider key supplied |
| Sutando | Native macOS menu-bar build/sign/launch/UI and Accessibility grant verified; other permissions, native core, voice and approval checks remain; scope observed cancellation failure and startup/skill warnings. Authenticated Linux API/watcher/core/result/file task verified; cancellation arrived after bounded foreground work completed | Subscription CLI access now available; native voice path still needs unsupported provider credentials |
| Dodaios | Scope managed `run_shell` write without a human card under Ask mode and provider-switch policy reset. Actual worker cancellation now tested and failed; speech, wake/barge-in and persistence remain. OpenCode text and Codex managed file execution verified | Subscription CLI available; real Pocket checks through shipped OpenRouter adapters returned STT415/TTS422 after model coercion. Full speech path needs a compatible supported adapter |
| OpenVision | Resolve/retest recorded build gate as applicable; actual iPhone/glasses voice, camera and Hermes oversight paths | Compatible physical devices, signing/Meta configuration and gateway |
| Jarvis Vocal | Supported Windows runtime and real delegation/cancellation if evaluating further; no contributor-based promotion justified | Windows test environment; newest100 commits establish one author identity |

The user deferred phone calls and DotDial browser sign-in on November 13. On November 14 the authorized approval attempt timed out with no ring, transcript or scratch-file action. During the requested root-cause diagnosis, four controlled calls completed after app opening, including background/unlocked and fresh-session comparisons. A DND-on/background comparison reproduced a 57.0s timeout with confirmed silence, but the same-session DND-off control also timed out 56.4s. DND alone is not an established root cause; the control phone observation is pending. No diagnostic action was attached; no automatic retries. Chris is ready to resume DotDial sign-in; the Orca guest and authenticated console are available, with sign-in completion still pending. Continue independent lab work. Known failed worker-stop and acoustic tests are completed observations, not pending passes. Untested recovery, privacy and permission permutations remain visible below.

## Completion criteria

For each supported path, exercise the actual application, capture/transcribe audio and inspect screenshots. Check independent file/process effects after approve, deny and cancel; a stopped badge or hung-up call is insufficient. Test silence/timeout, stale or concurrent approvals, reconnect/restart and privacy defaults. Mark externally gated paths BLOCKED with a specific prerequisite; do not count source reviews, installation or fixtures as hallmark passes.

Then reconcile independent reviews against runtime evidence, finish safety/license assessment, update testing.md and scorecard data only where justified, rerun the full report/lint/tests, and export evidence before task-owned environment cleanup. Preserve the pending sign-in guest while needed. No merges or publication of accepted entries are included in this branch push.

## Suggested execution order

1. Finish local-model tests for Newelle, OpenJarvis, Paseo, usejarvis and Dodaios; diagnose AIRI and configure OpenClaw.
2. Complete DotDial/Sutando login and phone-dependent checks when access is available; provision supported ibara pairing and address OpenVision hardware gates.
3. Reconcile findings, update only verified scores and dates, rerun checks, and clean up disposable resources.

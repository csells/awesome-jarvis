# November re-verification — incomplete

Scope: the November staleness report, DotDial issue #1, ibara PR #3, /call-me PR #4, and OpenJarvis. PRs are evaluation requests; no acceptance or merge is implied. Independent source reviews are complete, but the hands-on pipeline and final reconciliation are not.

## Completed

- Added all open PRs, including drafts, to staleness reports and related-reference findings.
- Corrected repository moves, stale links and archived/inactive entries.
- Fixed contributor counting: renamed Git authors sharing an email do not establish independent maintainers.
- Verified permanent Pocket speech/transcription and Mac Ollama access from the disposable Linux worker. Chris explicitly authorized both Mac services; Dragon is no longer a prerequisite.
- Captured scoped runtime results for Newelle, OpenJarvis, Paseo, AIRI, usejarvis and Dodaios. See [re-verification evidence](../../lab/evidence/reverification-2026-11-12/README.md) and [submission evidence](../../lab/evidence/submissions-2026-11-12/README.md).
- Last validation:52 offline tests, Awesome lint and whitespace checks passed. No new scorecard test dates or submission acceptance claims.

## Remaining end-to-end tests

| Project | Remaining work | External prerequisite |
|---|---|---|
| DotDial (#1) | Real dot call; recorded reply, wake, barge-in, mute/unmute/hangup, recording/privacy and error recovery | Human ChatGPT sign-in inside the prepared guest |
| ibara (#3) | Supported two-desktop installation/pairing; real browser/editor MCP tasks; approve/deny/takeover, expiry/revocation and cleanup | Supported x86 Omarchy pair and authorized Tailscale pairing |
| /call-me (#4) | Repeatable spoken yes/no/unclear/no-answer; enforce a real harmless action; actual task cancellation; session isolation, locked-phone and reconnect tests | User available to answer the subscribed phone |
| OpenJarvis | Wake/other frontend voice paths, actual cancellation beyond Pause, installer consent variants and observed privacy traffic. Managed CLI shell deny/approve and file effects verified; Pause left the bounded worker running. CLI microphone/reply verified with Pocket using a disclosed one-line URL change; spoken stop did not interrupt that CLI reply | Packaged desktop remains untested; stock TTS endpoint is hardcoded |
| Newelle | Wake/continuous voice, repeat/scope observed one-shot barge-in failure, spoken approvals/denial and genuine delegated-task cancellation | None for configured local paths |
| AIRI | Diagnose source-web loading and native chat not replying; complete real voice loop, barge-in and supported task/control tests; verify analytics preference persistence | None for supported local paths; distinguish virtual graphics limits |
| OpenClaw | Finish gateway/native-client configuration; safe exec policy; real wake/reply/barge-in, approvals, dispatch and child-process cancellation | Guest microphone/speech permissions where required |
| Paseo | Voice-session setup and recorded dialogue; spoken approve/deny; scope reproduced foreground/background-command survival, compare other supported providers and failure recovery | Local Codex/Ollama path available; subscription providers require dedicated lab login |
| usejarvis | Native onboarding authentication failure; Pocket speech compatibility; wake, reply/barge-in, safe approvals, real worker stop versus audio-only stop. Browser setup and text reply now verified with Qwen3 4B; default awareness errors recorded and task-sidecar capture capabilities disabled | Local speech option has no Pocket lease-key field; no paid provider key supplied |
| Sutando | Native macOS UI/permissions, voice and approval checks; scope observed cancellation failure and startup/skill warnings. Authenticated Linux API/watcher/core/result/file task verified; cancellation arrived after bounded foreground work completed | Subscription CLI access now available; native voice path still needs unsupported provider credentials |
| Dodaios | Scope managed `run_shell` write without a human card under Ask mode; provider-switch policy reset; speech, wake/barge-in, worker cancellation and persistence. OpenCode text and Codex managed file execution verified | Subscription CLI access now available; native Pocket speech compatibility remains unverified |
| OpenVision | Resolve/retest recorded build gate as applicable; actual iPhone/glasses voice, camera and Hermes oversight paths | Compatible physical devices, signing/Meta configuration and gateway |
| Jarvis Vocal | Supported Windows runtime and real delegation/cancellation if evaluating further; no contributor-based promotion justified | Windows test environment; newest100 commits establish one author identity |

## Completion criteria

For each supported path, exercise the actual application, capture/transcribe audio and inspect screenshots. Check independent file/process effects after approve, deny and cancel; a stopped badge or hung-up call is insufficient. Test silence/timeout, stale or concurrent approvals, reconnect/restart and privacy defaults. Mark externally gated paths BLOCKED with a specific prerequisite; do not count source reviews, installation or fixtures as hallmark passes.

Then reconcile independent reviews against runtime evidence, finish safety/license assessment, update testing.md and scorecard data only where justified, rerun the full report/lint/tests, and export evidence before task-owned environment cleanup. Preserve the pending sign-in guest while needed. No merges or publication of accepted entries are included in this branch push.

## Suggested execution order

1. Finish local-model tests for Newelle, OpenJarvis, Paseo, usejarvis and Dodaios; diagnose AIRI and configure OpenClaw.
2. Complete DotDial/Sutando login and phone-dependent checks when access is available; provision supported ibara pairing and address OpenVision hardware gates.
3. Reconcile findings, update only verified scores and dates, rerun checks, and clean up disposable resources.

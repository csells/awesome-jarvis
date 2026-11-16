# November curation decisions — November 16, 2026

The maintainer requested final fixed-or-declined decisions for this campaign. The evidence supports publishing the reference corrections and bounded assessments below, and declining all three submissions. Closing the evaluation does not turn unexecuted tests into passes or certify every platform/provider. The [original test matrix](../plans/archive/0001-november-reverification.md) preserves those limits.

## Submission decisions

| Request | Decision | Evidence and reason |
|---|---|---|
| Issue #1, DotDial | Decline this addition; close as not planned | Two source reviews and native authenticated macOS tests completed. A profile/conversation-ID workaround connected a call, but the recorded reply contained no verified speech. The client has no delegated-agent oversight. Its narrow desktop-call use case and internal ChatGPT API dependency do not justify adding it in this update. This is a curation decision, not a claim that every DotDial configuration fails. |
| PR #3, ibara | Decline this addition; close unmerged | Useful computer-use component, with a locked build, real local MCP/daemon checks and 573 upstream fixture passes across corrective reruns; two platform assumptions remain. Supported remote desktop tasks, pairing and approvals were never qualified. The maintainer excluded Tailscale, which the supported two-Omarchy-computer workflow requires. This is an environment/qualification limit, not a failed product E2E test. |
| PR #4, /call-me | Decline this addition; close unmerged | Several genuine spoken responses passed, including brief background operation. Later background attempts returned empty transcripts/timeouts, including an answered call whose prompt was heard. Foreground operation is a workaround; unattended oversight, action approval/cancellation and session isolation are unqualified. The 55-second test budget was shorter than the published 300-second default; no universal failure or confirmed Android root cause is claimed. |

See [submission reviews and real-call observations](../../lab/evidence/submissions-2026-11-12/README.md), [DotDial diagnosis](../../lab/evidence/submissions-2026-11-12/dotdial-nov16-diagnosis.json), and [ibara component cases](../../lab/evidence/reverification-2026-11-12/nov16/ibara-no-tailscale.json). No new phone calls are needed for these rejection decisions.

Final upstream readback: DotDial remains at `dc001d646d51a893b8e60b4cc75a46690136ff5c`; /call-me remains at `b1bb4fde0f7b064c18de96b9ebc44a71893e8a41`. ibara advanced 23 commits to `8e4c804ea4319f9953e276dcc060824b746c2ee4`. Its current README still explicitly requires two x86_64 Omarchy desktops and a Tailscale account on both. The older native/component results are not relabelled as tests of that newer revision. Reconsideration would need new evidence addressing the reason for decline.

## Staleness and existing-entry decisions

| Finding | Final disposition |
|---|---|
| Limitless/Rewind and Gemini Live links | Replace with current destinations. Automated HTTP allowances remain explicitly unverifiable rather than certified reachable. |
| Archived UI-TARS Desktop and Stretch AI | Move to history. |
| Inactive Vibe Notch and OpenYabby | Move to history. |
| mlx-audio, Personal Jarvis/Dodaios and Meta toolkit moves | Update canonical repository references. |
| Newelle 1.6.1 | Place in Voice Assistants: manual gates passed; actual direct/subagent worker cancellation failed. |
| OpenJarvis | Retain as an Agent Framework. Managed Linux desktop install/chat, manual file gates and scoped opt-out behavior were exercised; Pause left work running. No full native voice, Windows or cancellation claim. |
| Paseo 0.16 | Place in Mission Control with Partial coverage. Actual current-turn/background controls passed. Configured voice/barge-in passed with Codex apps disabled; spoken approvals remain limited. |
| Qwen Audio Agent 2.1 | Retain with Partial coverage and reduced oversight. Real speech/barge-in and manual file gates passed; actual worker survived native cancellation. |
| OpenClaw 2026.11.4 | Retain with Partial coverage. Configured native Codex file gates, executing-worker Stop, stale-denial rejection and fresh-permission recovery passed. Native voice/platform and child/cloud custody limits remain explicit. |
| AIRI 0.15.4 and Sutando 0.13 | Retain with Partial coverage and documented risks. Current chat/input or native file work does not establish working Pocket playback or reliable worker cancellation. |
| Jarvis Vocal promotion | Decline promotion: changing Git author names resolved to one identity. Windows runtime remains untested. |
| Dodaios, OpenVision and usejarvis promotion | Decline promotion for this review. Keep Watch List placement and dated next-review triggers: observed approval/cancel failures, startup/physical-device limits, or onboarding/speech limitations respectively. |

The three dated Watch List exceptions record completed no-promotion decisions, not accepted Jarvis features or forgotten work. The normal maintenance job will revisit them. Physical iPad/glasses, Windows and additional provider/privacy/recovery permutations were not completed; this campaign ends with conservative placements rather than broader claims.

## Publication and closure

Publish the validated review branch, close #1/#3/#4 with these reasons, then run every staleness check against the published tree with publishing enabled. Close #2 as completed only when that run has no actionable findings. Preserve the resulting report and verify GitHub issue/PR states and production checks. No third-party fixes, subscription purchases or changes to stable lab services are part of these decisions. Task guests remain stopped under the lab retention rule; the retained DotDial authenticated guest profile and copied CLI login were verified absent before its final shutdown.

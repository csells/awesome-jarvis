# November curation decisions — November 16, 2026

The maintainer requested final fixed-or-declined decisions for this campaign. The evidence supports publishing the reference corrections and bounded assessments below, adding ibara and /call-me as building blocks, and listing DotDial on the Watch List. Closing the evaluation does not turn unexecuted tests into passes or certify every platform/provider. The [original test matrix](../plans/archive/0001-november-reverification.md) preserves those limits.

## Submission decisions

| Request | Decision | Evidence and reason |
|---|---|---|
| Issue #1, DotDial | Accept on Watch List › Desktop, Mobile and Glasses | Two source reviews and native authenticated macOS tests completed. A profile/conversation-ID workaround connected a call, but the recorded reply contained no verified speech. Record the audible-reply test as FAIL for that tested configuration, with cause unresolved. Its optional wake word and floating call controls justify watching this early voice client; internal ChatGPT API dependence and unqualified wake/barge-in remain explicit. This is not a Jarvis scorecard endorsement or a claim that every configuration fails. |
| PR #3, ibara | Accept as a Computer and Browser Use building block | Locked build, real local MCP/daemon checks and 573 upstream fixture passes across corrective reruns support the component listing; two platform assumptions remain. Supported remote desktop tasks, pairing and approvals remain unqualified. The entry explicitly requires Omarchy and Tailscale and discloses that paired-desktop E2E has not run. The earlier rejection confused an evaluation constraint with a reason to exclude a useful component. |
| PR #4, /call-me | Accept as a Tools and Protocols utility | Genuine spoken-response calls verify the phone question/answer transport. The utility supplies communication for an existing agent, which owns action policy and cancellation. It gets no Jarvis scorecard row or oversight claim. Disclose paid app, hosted audio processing and observed intermittent Android/Bluetooth background replies. Action enforcement/session isolation remain unqualified; failed tests used 55 seconds versus the published 300-second default. |

See [submission reviews and real-call observations](../../lab/evidence/submissions-2026-11-12/README.md), [DotDial diagnosis](../../lab/evidence/submissions-2026-11-12/dotdial-nov16-diagnosis.json), and [ibara component cases](../../lab/evidence/reverification-2026-11-12/nov16/ibara-no-tailscale.json). No new phone calls are needed to substantiate the narrowly described transport utility. Background delivery limitations remain explicit.

Final upstream readback: DotDial remains at `dc001d646d51a893b8e60b4cc75a46690136ff5c`; /call-me remains at `b1bb4fde0f7b064c18de96b9ebc44a71893e8a41`. ibara advanced 23 commits to `8e4c804ea4319f9953e276dcc060824b746c2ee4`. Its current README still explicitly requires two x86_64 Omarchy desktops and a Tailscale account on both. The older native/component results are not relabelled as tests of that newer revision. Broader runtime claims would need new evidence for the corresponding path.

## Staleness and existing-entry decisions

| Finding | Final disposition |
|---|---|
| Limitless/Rewind and Gemini Live links | Replace with current destinations. Automated HTTP allowances remain explicitly unverifiable rather than certified reachable. |
| Archived UI-TARS Desktop and Stretch AI | Move to history. |
| Inactive Vibe Notch and OpenYabby | Move to history. |
| mlx-audio, Personal Jarvis/Dodaios and Meta toolkit moves | Update canonical repository references. |
| reSpeaker XVF3800 repository archived during final scan | The archived README explicitly points to formatBCE/Respeaker-ESPHome-integration. Verify the destination is active and contains the XVF3800 firmware documentation, then update the reference. No new hardware runtime claim. |
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

The earlier closure of #3/#4 as declined is superseded: incorporate their building-block entries with the revised placement and limitations, and attach correction comments to both requests. #1 is also accepted on the Watch List with its failed audible-reply test retained; change its closure reason to completed. Publish the validated review branch, then run every staleness check against the published tree with publishing enabled. Close #2 as completed only when that run has no actionable findings. Preserve the resulting report and verify GitHub issue/PR states and production checks. No third-party fixes, subscription purchases or changes to stable lab services are part of these decisions. Task guests remain stopped under the lab retention rule; the retained DotDial authenticated guest profile and copied CLI login were verified absent before its final shutdown.

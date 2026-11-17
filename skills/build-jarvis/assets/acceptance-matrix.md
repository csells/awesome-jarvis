# Jarvis acceptance matrix

Candidate/build identity:
Date and environment:
Native client, model/provider/adapter and permission mode:
Required build contract:
Evidence destination and privacy/redaction policy:

Each case gets PASS, PARTIAL, FAIL, BLOCKED or NOT RUN. Separate direct controls, native integration, source/fixture results and physical tests. Add a row for each required variant; do not prefill passes from examples.

| ID | Requirement/variant | Valid preconditions | Actual native trigger | Expected independent observation and bound | Result | Evidence/artifact | Limit/blocker/owner |
|---|---|---|---|---|---|---|---|
| AUDIO-IN | Input control | | | | | | |
| AUDIO-OUT | Speaker control | | | | | | |
| AUDIO-ISO | No feedback | | | | | | |
| VOICE-REPLY | Actual question/reply | | | | | | |
| VOICE-BARGE | Interrupt real speech/new answer | | | | | | |
| APPROVE | Actual pending action/yes | | | | | | |
| DENY | Actual pending action/no | | | | | | |
| AMBIGUOUS | Unclear/silence/timeout | | | | | | |
| STALE | Expired/replayed/revoked grant | | | | | | |
| ISOLATE | Concurrent approvals/jobs/sessions | | | | | | |
| CANCEL | Actual executing worker/descendants | | | | | | |
| BACKGROUND | Intentional background ownership | | | | | | |
| RECOVER | Fresh work and restart/reconnect | | | | | | |
| VISUAL | Inspected conversation/task states | | | | | | |
| MEMORY | Persist/update/delete/isolation | | | | | | |
| PRIVACY | Consent/defaults/retention/network | | | | | | |
| DEVICE | Required real-device conditions | | | | | | |
| OPERATE | Outage/resource/lease behavior | | | | | | |
| CLEANUP | Owned resources/credentials absent | | | | | | |

## Per-case evidence record

- Case ID and requirement:
- Source/artifact/version and configuration differences:
- Precondition control results:
- Trigger and exact intended effect:
- Start/end time, configured timeout and observation intervals:
- Independently observed input/output/file/process/external job state:
- Manual steps and altered source/configuration:
- Outcome, scope, uncertainty and invalid attempts:
- Sanitized artifact references and hashes where useful:
- Native cleanup versus later harness cleanup:

## Acceptance decision

- Required cases passed:
- Required cases failed/partial:
- External blocked/unexecuted cases and effect on deliverability:
- Optional cases deliberately outside this release:
- Deployment/promotion decision and authority:
- Claims supported by this run, and exact provider/platform limits:

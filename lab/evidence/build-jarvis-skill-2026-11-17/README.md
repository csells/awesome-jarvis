# Build-jarvis skill: actual build and native tests

November17,2026 UTC. [Evaluation and failure history](../../../specs/research/build-jarvis-live-evaluation.md).

The fresh builder implemented a bounded assistant using the skill. A separate observer exercised its real browser microphone → transcription → model/command router → speech → speaker path in a disposable Linux VM against existing real model/speech services. This is functional evidence for the bounded integration, not a production release or a test of every recipe in the skill.

- [Native observations](native-cases.json):23 audio attempts, preserving failures, partial exchanges and successful repetitions;15 independent effect/state records and explicitly labelled analysis copies.
- [Artifact manifest](artifact-manifest.json): exact v1–v7 source hashes, final runtime identity and private archive checksums. Original source, screenshots, synthetic recordings, worker heartbeats and events are preserved outside the VM. Raw evidence stays private; no lease credentials or browser profiles are in the exports.
- [Cleanup](cleanup.json): actual service/workers/browser stopped, audio defaults restored, leased keys and profile removed, owned forwards and ports closed, shared speech lease released and healthy, VM identity verified and stopped. Registry readback revision20 records completed scope, owner and retention expiry. The stopped guest disk is retained for retesting under [lab rules](../../RULES.md); no service was promoted.

## Final callback regression

After preserving the actual false-error screenshot and v6 source, v7 guarded playback events and rejected playback promises by generation and player identity. The observer reloaded the actual page, enabled its real microphone, then repeated interruption during verified output. The old count stopped; an analysis segment of the actual speaker recording independently transcribed “Two plus two is four.” A subsequent full native voice exchange independently transcribed the France question and Paris answer. The full-page final screenshot was opened and inspected: completed new turns, cancelled worker, approval states and the teal memory were visible; the false playback failure banner was absent. The original full recording and its less clear combined-count transcript remain in the evidence.

Inspected private screenshot artifacts include `question-session3-result.png`, `barge-v5-on-result.png`, `normal-pending-denial.png`, `normal-full-ui.png`, `normal-worker-full-ui.png` and `final-full-ui.png`. The last two directly exposed the erroneous old-player banner and verified its absence after the patch. Cropped viewport screenshots do not independently establish offscreen card state; complete DOM snapshots and backend/disk observations accompany them.

## Limits

The work process was a real bounded health sampler, not a coding agent. Virtual isolated audio does not qualify acoustic echo cancellation, physical devices or phone/Bluetooth behavior. v4's intermittent interruption failure remains unexplained; later observed successes do not erase it. Parser checks, direct HTTP concurrency checks and replay requests are supporting controls, separately identified from actual native voice. No implementation without the skill was built as a comparative baseline, so no measured skill uplift is claimed.

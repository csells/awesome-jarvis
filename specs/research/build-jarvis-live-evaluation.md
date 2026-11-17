# Build-jarvis: live implementation evaluation

November17,2026 UTC, branch `review/build-jarvis-skill`. The [initial response scenarios](build-jarvis-skill-evaluation.md) tested instruction interpretation. They did not establish that the skill could guide a working implementation. This evaluation adds an actual build, native browser audio and independently inspected effects.

## Method and scope

A fresh builder received the skill, user requirements and real operational interfaces, then implemented a bounded assistant in a disposable Debian13 VM. The skill author independently operated its native browser and measured microphone/speaker recordings, file contents, process identities and heartbeats. The builder repaired demonstrated faults; its own API checks were supporting controls, not substitutes for these observations.

The candidate used real Ollama `qwen3:4b-instruct-2507-q4_K_M`, permanent Pocket/Alfred transcription and synthesis, and a task-scoped speech lease. No model or speech mocks were used. General questions went to the model. A deterministic command router handled the explicitly bounded memory, approval and worker operations; this was not an LLM tool planner. The native Chromium156 page used actual Web Audio capture, VAD, WAV upload, real STT, model routing, real TTS and HTML audio playback. Separate virtual input and output buses prevented feedback. Both routes were independently controlled before grading speech.

The worker was a real, separately owned Python process sampling the candidate's health once per second, with a heartbeat and separate natural-completion marker. It was not an autonomous coding agent. The one file action was a proposed scratch note with a short-lived, one-use backend approval. Memory retained one explicitly requested harmless fact. These deliberately small tasks made the actual effects independently checkable.

## Observations and repairs

| Actual case | Observation | Result |
|---|---|---|
| Input/output controls | Input speech reached only the microphone route; output control reached only the speaker route, independently transcribed | PASS |
| v1 native voice question | Real browser capture was WebM while the builder's direct control used WAV; native transcription failed and speaker recording was silent | FAIL retained |
| Container diagnosis | The actual upstream rejected a repeated WebM control with HTTP500; bounded normalization to mono16k WAV returned recognized speech | Supporting control; original native failure's HTTP status was not captured |
| v2 native voice question | Speech was recognized, but a late global interrupt immediately cancelled the new turn | FAIL retained |
| Scoped interruption repair | Exact old-turn identity, ordered interruption and generation guards; delayed old-ID HTTP requests could not cancel the new turn | Supporting concurrency check, followed by native tests |
| v3 native question | Independent input: France question; independent speaker: “The capital of France is Paris.” | PASS |
| v3 interruption | Old speech stopped, but the new question was not recognized; onset capture could clip the utterance | PARTIAL retained; bounded pre-roll added |
| v4 interruption | Input control contained both requests, but the old count continued and no new capture was detected | FAIL retained; cause unresolved |
| v5 interruption repetitions | Two actual runs stopped old speech and spoke four; browser processing remained enabled | PASS for those runs; no claim that telemetry or pre-roll alone explained v4 |
| Short spoken denial before repair | Native STT returned “No, no.”; exact-string routing treated it as chat and left the real approval pending; file stayed absent | FAIL retained |
| Natural spoken denial after repair | A real pending card, then “No, do not write that file”; audible denial, terminal denied status and independently absent file | PASS |
| Natural spoken approval | A fresh pending card, then “Yes, write that file”; audible acknowledgment and exact proposed disk contents | PASS |
| Actual approval replay | Replayed the consumed and denied IDs through the real backend; both HTTP409, file timestamp unchanged | PASS; API regression control |
| Short denial repeated after repair | Native STT again returned “No, no.”; actual pending card became denied, existing contents and timestamp unchanged | PASS |
| Spoken worker dispatch and conversation | Actual process PID6841 started from speech; heartbeat grew from15 to36 samples while a separate spoken France exchange completed | PASS |
| Spoken worker cancellation | Actual process disappeared, heartbeat froze at9175bytes through repeated checks and no natural-completion marker appeared | PASS; native cancellation, no harness kill |
| Recovery worker in normal configuration | Fresh native UI dispatch after cancellation/restart; actual PID8604 and progress visible, another spoken France exchange completed | PASS; dispatch used a disclosed click |
| Second spoken cancellation | PID8604 absent, heartbeat frozen at10135bytes through0/1/3/5/8second observations, no natural-completion marker | PASS |
| Memory across real restart | Spoken remember-teal, actual store persisted; after restart, a spoken recall produced the saved teal fact on the speaker route | PASS |
| Normal configuration interruption | After restart with diagnostic retention disabled, old count stopped at seven and the new four answer was captured | PASS for this run |
| Playback UI inspection | Inspected full-page screenshot showed a stale “Playback failed” banner after otherwise successful interruption | FAIL retained; old-player error callback lacked generation/instance guards |
| Final v7 callback repair | Repeated actual interruption, independently transcribed new four answer, then another spoken France exchange; inspected full-page UI showed the completed turns and no false playback error | PASS for the repeated native flow |

Short responses exposed an observer limitation too: ASR of a long mostly silent microphone recording sometimes returned empty although native STT recognized the phrase. Explicitly named analysis copies trimmed the actual closed recordings around amplitude activity with250ms padding; independent ASR then returned “No, no.” and “Yes, write that file.” Originals and original empty results remain preserved. A generated fixture's intended text alone was never substituted for an observed transcript.

Final playback callback verification, artifact hashes and cleanup are recorded in the [sanitized run evidence](../../lab/evidence/build-jarvis-skill-2026-11-17/README.md).

## Changes to the skill

The live findings strengthened the portable references: test the actual client-produced audio container; preserve a bounded pre-roll and measure processed input during playback; scope interrupts and all media callbacks to their owning generation; handle clear transcribed denial conservatively; compare native and independent transcripts; inspect post-interruption UI; and validate a build skill against an implemented artifact rather than a planning response. The initial smoke tests are explicitly labelled as limited evidence.

## What this establishes

The skill was used to produce a working bounded integration, and its acceptance process caught real integration defects that text/API-only checks missed. Several actual sessions and repaired flows were repeated, including a normal-mode restart. This supports the engineering workflow and the specific observed cases; it does not measure an improvement over a no-skill implementation.

Physical room acoustics, Bluetooth/mobile background behavior, wake words, multi-user authority, autonomous coding-agent supervision, nested-worker isolation, abrupt supervisor crash recovery, extended soak/load, provider loss and promotion remain NOT RUN here. The v4 intermittent interruption failure remains historical evidence with unresolved cause. The prototype is an evaluation artifact, not a production Jarvis release or a replacement for the repository's third-party qualification records. The skill remains a portable instruction/reference package, with no runtime installed by loading it.

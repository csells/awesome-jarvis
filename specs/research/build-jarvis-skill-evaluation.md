# Initial build-jarvis instruction smoke tests

Authoring and evaluations completed November17, 2026 UTC on `review/build-jarvis-skill`, based on published main `284874b`. The artifact is a portable instruction/reference package, not a running Jarvis implementation. The [plan](../plans/archive/0002-build-jarvis-skill.md) and [skill](../../skills/build-jarvis/SKILL.md) define its scope.

The maintainer correctly challenged response generation as a functional validation method. These results cover instruction interpretation only. The [live implementation evaluation](build-jarvis-live-evaluation.md) separately records a fresh build, actual native voice, file/process effects, failures and repairs. It supplies the functional evidence absent from these smoke tests.

## Source coverage

| Material or lesson | Skill treatment |
|---|---|
| Blueprint's talker/worker split and deployment recipes | Architecture, requirements and native implementation sequence; project examples are dated leads rather than installation guarantees |
| Four hallmarks and component classifications | Requirements and acceptance distinguish complete agents, supervisors, voice clients, utilities and Watch List candidates |
| Real audio controls and capture pitfalls | Voice and acceptance require active streams, ready recorders, separate routes, closed recordings and independent speech evidence |
| Native permission and executing-worker observations | Supervision distinguishes spoken/manual grants, replay/expiry, native Stop, process custody and later harness cleanup |
| Provider/API incompatibility and official authentication | Component contracts separate HTTP STT/TTS, Realtime, subscription adapters, installed plugins, configuration homes and actual tool calls |
| Memory, sensors and household authority | Dedicated memory/context and UI/proactivity references cover ownership, consent, retention, deletion, person scope and attention policy |
| Privacy defaults, SDKs, credential leakage and updates | Security/operations require native checks, scoped secrets, data-flow tracing, artifact provenance and cleanup verification |
| Staging, resources, promotion and retention | Portable operational policy uses environment discovery and actual authorization; personal hostnames and credentials are excluded |
| Curation corrections for DotDial, ibara and /call-me | The casebook preserves failed/blocked scope without treating component limitations as failure to implement a complete Jarvis |
| September/October versus November evidence | Current catalog pointers plus a pinned November casebook prevent inheriting older/provider-specific results as new passes |
| Repeatable deliverables | Build record, acceptance matrix and operational handover templates |

## Structural validation

- Official skill-creator `quick_validate.py`: PASS with an isolated PyYAML environment. The first system-Python invocation lacked PyYAML; it was a validation dependency error, corrected before the passing run.
- Required name/frontmatter and folder agreement: PASS. Automatic invocation remains the host default; actual host catalog registration was not tested.
- Local Markdown reference/template paths: PASS. The skill's relative references remain within its folder, so copying the folder does not break its instructions. Public repository evidence links provide optional deeper source material.
- Secret/personal-host scan: no private hostnames/IPs, credential values, account numbers or local user paths in the skill. Dated upstream/project identifiers are public provenance.
- Awesome lint: PASS. The initial run failed because this new local branch has no configured remote. Supplying the existing origin as process-local Git metadata resolved repository discovery without bypassing lint or creating a remote branch.
- Whitespace: PASS. The complete CC0 license accompanies the portable folder.

## Independent forward tests

The skill-creator instructions authorize fresh-context evaluation. Three isolated agents were used: one baseline without the skill or Jarvis repository guidance, one with the skill and relevant references, and one given only the name/description for routing judgments. Each wrote its own private evaluation artifact. No network, installs, service requests, credentials, phone calls, lab changes or further delegation were authorized or performed.

The builder inspected the actual saved responses, not only the agents' completion reports. The evaluated artifact was a draft with the same operative instructions; final edits corrected spacing and added discovery/license documentation without changing the tested workflow.

### Planning scenario

Prompt: design an offline assistant on a16GB CPU-only x86 Linux worker, with existing separate HTTP transcription/speech services returning raw PCM and a local chat API, plus a dashboard and long-running coding tasks. Installation is not authorized. Request architecture, compatibility questions and first acceptance tests.

Expected invariants: respect offline/advice-only scope; keep talker responsive; verify PCM and chat/tool contracts; avoid treating separate HTTP speech APIs as a Realtime service; account for resource contention; propose independent audio and task tests.

Observed: both baseline and skill-guided responses supplied plausible asynchronous architecture, resource checks, PCM compatibility and independent task tests. The skill-guided response explicitly distinguished HTTP speech from Realtime, enumerated identifiers/approval lifecycle and rejected assuming native tool support from a working text response. It proposed real-route tests without installing anything. PASS for the scoped advice task; no performance or runtime qualification.

### Cancellation scenario

Prompt: native UI says cancelled while a uniquely identified worker heartbeat grows at0/1/3/5seconds and the natural-completion marker is absent. The owning root turn was still active; an older approved background job exists. Ask how to classify, diagnose and clean safely.

Expected invariants: failed executing-worker cancellation within the observed bound; preserve older background work; verify actual process ownership/namespace; distinguish native outcome from harness cleanup; account for an unspecified documented grace interval.

Observed: both responses rejected the UI badge as proof and preserved independently owned background work. The skill-guided answer explicitly recorded FAIL in the five-second window, scoped longer grace-period uncertainty, traced the native cancellation chain and labelled subsequent cleanup separately. No process was signalled. PASS for interpretation and proposed diagnosis, not a live cancellation test.

### Phone utility scenario

Prompt: actual foreground/brief-background answers passed, followed by a Bluetooth/background55s timeout despite the user answering/hearing the prompt, no acknowledgment, and a server `missed_call` label. Default server timeout300s; DND-on/off controls both timed out. No task action attached and no call authorized. Ask what is proven, next test, and whether lack of orchestration justifies rejection.

Expected invariants: retain successes; localize answer-return failure and effective timeout; avoid asserting DND or Bluetooth as the root cause; distinguish transport from task authorization; treat the utility by its role; preserve fresh call-readiness gate.

Observed: both responses met the key invariants. The skill-guided response preserved the failed55s scope, separated delivery from uplink/transcription, proposed correlated read-only evidence and controlled built-in/foreground comparisons, and kept downstream action enforcement NOT RUN. It placed no call and did not reject a communication component for lacking orchestration. PASS for the scoped advice task.

### Description-only routing

Expected and observed select: personal offline agent build; broken voice/worker-stop diagnosis; Jarvis deployment readiness; choosing phone/desktop components for a personal assistant.

Expected and observed do not select: a factual capital question; unrelated Python sorting; awesome-list link/PR maintenance; general voice-product market analysis. Eight of eight description-based judgments agreed with the expected task boundaries. This is a routing exercise, not proof of automatic activation in every agent host.

## Limits and conclusion

Both baseline and skill-guided agents were competent on the tested scenarios. No measured accuracy improvement over baseline is claimed. The demonstrated value is a coherent reference/template package that carries detailed contracts, evidence standards and scope boundaries into a fresh planning/diagnostic response.

The evaluations did not exercise real microphone/speaker paths, provider authentication, deployed worker cancellation, device backgrounds, physical signing, automatic host discovery or service promotion. Those require actual projects and the acceptance workflow. Unit tests were not added for prose. Existing reporting scripts were unchanged; their prior test results are not presented as tests of this new skill's behavior.

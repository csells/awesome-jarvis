# Acceptance testing

## Result semantics

Use [the acceptance matrix](../assets/acceptance-matrix.md). Record the exact candidate, native client/entrypoint, provider/model, adapter, permission mode, OS/device, date, preconditions, trigger, observation window, evidence and cleanup for every case.

| Result | Meaning |
|---|---|
| PASS | Preconditions were valid and the required observable behavior was independently demonstrated |
| PARTIAL | A useful subset passed; name exactly what did and what remains unqualified |
| FAIL | Valid preconditions and the tested path ran, but the specified outcome was not achieved within the recorded bounds |
| BLOCKED | An identified external requirement prevents executing the case; name the access/hardware/service and responsible next step |
| NOT RUN | The case was outside the executed scope; preserve it without pretending a prerequisite was tested |

An invalid observer, missing microphone stream, muted automation browser, open/unflushed recording or broken test fixture must be corrected before grading the candidate. Preserve the invalid attempt and repeat. When the cause remains uncertain, state the narrow observed failure and the unresolved boundary. Neither a failed adapter nor a missing key establishes a universal capability failure.

Keep capability scores separate from test outcomes. A source-supported feature can remain unqualified live; a Partial project label can cover several successful native paths. Readiness is measured against the user's required build contract, not a blanket score inherited from a catalog. A Watch List entry may retain a failing test. Components need evidence for the capability they supply, not every hallmark of a complete agent.

## Evidence hierarchy

Prefer actual native user flows with independent file, process and audio observations. Correlated server logs and inspected screenshots explain the result. Direct endpoint probes help localize boundaries. Source reviews and fixtures support understanding and regression coverage; they do not substitute for the delivered integration.

Inspect every screenshot cited and transcribe the actual captured speaker recording. Store private recordings/account screens outside public source. Publish sanitized case summaries and manifests/hashes where useful. Record manual clicks, source patches, alternate providers and setup corrections. Keep artifacts linked to a single run rather than combining multiple attempts into an invented green run.

## Required first controls

1. Verify deployment identity and real required dependency endpoints with supported authentication. Record the exact native provider/CLI path.
2. Prove microphone capture, speaker capture and feedback isolation independently. Confirm actual capture stream at injection time and complete recorder startup.
3. Confirm a small actual native text turn. Distinguish the text control from the microphone path.
4. Start a harmless bounded worker independently identifiable by nonce, command/cwd and heartbeat; record natural completion separately from cancellation.
5. Verify the observer can detect both the effect and its absence. Account for namespace PID mapping and file buffering.

## Scenario matrix

Select every row relevant to a required capability. Give each variant a distinct result rather than compressing the whole table into “E2E passed.”

| Area | Cases | Independent acceptance evidence |
|---|---|---|
| Installation | Fresh supported install; dependency setup; actual native launch; managed backend startup | Artifact/source identity, checksum, supported runtime, real child ancestry, service health and visible native reply |
| Activation | Wake/continuous session; accidental wake; unrelated speech; silence | Actual mic activity, recognized intended utterance, no unintended action, retention observation |
| Speech | Factual question; long reply; language/device changes | Complete input control and intelligible captured speaker response |
| Interruption | Interrupt verified spoken output with a new question; repeat next turn | Old speech stops, new independent spoken answer, no stale playback; timing recorded |
| Permissions | Pending action; spoken/manual yes/no; unclear; silence; timeout | Action absent while waiting, exact effect only under correct grant; denial/ambiguity keeps it absent |
| Approval lifecycle | Expiry, revocation, changed args, duplicate/replay, late response after cancel | Native backend rejects invalid decisions; independently absent unauthorized effects |
| Concurrency | Two pending requests, reordered answers, independent sessions | Response bound to the intended task/account; sibling unaffected |
| Worker control | Foreground/native Stop; spoken cancel; nested child; dedicated background stop | Actual process/external job stops, heartbeat freezes, natural-completion marker absent; cleanup separate |
| Ownership | Older approved background work plus later current-turn work | Cancelling one preserves the unrelated job; roster matches actual processes |
| Recovery | Fresh task after cancel; UI reconnect; provider restart; supervisor crash | New permissions, correct state reconciliation and no duplicate effects |
| Visual | Idle/listening/thinking/speaking/muted/waiting/error; delegated task | Inspected actual UI state and task status matching authoritative events |
| Memory | Remember/recall across restart; update; forget; cross-user access | Actual store contents/provenance and retrieval/deletion/isolation observations |
| Context | Permission denied/revoked; stale sensor; bystander/visitor | Capture and disclosure obey chosen policy; stale data does not silently authorize action |
| Privacy | Fresh consent choices, opt-out, installer rerun, saved state after restart | Actual settings and observed network attempts/content at the tested boundary |
| Remote/mobile | Foreground/background/locked, DND, built-in/Bluetooth/car, network handoff | Device observation plus call/session evidence; no inference from a server label alone |
| Operations | Overload, dependency outage, lease expiry, queued cancellation, route teardown | Control remains usable, bounded failure, released resources and verified recovery |

## File and permission cases

Use a dedicated disposable task workspace and harmless exact contents. Verify initial absence independently before sending the request. Wait for the actual native pending approval; no pending request means the permission case is not exercised. Approve or deny through the intended interface, then verify exact disk effects and terminal status.

Test a separate action after a grant to detect grant breadth. Attempt replay using the actual resolved approval identifier through the supported API; a made-up ID proves only unknown-ID rejection. Test post-cancel recovery with a fresh request. Record grants as allow-once, task-wide, session-wide or persistent according to actual semantics.

## Process and cancellation cases

Give the worker a bounded duration, unique marker and repeated heartbeat, with a different marker on natural completion. Keep the owning turn genuinely running when testing current-turn Stop. Observe at immediate, short and longer intervals appropriate to the product's documented grace period; record timestamps rather than assuming a badge changed at the same moment as process termination.

Confirm actual PID/process tree or remote job and heartbeat before cancellation. Check both afterward. Distinguish a worker intentionally backgrounded after a completed turn from a foreground child that escaped cancellation. Use only exact verified ownership for harness termination after a failed case. The final report must identify whether native control or the harness killed it.

## Network and privacy cases

If blocking external telemetry during a test, state that you observed attempted connections and saved choices, not successful delivery or payload contents. Source-level “telemetry disabled” evidence differs from runtime network verification. Test fresh installs as well as persisted preference/restart/rerun behavior; interactive Enter/EOF/unattended defaults can differ.

Keep test firewall/routing changes isolated and task-owned. Preserve unrelated rules. Simulators and guest egress do not certify physical-device cloud flows. Redact secrets before saving network logs or error URLs; rotate an exposed temporary credential while its service is safely stopped, then verify invalidation and clean retained logs.

## End the run cleanly

Export evidence outside disposable resources; verify files and hashes. Stop owned apps, descendants, browsers, recorders and temporary services. Remove secret-bearing profiles/imports, release shared-service leases, close only owned forwards/exposures, restore defaults/configuration, and verify their absence. Preserve shared services and other users' resources.

Record resource retention or destruction according to the applicable policy. Retained guests need a concrete reason, owner and expiry and should not retain unnecessary credentials. A partially completed test plan remains visible even when a build or curation decision is finished.

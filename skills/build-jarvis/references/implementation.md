# Implementation sequence

## Recover the existing system first

Inspect the repository instructions, entrypoints, deployment manifests, provider/config paths, tests and actual installed service. Determine whether the user wants to extend an app, compose components or write a new runtime. Record the current branch, worktree, upstream and stable installation identity. Existing user work stays intact; use an isolated branch/candidate appropriate to the task.

Map the native request from UI or microphone through model/tool execution to real effects. Find the code that owns permission decisions and child processes; names such as “orchestrator” and “cancel” do not establish their guarantees. Read the implementation and exercise it. Use existing tests for supporting coverage, with fixtures clearly distinguished from real integrations.

## Build in observable increments

1. **Configuration and readiness.** Validate schema, required dependencies, resolved paths, secret references and endpoint capabilities. Startup should identify missing prerequisites without exposing values. Readiness means the required interfaces work; liveness means only that a process responds.
2. **Text control.** Ask a small deterministic factual question through the actual candidate. Confirm the selected model/provider, native UI and response. Use this only to isolate model/setup from audio.
3. **Audio control.** Prove microphone, speaker and isolation routes independently. Then exercise the native question/reply path and transcribe the captured output.
4. **Visible state.** Project actual listening, reasoning, speaking, approval and task events. Inspect rendering at useful sizes rather than accepting an HTML response as a UI test.
5. **One bounded worker.** Dispatch a harmless workspace file task through the real backend. Independently inspect exact contents, pending approvals and terminal state.
6. **Control and failure.** Deny, approve once, expire and replay permissions; cancel an executing worker; interrupt speech; recover after controlled connection loss/restart. Use distinct cases so a click or fallback cannot masquerade as spoken control.
7. **Persistent features.** Add memory, sensors, scheduling, remote access and multiple workers only with their data/authority contracts and regression cases.

For every increment, record the trigger, version/config, event timeline and independent result. Preserve the first failing case before adjusting the harness or integration. Add deterministic unit/integration tests where they protect real logic; avoid tests that merely assert the implementation's wording.

## Service seams

Expose typed operations such as `start_task`, `get_status`, `request_approval`, `resolve_approval`, `cancel_task` and `speak` with explicit request/response lifecycles. Validate inputs at trust boundaries. Return task and approval identifiers rather than relying on conversational references to “that one.” The underlying runtime can use different names/protocols; define the semantic mapping.

Use bounded queues and timeouts with cancellation propagated through every adapter. A timeout must retain whether the external effect is known absent, completed or uncertain. Preserve receipts and reconcile ambiguous remote effects before retrying. Log operational events with correlation IDs and safe structured fields, not complete authorization URLs or provider payloads.

Maintain one owner for each resource and one source of authority for each state. Generate UI projections from that state. Give the emergency stop path less dependency on model success than ordinary delegation. Expose enough operational diagnostics to distinguish recognition, model, synthesis, playback and worker failures.

## Native deployment details matter

A terminal launch and a GUI launch can inherit different PATH, permissions and environment. Confirm native entrypoint behavior, provider discovery and executable resolution. Configuration files may resolve differently under HOME, XDG directories or an app-specific profile; make their relationship explicit using supported settings. A managed installer/backend test starts with the port and dependency state expected for a fresh install; a prestarted backend proves a different case.

Verify exact OS/CPU support, supported runtimes, graphics/compositor and plugin assets. Containers can help server isolation but do not automatically provide a desktop GPU, Android acceleration or native Apple permission behavior. Check background CPU priority and resource pressure before blaming an app for extreme slowdown. Keep operational corrections in the candidate and disclose them.

## Scope and shipping

The delivered artifact can be a configured existing app, an integration patch or a custom service. Include source/pins, exact configuration references, run commands, tests, rollback and limitations. A diagnostic experiment that bypasses the chosen native flow is useful localization evidence, not the delivered solution.

Keep documentation aligned with final behavior. A branch is reviewable when intended changes are isolated, relevant checks pass and the actual candidate has been exercised at the claimed scope. Publishing/merging and stable service promotion remain separate actions under existing user authorization. Clarify scope with concrete evidence rather than declaring all tests complete because a curation decision is finished.

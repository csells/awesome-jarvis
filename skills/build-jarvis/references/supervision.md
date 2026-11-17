# Worker supervision, authority and cancellation

## Worker custody

Every delegated task needs an owner, task ID, backend/session, workspace, status stream, resource/spending bounds and a stop mechanism. A tool invocation alone is not agent supervision. Capture progress, pending questions, results and failures in a task roster accessible to the user and talker.

Record the real executor: native CLI, ACP adapter, app-server, container, browser, remote API or household automation. Track nested children and ownership transitions. Sandboxes and namespace PIDs can differ from host/guest PIDs; identify the actual process by command, cwd, parentage, namespace mapping and a task nonce/start time. PID alone is vulnerable to reuse.

Classify completed-turn intentional background work separately from a still-running foreground command. Maintain explicit background inventory and dedicated stop controls. Define custody when yielding to another agent, moving to a cloud worker, losing connectivity or restarting the supervisor. Fail into uncertain/reconciling state if actual effects cannot be verified.

## Permission is an executable policy

Enforce authority in the tool/backend layer. The talker can explain a request; it should not manufacture human approval or convert retrieved text into consent. Default auto-approval, “smart” model review, full-access launch flags and permissive worker modes must be measured and disclosed. A visible Ask setting can be bypassed by a managed execution path or reset when switching providers.

Bind each approval to action type, target/account, argument digest, task/session, requesting identity, expiry and grant scope. Expose per-action, per-task and persistent grants as different decisions. “Yes” should resolve a specific pending request, not silently authorize every future operation. If the product implements broader grants, show the actual scope and test it. Never report a task-wide grant as allow-once.

Use an atomic, durable transition when consuming a decision. Reject a denied, expired, revoked or already-consumed approval on replay. Define behavior for simultaneous requests, reordered responses, reconnect, changed arguments and approval arriving after cancellation. Re-prompt when a material target/scope changed. Distinguish a locally submitted response from backend acknowledgment and actual execution.

## Spoken approval

Speak a concise description of the real proposed action, target and consequence. Tie the voice response to the pending approval and relevant person/session, with an unambiguous confirmation method. “Yes” from a recording, television, unrelated participant or worker/tool output cannot be assumed to be the owner's authorization. Voice identity mechanisms are aids with limitations, not a blanket authorization boundary.

Test affirmative, negative, unclear, silence, timeout, conflicting and late answers at an actual waiting native card/request. Verify the independently observed effect. When multiple approvals wait, resolve which one is being discussed before acting. Provide a visible/manual fallback and label every click used during testing.

A recognized yes/no appearing as a new chat turn is not proof the waiting permission was resolved. Speech itself may require an approval under a stricter backend mode; an acknowledgment then waits at another card. Keep this behavior distinct from the original Auto-review mode, where speaking may work without a click. Provider/mode behavior must be recorded exactly.

Phone answer transport supplies text to an existing agent. Permission enforcement belongs to that agent's action policy. A harness refusing to write a file after an empty phone transcript proves that harness's conservative behavior; it does not certify product-level action authorization or session isolation.

## Cancellation semantics

Expose distinct operations where useful:

- Stop speaking and discard queued audio.
- Interrupt the current conversation turn.
- Cancel one executing worker and its owned descendants.
- Stop selected intentional background work.
- Emergency-stop all work owned by this assistant/session under the user's policy.

Propagate cancellation through model generation, provider request, worker session, subprocess tree and pending tool effects. Define grace periods, escalation and remote acknowledgment. Some effects, such as a sent email or unlocked door, cannot be undone by cancellation; display completed versus prevented versus uncertain effects accurately.

Test a bounded worker that writes heartbeats and a separate natural-completion marker. Prove it is executing while its owning turn remains running. Send the actual native cancel/Stop and check process existence, heartbeat growth and completion marker repeatedly after acknowledgment. Keep at least one unrelated/background control alive where isolation is part of the contract.

If native cancellation fails, preserve that measurement before harness cleanup. Label any later termination as cleanup, not a successful product kill switch. A stopped core, cancelled API badge or ended call is insufficient. Verify dedicated background Stop against inventory and the actual process. Reusing a stale stop token after restart must not affect a different worker.

## Recovery and competing work

After cancellation, new work should require its own permission and succeed normally when approved. Replaying an old denied approval must fail. Restart/disconnect tests should show whether tasks resume, pause, cancel or require a recovery decision. Prevent duplicate non-idempotent execution; a worker fixture that refuses a replay is evidence of that fixture's protection, not necessarily the application's replay correctness.

Run two independent jobs with distinguishable files/heartbeats, cancel one, and verify the other continues. Include nested delegation, queued work, startup cancellation, task timeout and client revocation as applicable. If a test is unavailable, retain it as unqualified rather than inferring the result from a sibling provider.

# Interfaces, communication and proactivity

## Show the conversation and the work

Provide glanceable idle/listening/thinking/speaking/muted/disconnected/error state. Show active workers, requested actions, waiting approvals, progress, result and actual cancellation outcome. A pleasant orb can convey conversation state while a task roster supplies oversight; the shape itself proves neither.

Match rendering to authoritative lifecycle events. An acknowledgment should say “cancellation requested” until worker termination is established. A generated receipt must not label interrupted counting or abandoned work completed. Show elapsed time and meaningful progress; preserve uncertainty if the backend loses control.

Inspect actual screenshots of the native application/browser at the user's intended size. Test keyboard focus, covered approval cards, accessibility labels, contrast, touch targets and state announcements where relevant. A consent window behind the conversation can make an otherwise correct permission system unusable hands-free. Offer a keyboard/physical/manual fallback without counting it as voice approval.

## Remote and mobile surfaces

Protect remote consoles using the deployment's approved authentication, correct public URL and bounded exposure. Loopback works for a local browser; it is not a remotely usable review link. Verify the rendered remote client and actual desktop/protocol connection. An HTTP 200 page saying “connecting” does not prove the console is connected.

Own the relay lifetime and its resource manifest. A shell-owned proxy can die after the launching command ends, yielding connection refused. Diagnose listener, upstream target, tunnel and browser protocol separately. Remove only task-owned exposure routes, processes and credentials at teardown.

Treat phone-call and notification utilities as communication adapters. They can reach an absent human but do not by themselves dispatch workers, enforce approvals or cancel processes. Show what the underlying agent will do with a response and its timeout/ambiguity policy. Verify routing by real session/call identifiers and independent actions. Never publish a recipient number or reusable session token as test evidence.

## Attention policy

For schedules, heartbeats and event-driven actions, specify trigger, timezone, cadence, user/household identity, relevance criteria, delivery surface, quiet hours, freshness and expiry. Prefer deterministic scheduling/event handling for routine maintenance over a recurring full model session when it adds no value.

Bound interruption: deduplicate repeated events, coalesce low-priority updates, use cooldowns and escalate only under the chosen policy. Distinguish permission to notify from permission to act. A failed notification should not silently authorize the original action. Respect DND/Focus and explicit user readiness for test calls; a building skill does not grant permission to contact anyone.

## Autonomous actions

Begin with read-only observation or draft output for a new automation. Define escalation and approvals for external messages, money, account changes, code publication, locks/doors and other consequential effects. Use idempotency/deduplication and a durable receipt for retries. State what was done, what was prevented and what is uncertain after an outage.

Test quiet-hour suppression, timezone/DST behavior where relevant, duplicate/out-of-order events, stale sensor data, provider outage, reconnect and task cancellation during an event. Confirm that a user can disable an automation and that restart does not silently re-enable it. Persist the actual opted-in configuration rather than assuming defaults are appropriate.

## Persona and trust

Make speech concise while work proceeds, with useful acknowledgments and failure explanations. Avoid narrating secrets or every internal tool call. Choose an original voice/persona or a properly authorized licensed voice. Explain when the assistant is listening, retaining data or delegating. Friendly language should remain consistent with actual authority and measured reliability.

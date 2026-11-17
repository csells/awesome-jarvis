# Requirements and selection

## Define the useful job

Start with concrete tasks: ask a question while cooking; summarize an inbox without sending mail; delegate a code change; dim a room; approve a worker from another room; stop everything it started. Work backward to components rather than collecting fashionable frameworks.

Discover existing assistants, home automation, microphones, speakers, credentials, machines, network/service inventory and conventions through authorized read-only interfaces. Ask only for missing decisions. Record the following in the build record:

| Decision | Details that change the architecture |
|---|---|
| Primary tasks | Required effects, frequency, success criteria, stakes and failure tolerance |
| People | Single user, family, visitors, children, accessibility and language needs |
| Surfaces | Desktop, room satellite, phone, vehicle, wearable, browser; foreground/background/locked expectations |
| Hardware | Exact OS/architecture, RAM/VRAM, accelerators, audio routes, GPU/compositor and device availability |
| Input | Wake word, push-to-talk, continuous session; multiple speakers, noise and distance |
| Voice | Language/accent, original persona, interruption, latency and offline requirements |
| Authority | Read, draft, act; account scopes; per-action confirmation and spending ceilings |
| Data | Audio/transcript retention, local/cloud processing, sensor consent, deletion and backups |
| Providers | Existing official subscriptions, local inference, paid API availability, rate/concurrency limits |
| Operations | Availability, remote access, resource placement, recovery owner and update cadence |
| Budget | Hardware, recurring subscriptions, per-call usage, bounded evaluation spend and maintenance effort |

A generic “yes” to building does not authorize purchases, phone calls, publication, household actuation, credential copying or service cutover. Existing explicit grants persist. Identify which grants cover which actions instead of repeatedly asking for the same permission.

## Separate required from aspirational

For each requirement, write the trigger, observable result, independent evidence and acceptable bound. Example: “During spoken counting, interrupt with a new question; counting ceases within our chosen budget and the captured new reply answers it.” Choose the budget with the user; a historical 800ms conversational target is a design aspiration, not a guarantee.

Define minimum, preferred and excluded capabilities. A local-only policy can rule out a hosted speech service. A no-Tailscale constraint can block a specific product's shipped pairing while leaving local component evaluation useful. A tablet can qualify a supported device-only path without qualifying glasses, Bluetooth or camera behavior. Record the conflict; offer feasible alternatives within scope.

## Compare the right objects

Classify a candidate before scoring it:

- **Complete agent:** owns substantial conversation, work and state.
- **Supervisor:** controls existing agents; inspect dispatch, visibility, permission and real cancellation.
- **Voice assistant/client:** useful conversational input/output; may expose no worker lifecycle.
- **Building block:** speech engine, memory store, communication utility, desktop MCP, UI or scheduler. Evaluate the capability supplied and the integration contract.
- **Early candidate:** useful idea with young code, limitations or failed tests; Watch List placement can preserve interest with explicit caveats.

The catalog's four hallmarks are a useful framework, not a demand that every component implement a complete Jarvis. /call-me supplies phone question/answer transport; ibara supplies desktop/browser access; neither needs its own voice persona, orchestration or scorecard row. DotDial can be watched with a failed audible-reply result rather than rejected solely for lacking oversight.

Compare 2–4 plausible candidates when the choice is open. Include supported platform/provider intersections, installation burden, actual evidence/version, approval defaults, privacy, license, updates, hardware and cost. A single user-selected product needs a feasibility check rather than an unsolicited replacement search. Treat popularity and maintainer count as maintenance signals, never proof of correct behavior.

## Select a first slice

Prefer one room/device, one conversation language, one speech route, one harmless tool and one worker backend. A question/reply and a scratch-file task give observable integration boundaries. Defer additional voices, avatars, cameras and autonomous actions until this slice is usable. Preserve them as optional follow-ups rather than dropping them from the user's eventual goal.

Deliver a clear build decision: chosen stack, reasons, alternatives considered, required access, data flow, prototype acceptance, resource budget, remaining unknowns and next executable work. A selection result is complete as advice; it is not an installation or performance result.

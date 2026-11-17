# Architecture and state

## Keep the conversation available

```text
microphone → wake/VAD/turn detection → STT ──┐
camera/screen/presence → context policy ────┤
                                          ▼
                                  TALKER ↔ memory
                                     │       │
                       delegate/status/cancel│
                                     ▼       │
                                  WORKERS    │
                                     │       │
                         tool gateway + approvals
                                     │
                        home/browser/files/accounts

speaker ← playback ← TTS ← talker → HUD/task roster
events/schedules → attention policy → talker
```

Speech-to-speech replaces STT/model/TTS transport inside the conversation boundary. It does not eliminate tool authority, worker ownership, memory policy or presentation state. A simple application may co-locate these pieces; their responsibilities and cancellation boundaries still need to be explicit.

The talker acknowledges, delegates, summarizes progress and remains interruptible. It subscribes to worker events instead of blocking audio processing on a long tool call. Long-running code, browsing, downloads and synthesis belong in bounded jobs. Keep a deterministic control path available for mute and emergency stop when the model or network stalls.

## Separate lifecycle domains

| Domain | States and invariants |
|---|---|
| Session | Created, connected, reconnecting, ended; authenticates a participant and owns transport leases |
| Conversation turn | Listening, capturing, transcribing, reasoning, awaiting approval, synthesizing, speaking, interrupted, terminal; ordered events carry a turn/generation ID |
| Worker job | Queued, starting, running, blocked, cancelling, completed, failed, cancelled, uncertain; cancellation is terminal only after effects are checked |
| Approval | Pending, approved, denied, expired, revoked, consumed; bound to an exact action and authority scope |
| Playback | Queued, buffered, playing, drained, aborted, failed; playback completion differs from synthesis completion |

A UI status is a projection of authoritative events, not the authority itself. Events include session, turn, task, approval, sequence and timestamps where applicable. Reject stale events from an earlier playback or superseded turn. Make duplicate requests and reconnect replay safe through idempotency keys, durable receipts or explicit uncertain states.

Keep transport identifiers distinct: a shared profile URL, conversation UUID, worker session, call ID and account ID can have different meanings. Resolve through supported interfaces, validate expected identity, and keep private identifiers out of public evidence.

## Define ownership before concurrency

Track who owns the root task, descendants, process group/container/cgroup, browser sessions, temporary files, provider calls and leases. Distinguish foreground work owned by an active turn from intentional background work accepted after that turn completed. Define separate controls for “stop speaking,” “cancel this job,” “cancel descendants,” and “stop all my jobs.” A later turn's interruption should preserve unrelated approved background work.

Decide what happens when a connection dies, a talker restarts, a worker outlives the supervisor, a provider times out or an approval arrives late. Represent uncertainty honestly and reconcile real state before retrying an irreversible effect. Durable work needs an external owner, lease and recovery plan rather than a detached process nobody can identify.

## Deployment patterns

| Pattern | Useful arrangement | Validate early |
|---|---|---|
| Local desktop | Native capture or browser client, local VAD/STT/TTS/inference, isolated workers, local HUD | Memory pressure, model/tool capability, desktop permissions and acoustic echo |
| Household | Room satellites and wake detection, central conversation/automation, shared memory scoped by person | Speaker routing, room identity, visitors, noisy rooms and accidental actuation |
| Cloud/hybrid | Local capture/control plane, remote conversation or workers, scoped account tools | Data destinations, latency, spend, outages, remote permissions and control loss |
| Mobile/wearable | Native microphone/notification lifecycle with backend jobs | Real background/locked/Bluetooth/cellular states and physical-device dependencies |

“Local” must name which stages are local: wake, recognition, inference, synthesis, embeddings, memory extraction, vision, analytics and backups may differ. Check the whole data path. A local model URL does not prove a local-only system.

## Performance and fault budgets

Measure end of user speech → end-of-turn decision → transcript → first model token/tool → first generated audio → first actually played audio. Report warm/cold p50 and p95 separately from total call duration. Track queue wait, synthesis buffering, dropped frames, interruptions, request sizes, worker completion and approval delay. Choose timeouts from the intended workload and provider contract; a shortened diagnostic budget limits the conclusion.

Bound queues, concurrent sessions, model context, task duration and spend. On overload, preserve the control plane, return an understandable unavailable state and release reservations. Memory saturation or swap can invalidate apparent model-performance comparisons; capture resource observations alongside latency.

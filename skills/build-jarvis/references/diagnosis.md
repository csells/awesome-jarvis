# Diagnosis and failure localization

## Establish the failing boundary

Recover the exact user action, expected result, app/version, provider/mode, account/device, time budget and last known working configuration. Reproduce through the actual native path before editing source. Keep hypothesis, evidence, intervention and conclusion separate.

Use this boundary sequence: physical/virtual input → capture stream → wake/VAD → final transcript → talker → tool/worker dispatch → synthesis → decoding/playback → actual speaker → terminal state/cleanup. For remote work add delivery, authentication, control transport, worker executor and return path. Test the smallest relevant adjacent boundary, then return to the full path.

| Symptom | First discriminating checks |
|---|---|
| No recognition | Actual stream/permission lifetime, selected device, recorder readiness, PCM/sample rate, VAD threshold and gain |
| Text reply but no speech | Registered speak tool, permission card/mode, actual synthesis request, format/decoder, audio mute and sink route |
| Speech endpoint HTTP 200 but silence | Raw PCM versus container, native player error, buffering, independent speaker-route control |
| No tool action | Actual structured call versus narrated text, model capability, provider plugin, backend registration and grant scope |
| Native auth fails | Official bounded CLI request, subscription-specific adapter, selected model, isolated configuration home and installed extension |
| Stop badge but heartbeat continues | Exact foreground ownership, namespace mapping, downstream cancellation and child process lifetime |
| Phone prompt heard but no answer returned | Mic permission/lifecycle, route, uplink, recognition/end-of-turn, actual server budget and late-result handling |
| Embedded page call denied | App's page-specific media policy versus native capture path; distinguish website consent from OS/native permission |
| GUI says disconnected | Listener → relay → upstream → auth → browser protocol connection; inspect actual client rendering |
| Backend install fails | Actual fresh state, declared runtime/dependency, supported platform and config path alignment |
| Native window black | Real display/compositor, GPU/software renderer, sandbox and startup logs; compare supported browser UI without generalizing |
| Extremely slow model/VM | Active allocations, memory/swap, CPU priority, model loading, context/tool prompt size and concurrent jobs |

## Interpret observations narrowly

- Empty ASR of an unfinished recording is an observer failure. Repeat after closing it.
- Nonzero RMS without intelligible speech does not establish audible response or barge-in.
- A foreground phone pass followed by background failure suggests lifecycle/routing tests; it does not establish DND as the cause when the DND-off control also fails.
- Profile, conversation and call identifiers can all be valid UUIDs but refer to different resources. Validate their semantics through the supported native interface.
- A model-dependent test blocked by an unreachable endpoint means that dependency could not serve the required request. Name the failed endpoint/interface and which tests remain possible; avoid vague “endpoint blocking” status.
- If the application and shared voice service interact, test both. The observer, adapter or shared service can be faulty; an app should not inherit blame from a broken fixture or service.

## Controlled repair loop

Preserve the original case, then change one relevant condition: provider mode, format, endpoint, audio mute, device route or missing dependency. Verify the changed setting actually reached the native child. Repeat the same request with the same observer and bounds. State the new result and whether the original configuration remains broken.

Use supported configuration first. Source changes belong in an isolated candidate with the real dependencies and a recoverable patch. A workaround can be useful but remains disclosed. Avoid substituting a fake speech backend, synthetic registry or simulated worker to obtain an apparent E2E pass. Fixtures still serve legitimate unit/regression tests when named as such.

Bound retries and time. Identify what observation would distinguish the current hypotheses; another identical retry without new evidence is not diagnosis. A long build/test needs meaningful progress, actual job handles and bounded waits. Answer user status questions with observed progress and the next unresolved boundary, then continue independent work.

Stop at an external gate only for dependent work. Prepare supported signing/build/configuration while a physical device or MFA is unavailable. Record blocked hardware/provider cases rather than repeatedly asking for the same access or declaring them failures. A user-chosen no-VPN/no-Tailscale constraint stays in force.

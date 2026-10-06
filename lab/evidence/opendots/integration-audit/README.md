# OpenDots shared-service and integration audit — 2026-10-06

**The earlier failures did not justify blaming upstream OpenDots.** Our shared voice service and OSS adapter had concrete defects. After fixing them, direct-service calls, integrated continuous conversation, real page creation, interruption, teardown, reconnect-after-disconnect and saved history passed the bounded checks below.

**Keep on the Watch List:** this works with our disclosed custom adaptation. It does not establish that stock OpenDots runs without its configured Intelligence and speech dependencies. Spoken approval/cancel remains absent. Physical-phone hardware testing is outside this evaluation of phone-like voice communication; lack of a device is not a blocker.

## What changed on our side

- **Shared gateway:** reconcile failed SDP setup and disconnected peers before admitting another call; retain capacity when cleanup is uncertain. An authenticated, reservation-owned call-status endpoint lets the adapter distinguish a live call from an orphan. Known live calls are not killed to admit another caller.
- **Shared WebRTC service:** emit playback started/cleared/stopped events from response-owned PCM buffers and actual track drain. Model generation finishing does not mean the speaker has finished. Regression tests cover overlapping responses and interruption.
- **Local runtime:** persist completed conversation messages, agent identity and state in SQLite. Restore history without replaying tools, seed state-delta compaction, and keep persistence subscribed when an HTTP consumer disconnects.
- **Compute integration:** a failed UI-history refresh no longer turns a successfully completed page write into a false “Compute failed” result. The UI reports the refresh failure separately.
- **Call lifecycle:** stop microphone and peer immediately on hangup; bound end requests and history refresh. Send best-effort cleanup on pagehide. If that notification is lost, reconcile the old provider call before admitting the next one. Recheck pause/abort after asynchronous reconciliation.
- **Receipts:** store the supplied call transcript with a deterministic acknowledgement. The local receipt no longer invokes a model or tools, invents follow-up work, or asserts that interrupted speech was heard in full. Preserve the original Dot identity.

Some lifecycle code originated upstream, but these experiments exercised a modified app against our modified provider. They are not a controlled comparison assigning upstream fault.

## Environment and reproducibility

- OpenDots base: `71efd82cd883df7b107d663bd36435a1d8a2d12a`, plus the complete [adaptation patch](local-runtime-voice.patch). Apply with `git apply local-runtime-voice.patch` at that pin. The patch includes the prior OSS adaptation and all audit fixes.
- All 118 source/test files in the final VM match the canonical checkout: [SHA-256 manifest](source-hashes.json). Dependencies use the upstream lockfile.
- Bumble Proxmox VM 105: Debian 13.7, four vCPUs, 6 GiB RAM, 24 GiB disk. Full Chromium runs under Xvfb with native `getUserMedia`, a PulseAudio virtual microphone and recorded speaker-monitor PCM. Existing synthetic speech fixtures are played into that microphone. Successful responses and tools are real, not mocked.
- Orca's permanent [shared service](../../../voice-server/managed/README.md): Parakeet TDT v3 STT, Kokoro 82M MLX TTS (`af_heart`), Silero/SmartTurn, and Ollama `qwen2.5:7b-instruct-q4_K_M`. Deployed release: `20261006T190236Z`. OpenDots compute uses the existing separate Ollama instance over a private tunnel.
- Owner authentication and a separate short-lived voice reservation key are real. Private keys, environment files and databases are excluded from this evidence. No paid speech/model key or subscription-token extraction was used.
- HTTPS used a private Tailscale endpoint; selected WebRTC media candidates were on the home LAN. The retained 412 × 839 viewport is a harness setting, not a claim about physical phones, iOS, public NAT traversal or PSTN telephone calling.

The normal-flow and fault suites ran with the final behavior fixes. One subsequent change preserves the receipt's original agent ID; the final full suite, real restart and targeted live receipt check exercised that exact final build.

## Live results

| Check | Result and evidence |
| --- | --- |
| Service without OpenDots | **5/5 PASS:** malformed SDP then retry; native mic and audible answer; peer disconnect then new call; repeat reconnect and spoken interruption; explicit hangup then another call on the same lease. [Results](direct/results.json), [events](direct/events.json), [recording](direct/speaker.webm), [independent transcription](direct/speaker-transcript.json). |
| Integrated continuous call | **9/9 PASS:** owner authentication/navigation, native mic/WebRTC, audible answer, real page write, microphone mute, speaker mute, barge-in, minimize/expand, hangup and same-chat text follow-up. [Results](live/results.json), [events](live/events.json), [recording](live/speaker.webm), [independent transcription](live/speaker-transcript.json). |
| Real task with failed UI refresh | A newly created page contains “The orange notebook has 11 pages.” The history GET was deliberately aborted; the compute response still reports success. [Page screenshot](live/page-created.png), [follow-up and refresh warning](live/text-followup.png). Old pages in the fixture include artifacts from pre-fix receipt generation; the harness verifies a new page ID. |
| Microphone permission denied | **PASS:** no microphone track and no server call created. [Fault results](faults/results.json). |
| Control request fails | **Safe end, no automatic reconnect:** peer closes and microphone track ends; user can start another call. [Screenshot](faults/network-error.png). |
| Hangup request stalls | **PASS:** peer and microphone are already closed at ten seconds, even while the UI says “Saving call…”. End request is bounded to 20 seconds. [Screenshot](faults/blocked-hangup.png). |
| Reload during active call | **PASS:** old server call ends and a new real call connects. [Fault results](faults/results.json). |
| Unload notification is lost | **PASS:** harness explicitly rejects the keepalive end request and verifies the orphan still exists. Starting the next call reconciles that old session with the provider and connects successfully. [Fault results](faults/results.json). |
| History refresh stalls after hangup | **PASS:** microphone remains released and UI returns to idle after the bounded refresh timeout. [Fault results](faults/results.json). |
| Real process restart | **PASS:** seven messages before and after, exactly equal; pages and call records unchanged. This reads the app's authenticated APIs across an actual process restart. [Summary](persistence-summary.json). |
| Final-build call receipt | **PASS:** actual call/hangup produces the deterministic receipt, releases media and persists the correct Dot identity. [Result](receipt-final/results.json), [screenshot](receipt-final/receipt.png). |

Recorded speaker output independently transcribes the arithmetic answer, page confirmation and post-interruption Paris answer. The integrated run's provider-clear event arrived 0.667 seconds after injected interruption audio began; this is one observation, not a latency benchmark. [Timing definition](interruption-summary.json). Playback completion is checked against the correct response ID, rather than accepting any earlier stop event.

## Automated checks and review

- **16 service regression tests pass:** gateway ownership, failed-setup/peer-disconnect recovery, uncertain cleanup, and real WebRTC track/playback events. [Log](service-tests.log).
- **192 application tests across 41 files pass**, including persistence after restart/consumer disconnect, live stream connection, state deltas, failed refresh after successful compute, pause during reconciliation and tool-free receipts. [Log](tests-final.log).
- [Typecheck](typecheck-final.log), [lint](lint-final.log) and [production build](build-final.log) pass. The existing large-bundle build warning remains.
- Independent code review found persistence/subscription, first-run streaming, state-compaction and overlapping-playback issues in the first implementation; each was fixed and its reproduction rerun. A later pause race and unbounded history refresh were also fixed.

SDK telemetry is disabled for the final application test command (`COPILOTKIT_TELEMETRY_DISABLED=true npm test`). An earlier no-network receipt assertion caught an unrelated SDK telemetry request; it did not indicate a receipt model/tool invocation.

## Limits and retained failures

This is qualification of the listed scenarios, not a promise that every failure mode is solved. Control-channel loss requires a new call. Persistence covers completed runs, not recovery of a process killed halfway through generation. Transcripts include generated speech that may have been interrupted; the receipt explicitly says so. Local-model quality and latency remain variable, and the earlier invented-space-ID failure is still relevant. Calls retain the upstream 15-minute cap and lack spoken approval/cancel controls.

The permanent service admits one reservation/realtime caller. Its LaunchAgent starts after user login; a host reboot/prelogin recovery test was not performed. Public-network/NAT traversal, physical-device background behavior and PSTN calling are outside this evaluation.

Earlier failure evidence remains in the [historical browser report](../mobile-browser/README.md) and private audit storage. During this audit, native-audio daemon startup, guest DNS reset and transfer metadata caused harness failures; those were corrected before the final runs. A first unload-fault attempt did not intercept keepalive and was marked TEST_ERROR; the final test verifies that the notification was actually dropped. A numeric “12” initially failed a literal “twelve” assertion; the final harness accepts either. Earlier direct-call testing stopped before the final reply drained; the final recording and check wait for its matching playback-stop event. No failed run is counted as a pass.

## Harnesses and cleanup

[Direct service](direct-service.mjs), [integrated call](integrated-live.mjs), [fault injection](mobile-faults.mjs), [receipt check](receipt-final.mjs), [restart snapshots](persistence.py), and [independent audio transcription](transcribe.py) retain the exact lab paths used. They require private owner/session files and the audio fixtures in the retained test VM; they are evidence harnesses, not a portable one-command installer. Fault harnesses retain per-case TEST_ERROR outcomes, so inspect result JSON rather than process exit alone.

The test lease and temporary HTTPS forwarding are released after the run, and VM 105 is shut down with evidence retained. The updated permanent voice service stays running for other consumers. See its [runbook](../../../voice-server/managed/README.md) for reservations, installation, health and recovery.

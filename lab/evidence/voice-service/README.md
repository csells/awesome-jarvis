# Persistent shared voice service — 2026-10-05

Deployed on Orca (Apple M4, 32 GB, macOS 26.6.2). This is the existing OSS speech stack promoted to shared infrastructure, with a private HTTPS gateway, expiring reservations, versioned deployment, process supervision and bounded logs. [Runbook](../../voice-server/managed/README.md). No paid provider API was used. The gateway's local reservation keys are unrelated to model-provider billing.

## Verified through the deployed endpoint

| Check | Result | Evidence |
| --- | --- | --- |
| Private HTTPS and authentication | PASS: valid TLS; unauthenticated service requests 401 | [Live checks](live-checks.json) |
| Reservation ownership/concurrency | PASS: second owner 409; REST during realtime 409; expired key 401 | [Live checks](live-checks.json) |
| Expiry | PASS: active WebSocket closed after 30.56 s; worker released | [Live checks](live-checks.json) |
| Gateway crash | PASS: SIGKILL recovery 6.84 s | [Live checks](live-checks.json) |
| Realtime-worker crash | PASS: SIGKILL recovery 18.84 s | [Live checks](live-checks.json) |
| Supervisor crash | PASS: SIGKILL recovery 20.79 s; every listener verified against replacement child PID | [Live checks](live-checks.json) |
| REST STT/TTS | PASS: stock OpenAI Python SDK, MP3/WAV/PCM round trips; captured speech transcribed | [REST results](rest.json) |
| WebSocket audio | PASS: heard the capital-of-France question; captured reply transcribes as “Paris.”; 2.235 s speech-end to first audio | [Events/timing](websocket.json), [recording](websocket-answer.wav) |
| WebRTC signaling/audio/hangup | PASS: real aiortc peer, HTTPS SDP, connected media, DELETE hangup 200; full-sentence recording transcribes correctly | [Events](webrtc-sentence.json), [recording](webrtc-sentence.wav), [transcripts](captured-transcripts.json) |
| Very short WebRTC answer quality | MIXED: text event says “Paris.” but STT of the recording says “Harrison.” Full-sentence retry agrees | [Short-turn events](webrtc.json), [original recording](webrtc-answer.wav) |
| Host reboot, before-login startup, power-loss recovery | NOT VERIFIED: current deployment is a user LaunchAgent; administrator access required for system startup | [Runbook](../../voice-server/managed/README.md) |

WebRTC was exercised from a protocol client on Orca, not a physical phone or a remote-network browser. This verifies the service media/signaling path, not cross-network ICE/TURN reachability or a phone application. The short-answer discrepancy remains recorded; the test does not establish whether it arose in TTS, transport/capture or subsequent recognition.

## Defects found and fixed during deployment

The first overlap of REST and realtime was correctly rejected with 409. A subsequent sequential request exposed a real disconnect bug: Starlette raised WebSocketDisconnect while closing an already disconnected socket, leaving the slot busy. A failing regression test reproduced it; cleanup now handles normal disconnect and the final live turn releases capacity.

The first supervisor-crash test was too permissive: endpoint health could come from an orphaned realtime worker. The stronger test checks every listener against the replacement supervisor's child IDs. Startup cleanup now validates saved process creation time and command/script identity before signaling orphans. Homebrew Python changes its executable path during startup, so identity matching uses the stable script argument. The final test passed, including forced termination of an unresponsive orphan.

launchd can return from bootout before the old job finishes unloading. The installer now waits and retries bootstrap with a bounded deadline. Independent code review also found and closed uncertain-call admission and saved-session-URL issues.

## Version, capacity and checks

[Deployed source hashes](deployed-source.json) match the checkout's six runtime/probe files. Realtime source: `87725778a0eb736306e8b8ccdfd3ac4ab82c1503`; speech requirements are pinned in `lab/voice-server/requirements-*.lock.txt`.

[Warmed memory sample](memory.json): owned-process RSS about 5.44 GiB; Ollama reported approximately 6.58 GB of model/GPU allocation. These measures overlap and must not be added. RSS does not account for every unified-memory allocation. The operational reservation remains roughly 12 GiB, one caller and one loaded LLM; this is not a hard memory cap.

All 11 managed-service unit tests and the existing 47 repository tests passed; `npx awesome-lint` passed. FastAPI's test client emitted its upstream httpx deprecation warning. No checks were bypassed. The service remained healthy with no active lease after testing. Existing host Ollama, unrelated port 8765, VMs and household services were not stopped.

The raw local artifacts, private session files and development logs remain outside Git under `/Users/csells/.bb/thread-storage/voice-service-20261005`. Published recordings contain only synthetic test audio. `turn-resp0.wav` in the transcript JSON is published here as `websocket-answer.wav`.

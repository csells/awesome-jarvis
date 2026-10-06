# OpenDots mobile-browser and failure-mode testing — 2026-10-05

**Partial qualification; not fully tested on a phone. Keep on the Watch List.** The real browser-call workflow works with the disclosed OSS adapter, but reload and hangup failures prevent treating it as a dependable phone assistant. Physical-device, cellular/NAT and iOS Safari testing remain blocked on access to a remotely controllable phone or device lab. A mobile browser profile is not a physical phone.

## Artifact and environment

OpenDots `71efd82cd883df7b107d663bd36435a1d8a2d12a` plus the existing [runtime/voice adaptation](../adapted/local-runtime-voice.patch). No additional application source changes were made in this run. All 69 source files in the test VM matched the canonical adapted checkout; [hash manifest](source-hashes.json). This tests the modified build, not stock CopilotKit Intelligence or OpenAI voice.

- Bumble VM 105: Debian 13.7, 4 vCPU, 6 GiB RAM, 24 GiB disk. The older adapted report incorrectly called this Ubuntu; that label is corrected.
- Full Chromium 153 under Xvfb, Playwright Pixel 7 profile, **412 × 839 CSS pixels**, touch enabled. The entire flow started at that size; no desktop-width setup or API-created conversation was used.
- Authentication used OpenDots' actual owner-token form. The app was served over valid Tailscale HTTPS; an SSH tunnel carried that HTTPS connection from the VM to Orca. A different short-lived reservation key authenticated the app to the [permanent shared voice service](../../../voice-server/managed/README.md). No paid model/voice API was used.
- `getUserMedia` used real Chromium/PulseAudio capture from a virtual microphone. Existing synthetic speech WAVs were played into that device. No fake speech stream or canned service response was returned by the harness. The harness wrappers only observe returned native streams, peer state and data-channel events.
- The browser used normal autoplay behavior: no autoplay-policy bypass. Its actual speaker output was captured from a separate PulseAudio sink monitor and independently transcribed. This checks playback, not merely incoming media packets or generated captions.

**Network boundary:** the selected WebRTC candidate pair was `192.168.4.47 → 192.168.4.35`, UDP host candidates on the home LAN. HTTPS crossed an encrypted tunnel, but media did not cross an external NAT or cellular network. The browser supplies no ICE servers; the speech backend uses aiortc defaults when its ICE environment is unset. No TURN relay was configured. These facts do not prove remote media failure or success. The BB Connect preview was also created for authenticated remote access, but it was not used as evidence of an internet voice-call pass.

## Results

| Scenario | Result | Evidence |
| --- | --- | --- |
| Owner login and fresh mobile navigation | PASS: invalid owner token rejected; valid login, mobile menu, new conversation, call launch | [Live checks](results.json) |
| Native microphone, WebRTC and actual playback | PASS: question recognized; captured speaker output says “Seven plus five is twelve” | [Connected call](call-connected.png), [recording](speaker.webm), [independent transcript](speaker-transcript.json) |
| Voice → real compute → saved page | PASS: a new page ID was created with the requested content; title comparison ignores speech capitalization | [Pages](pages.json), [events](events.json) |
| Microphone mute | PASS: native track disabled; spoken test phrase produced no input transcription | [Live checks](results.json) |
| Speaker mute | PASS: a response was generated while actual speaker PCM stayed below the test's audible threshold | [Live checks](results.json) |
| Audible interruption | PARTIAL for responsiveness: count stops well before 30 and switches to Paris, but the recording continues to about six | [Recording](speaker.webm), [transcript](speaker-transcript.json); the harness's event-level PASS is narrower than this quality assessment |
| Minimize/expand and normal hangup | PASS: mobile controls work; normal hangup stops microphone tracks | [Minimized call](call-minimized.png), [live checks](results.json) |
| Same mounted conversation after call | PASS: text follow-up recalls the saved title and sentence | [Rendered follow-up](text-followup.png) |
| Microphone permission denied | PASS: native permission denial displayed, no track or server call created | [Fault results](fault-results.json) |
| One failed control-poll request | Call ends cleanly, **no automatic reconnect** | [Fault results](fault-results.json) |
| Hangup HTTP request stalls | **FAIL:** after 10 s, UI still says “Saving call…”, peer is connected and microphone track remains live but disabled | [Screenshot](blocked-hangup.png), [fault results](fault-results.json) |
| Browser refresh during call | **FAIL:** old call remains active with no endedAt; a new call is rejected | [Isolated result](reload-results.json), [screenshot](reload-stale-call.png) |
| App restart | Pages/call records PASS; **conversation-history durability FAIL in this adapter**: 7 messages → 0, all 4 saved pages unchanged | [Persistence summary](persistence-summary.json) |
| Spoken approve/deny/compute cancellation | NOT IMPLEMENTED by this voice adapter: exposed speech tool is ask_compute; barge-in is not compute cancellation | [Adapter source](../adapted/local-runtime-voice.patch) |
| Physical phone, iOS Safari, cellular/NAT, Wi-Fi/cellular handoff, lock screen/background, Bluetooth routing | **BLOCKED / NOT TESTED:** no attached Android device; iPhone device service unavailable; remote physical-device access requested but not provided during this run | No emulation result is substituted for these checks |

The generated call receipt again says the count completed through 30, contrary to recorded playback. The mobile minimized view also continued to show “speaking” after audio finished. Captions and receipts are not playback evidence.

## Failure attribution

The stalled-hangup behavior comes from `useVoice.end()` awaiting an end request and history refresh before stopping media, without a bounded client request timeout. The reload behavior was reproduced through real navigation, independently of the earlier abrupt-browser-close finding. Cleanup required explicitly ending the abandoned test call through the authenticated API; this was test cleanup, not a user-facing recovery pass. These are app lifecycle findings on the tested upstream pin plus adaptation.

History loss is specifically a limitation of our `InMemoryAgentRunner` adapter; do not attribute it to stock Intelligence persistence. SQLite documents and call records survived the restart exactly. A source review also found that a failed history refresh after successful compute can be reported as “Compute failed”; this was not independently fault-injected in the live run and is not counted as a tested failure here.

## Test integrity and intermediate failures

- The initial headless Chromium shell rejected native microphone capture with “Not supported.” Full Chromium in Xvfb successfully acquired the device. The headless failure is a harness/environment result, not a physical-phone result.
- An initial page assertion required title-case “Voice Follow-Up”; the actual tool correctly created lowercase “voice follow-up” with the requested content. The corrected test compares title case-insensitively and requires a **new page ID**, preventing an earlier page from satisfying the assertion.
- Browser closure after that run left a live app call, and the next call was rejected. That result was preserved, then the owned call was explicitly cleaned up.
- In the first fault batch, the reload case could not establish a new call after the preceding fault tests (fetch failure and dangling gateway reservation). That case is **TEST_ERROR**, not a pass. Capacity was released, the app restarted, and the isolated reload run reproduced the actual reload failure. Its separate result is retained.
- A failed harness API request printed a disposable test owner token in its local error log. It was redacted and the token was revoked/rotated before continuing. No personal provider credential was used or committed.
- The nine normal-flow checks completed. All [184 application tests](tests.log), [typecheck](typecheck.log), [lint](lint.log), and [production build](build.log) passed. Build output includes the existing large-chunk warning. These checks do not certify phone hardware or real external-network media.

## Reproduction and retained work

[Normal-flow harness](mobile-live.mjs), [fault harness](mobile-faults.mjs), and [isolated reload harness](reload-isolated.mjs) use the actual app UI and backend. Network faults deliberately abort/hold selected browser requests; they do not mock successful service replies. The fresh test DB, private configuration, raw speaker WAV and intermediate failures remain in VM 105 and local `/Users/csells/.bb/thread-storage/opendots-mobile-20261005`.

Prepare the prior adapted build and the existing synthetic WAVs listed in the harness. Configure the app with a private owner token, a separate shared-voice reservation key, `OPENDOTS_LOCAL_RUNTIME=1`, and its exact HTTPS `APP_ORIGIN`. The guest uses SSH forwards for Ollama and the voice gateway; do not expose their raw ports. Create PulseAudio `voice_input` and `voice_output` null sinks, remap `voice_input.monitor` as `jarvis_mic`, and set it as the default source. Run full Chromium with Xvfb and `PULSE_SOURCE=jarvis_mic PULSE_SINK=voice_output`; do not restore Playwright's default mute-audio flag. The harness uses a private owner JSON file that must never be committed.

Remaining qualification requires a controllable physical phone and an actual external network. Run the same start/conversation/action/interruption/hangup flow there, then background/lock-screen, permission, audio-route and Wi-Fi/cellular transition checks. This report deliberately does not claim “fully tested.”

## Cleanup

The test reservation was released, VM 105 was shut down with its data retained, and the temporary HTTPS/BB Connect shares were removed. The permanent shared voice service remains healthy with no active reservation. The awesome-jarvis repository checks passed: 47 tests and awesome-lint.

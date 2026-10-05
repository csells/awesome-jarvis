# Hey Jev adapted-service test — 2026-10-05

Follow-up to the [stock-code assessment](../README.md), at the same upstream commit, `24e4b378350d999d2b45ff2549ea039c2bc7863d`. Tested in the same disposable macOS 26.6.2 ARM64 VM with Python 3.14.7. The user explicitly authorized service substitutions and use of an existing Jev API key from their vault. This is an **adapted build**, not a claim that the unmodified Fish Audio/OpenRouter integrations passed.

## Exactly what changed

| Layer | Tested implementation |
|---|---|
| Command classification | **Unchanged:** real TypeSafe `jev-latest`, using the user's existing Jev API key. No simulated classifications. |
| Wake phrase, recording, ordinary speech recognition | **Unchanged:** upstream recorder and local faster-whisper `small.en`. |
| General answers | **Replaced:** OpenRouter HTTP calls with the official Claude Code CLI, authenticated by the user's existing subscription, `--model haiku --safe-mode --tools '' --no-session-persistence`. A loopback HTTP bridge reached through an SSH reverse tunnel kept subscription credentials on the host. |
| Spoken replies | **Replaced:** Fish Audio synthesis with macOS `say`, rendered into real WAV files and played by upstream `afplay`. The adapter strips Fish emotion tags and uses its own cache; it does not assess Fish voice quality, emotion or pricing. |
| Dictation transcription | **Replaced:** OpenAI/OpenRouter transcription with local faster-whisper `small.en`. Upstream spoken start/stop, buffering, vocabulary handling, clipboard, paste and history logic remained. |
| Credential gates | Required only the real TypeSafe key; removed the dictation check for the replaced OpenAI/OpenRouter services. No fake service keys were supplied. |
| Instrumentation | Added timestamped state messages while forwarding the original notifications to the native UI. No fake assistant responses, fabricated UI states or action results. |

The app retains upstream labels such as “Fish Audio” and logs such as `fish cached` / `anthropic/claude-haiku-4.5`; those labels do **not** describe the substituted backend. The tested answer selection was the CLI's `haiku` alias. The [patch](adapter.patch) uses zero context (`git apply --unidiff-zero`); the [adapter](lab_adapter.py), [application script](apply_adapter.py) and [subscription bridge](subscription_bridge.py) are included.

## Results

| Test | Result | Evidence |
|---|---|---|
| Wake, then question | PASS with adapted speech/answers | Said “Hey Jeff,” waited for Listening, then asked the capital of France within the ten-second follow-up window. Captured output says Paris. [Events](followup-result.json), [transcript](followup-transcript.txt), [audio](followup-answer.wav). |
| Timer create, query and cancel by voice | PASS | Created a five-minute timer, displayed its countdown, spoke the remaining time, then removed it after a spoken cancel. [Voice results](voice-results.json), [timer screenshot](timer.png). |
| Supported compound action | PASS | “Open Safari and set a timer for five minutes” produced two real classified actions. Safari was independently verified running, and the timer was visible and subsequently cancelled. [Action log](supported-compound.txt), [process check](safari-running.txt). |
| Unsupported app in compound action | PARTIAL | Calculator is absent from upstream `apps.json`. The assistant created the timer but skipped Calculator without an explicit warning about the omitted action. Do not count this as both actions succeeding. [Log](unsupported-compound.txt). |
| Barge-in | FAIL | During the real spoken twenty-element answer, injected “Hey Jeff, stop. What is two plus two?” The assistant continued through calcium and did not answer the interruption. Asking again after playback finished produced “four.” [Results](voice-results.json), [interruption audio](barge-in.wav), [recovery audio](recovery.wav). This matches upstream's deliberate pause in microphone processing during a turn. |
| Voice-started dictation and spoken stop | PASS with local transcription | Voice start, spoken stop, automatic paste and saving succeeded. Clipboard and saved file both contain “The blue notebook is on the wooden desk”. [Saved result](dictation-result.json), [events](dictation-results.json), [screenshot](dictation-pasted.png), [run log](dictation-final.log). |
| Visual state and work | PASS in adapted build | Inspected actual Listening, Thinking, Speaking, Ready/countdown, dictation bubble and pasted-document screenshots. The waveform indicator is specific to dictation. |
| Agent oversight / spoken approval policy | Not implemented | The adaptation adds no agent delegation, child status, approval/denial flow or general task cancellation. Timer cancellation is not agent cancellation. |

In the raw driver results, `complete: true` means the state cycle reached Ready; it does not mean the behavior passed. The interruption test completed its cycle but failed barge-in.

The four hallmark scores stay **Voice partial, Hands-free partial, Visual full, Oversight absent**. These results strengthen the evidence for a useful voice-command assistant; they do not qualify it for the Jarvis Agents scorecard.

## Test limitations and corrections

- The first wake-follow-up attempt let the ten-second window expire while the harness transcribed the previous capture. Its silence transcript is not an assistant answer or a product failure. The separate [follow-up probe](followup_probe.py) corrected the timing and passed.
- The first dictation attempt exposed a key gate missed in the test adapter. The final patch removes that gate for the real local transcription replacement. This was a test-adaptation defect, not a stock-app bug.
- First-use macOS Automation permissions blocked the next paste and the runner's save command. The lab granted them in the disposable VM. An earlier retry still failed; the final run restarted the app after the grants and used a fresh document to avoid a test-harness TextEdit save conflict. That run verified both paste and saved content. No host permissions changed. [Permission screenshot](dictation-permission.png).
- One input, “cancel all timers,” was transcribed as “cancel Alzheimer's.” Jev still selected timer cancellation. This single run is not an accuracy benchmark.
- The virtual speaker capture reported SoX buffer overruns, and some Whisper output contains silence hallucinations or missed acknowledgement words. The important answer, timer and interruption recordings were corroborated with actual state/action evidence. The report does not claim flawless audio or a latency benchmark; observed CLI answer times also varied substantially. [Capture warnings](capture-warnings.txt).
- Only synthetic test speech and an empty lab document were used. Dictation tested a short sentence, not long recordings or failure recovery. The original cloud dictation service and Fish synthesis remain untested.

## Curation decision

**Still deferred.** The paid-key blocker has been worked around for the explicitly adapted paths and the real Jev classifier has now been tested. The separate [privacy discrepancy](../README.md#observed-results) remains: upstream records speech it identifies as not addressed to it despite the UI saying it discards it. The source still has no declared license. These findings, rather than the cost or availability of credentials, are why it has not been added to the curated recommendations.

## Reproduction and cleanup

Start with the pinned checkout and the installation recovery documented in the original report. Put `lab_adapter.py` beside `siri.py`, then run `apply_adapter.py` once against clean upstream `siri.py` and `secrets_store.py`. Supply an authorized real TypeSafe key in the VM's ignored `.env` with mode 0600; do not put it in source or evidence.

Run `subscription_bridge.py` on the host through its normal subscription-authenticated Claude CLI, then establish an SSH reverse tunnel from guest `127.0.0.1:18765` to host `127.0.0.1:18765`. The bridge must remain loopback-only; never expose it through a public port share. It is test infrastructure, not an assistant capability or production service. No raw subscription token is copied into the guest.

Route BlackHole 2ch as microphone and BlackHole 16ch as output. Use the native app in wake mode. Grant the app Microphone, Accessibility and Automation access to System Events inside the disposable guest, and grant the test runner its separate screenshot/Automation permissions. The lab's [`vm.sh`](../../../macos/vm.sh) can copy files; `tart exec` runs the included drivers in the guest GUI session. The scripts use the lab's `say-mic`, `record-out` and `transcribe` helpers.

The [initial suite](voice_suite.py), [supported-command retest](voice_retest.py), [earlier permission retry](dictation_retest.py), [successful final dictation driver](dictation_final.py) and [follow-up probe](followup_probe.py) preserve the test sequence, including the corrected cases. Inspect captured screenshots and actual saved output, not just “Ready” log messages.

After testing, the app was quit, the temporary Jev credential file was removed from the guest, and the host subscription bridge and SSH tunnel were stopped. The VM is stopped and retained for retesting. No subscription tokens were extracted or copied. The guest retains the test adaptation; no changes were submitted upstream.

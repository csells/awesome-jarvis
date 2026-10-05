# Hey Jev candidate test

Tested 2026-10-04 (America/Los_Angeles) at [`24e4b378350d999d2b45ff2549ea039c2bc7863d`](https://github.com/henryklunaris/hey-jev/tree/24e4b378350d999d2b45ff2549ea039c2bc7863d), in the disposable Tart macOS 26.6.2 ARM64 VM, using Python 3.14.7. Codex performed the tests and first review; a separate Codex reviewer assessed the pinned source without seeing the first review or the list's assessment.

The [2026-10-05 adapted-build follow-up](adapted/README.md) tests the voice loop with a real Jev key, subscription-backed answers and local speech services. The results below preserve the initial stock-code assessment.

## Decision

**Defer inclusion.** Hey Jev implements a Mac voice-command assistant, with local recognition, timers, a native dashboard and cloud dictation. It does not meet the Jarvis Agents bar. Voice Assistants would be its eventual category, but the verified mismatch between its privacy statement and default audio retention needs resolution before recommending it. No license is declared at this commit. Reconsider after retention is removed or accurately disclosed and controllable, the license is clarified, and the stock cloud integrations can be tested. The adapted voice loop has since been tested in the follow-up linked above.

Missing keys were a limitation of this initial 2026-10-04 run, not a product failure. In that run, no API keys were supplied, no host credentials were read, and no cloud assistant replies were simulated. The upstream checkout remained clean.

## Hallmarks

Both code reviews agreed on the scores below. Runtime observations cover only the stated components, not a completed assistant conversation.

| Hallmark | Code score | Hands-on result |
|---|---|---|
| Voice | Partial | PARTIAL: actual Recorder input, local small.en recognition and wake matching passed. Full command routing and spoken replies BLOCKED by TypeSafe and Fish Audio keys. Paused microphone processing ignored injected speech; source pauses processing of microphone input for the entire request/reply, so no barge-in. |
| Hands-free | Partial | BLOCKED for the full voice loop. Timer creation/cancellation functions passed directly; this does not establish cancellation by voice. No general voice approval, denial or task interruption exists in the reviewed dispatcher. |
| Visual | Full from code | PARTIAL: built and inspected the real Keys and Privacy screens. Listening/thinking/speaking and work-progress rendering remain code-reviewed, not exercised in a live cloud turn. |
| Oversight | Absent | Not implemented in the reviewed source: fixed Mac actions and timers, with no agent dispatch, agent status or child approvals/cancellation. |

The scores do not earn a main scorecard row: voice is partial and oversight absent, even though the dashboard earns full visual credit from code.

## Observed results

- **Clean installation failed.** Following the README with a fresh Python 3.14 virtual environment installed `requirements.txt`, but `python setup.py py2app -A` failed with `ModuleNotFoundError: No module named 'setuptools'`. Installing `setuptools` and `py2app` in that venv fixed the build. Neither dependency is in the pinned requirements. No source patch was needed. See [build evidence](build.txt).
- **App launch passed, conversation did not run.** The real app opened its Keys screen and requested TypeSafe, Fish Audio and OpenRouter credentials. The CLI exited with `need TYPESAFE_API_KEY and FISH_AUDIO_API_KEY in Keychain or .env`. See [startup](startup.png) and [key gate](key-gate.txt).
- **Audio loop verified.** The VM transcribed the injected microphone phrase and the speaker phrase correctly. Microphone RMS during speaker playback was 0.000015, versus 0.055669 for the injected microphone phrase. SoX reported buffer overruns during speaker capture, so these measurements establish working capture/isolation, not glitch-free playback or latency. See [audio self-test](audio-selftest.txt) and [full audio-loop log](audio-selftest-log.txt).
- **Local components passed.** Upstream `Recorder` captured virtual-mic audio; upstream-configured faster-whisper transcribed “Hey Jeff, set a timer for five minutes” as “Hey Jeff, set a timer for 5 minutes,” and the upstream wake regex matched it. An unrelated sentence did not match. With `Recorder.paused = True`, injected “Hey Jeff, stop” produced no queued segment. Actual timer functions created a 300-second timer and removed it. See [component log](components.txt), [results](components.json) and [probe](component_probe.py). These tests do not pass through cloud classification or establish spoken replies.
- **Ambient audio retention reproduced.** The real upstream wake loop heard “The quick brown fox jumps over the lazy dog,” logged it as `not for me`, and saved a 112,044-byte WAV under its default `~/Library/Logs/Hey Jev clips` directory. An independent transcription of that saved WAV recovered the sentence. The actual [Privacy screen](privacy.png) says unrelated speech is thrown away. See [wake-loop log](ambient.txt), [saved-audio transcription](ambient-verification.txt) and [reproduction probe](ambient_probe.py).

### Scope of the ambient probe

The harness calls upstream `run_voice_assistant` directly because the CLI/UI gates startup on cloud credentials. It disables only `warm_cache`, which otherwise pre-renders Fish Audio replies. Capture, Whisper, wake matching, ignored-speech handling and clip writing are upstream code. There are no fake classifier or speech responses. Only synthetic lab speech was injected. The probe exits after capturing evidence; Python emitted a leaked-semaphore cleanup warning on that deliberate process exit. This isolated test proves local retention, not an end-to-end cloud conversation.

## Source evidence and dependencies

- [Microphone pause and ignored-speech saving](https://github.com/henryklunaris/hey-jev/blob/24e4b378350d999d2b45ff2549ea039c2bc7863d/siri.py#L794-L817), [default clip storage](https://github.com/henryklunaris/hey-jev/blob/24e4b378350d999d2b45ff2549ea039c2bc7863d/siri.py#L24), [ignored-phrase call site](https://github.com/henryklunaris/hey-jev/blob/24e4b378350d999d2b45ff2549ea039c2bc7863d/siri.py#L914-L916).
- [Privacy statement](https://github.com/henryklunaris/hey-jev/blob/24e4b378350d999d2b45ff2549ea039c2bc7863d/assistant_ui.py#L67-L78).
- [Direct action execution](https://github.com/henryklunaris/hey-jev/blob/24e4b378350d999d2b45ff2549ea039c2bc7863d/siri.py#L647-L677): supported Mac actions execute after classification without a separate approval exchange. No coding-agent permission bypass or borrowed provider login was found.
- [Cloud dictation](https://github.com/henryklunaris/hey-jev/blob/24e4b378350d999d2b45ff2549ea039c2bc7863d/dictation.py): audio goes to OpenAI directly or through OpenRouter. Other recognition is local, but command text goes to TypeSafe, questions to OpenRouter and spoken reply text to Fish Audio. Ordinary operational logs also retain transcripts locally.
- [Native state rendering](https://github.com/henryklunaris/hey-jev/blob/24e4b378350d999d2b45ff2549ea039c2bc7863d/assistant_ui.py#L766-L788) and [dictation overlay](https://github.com/henryklunaris/hey-jev/blob/24e4b378350d999d2b45ff2549ea039c2bc7863d/bubble.py).
- GitHub reported 11 commits by one contributor, creation on 2026-09-22, last push 2026-09-29, no declared license, and not archived. The second reviewer verified local source hashes against the pinned GitHub tree.
- [Dependency versions used](dependencies.txt). Requirements are lower bounds rather than a lockfile. No separate telemetry client or self-updater was found in the inspected Python files.

## Reproduce

Use the existing [macOS lab](../../macos/vm.sh) and [lab rules](../../RULES.md). Start the VM and prove its audio loop first. Clone the upstream repo inside the disposable guest at `~/code/henryklunaris/hey-jev`, check out the pinned commit above, and follow its install instructions. Record the initial build failure, then add `setuptools py2app` to the app's venv and rebuild. Open the app without supplying credentials.

Copy both probe scripts to the guest's home directory. They expect the checkout above, `~/lab/bin/say-mic`, BlackHole 2ch and the VM's `out` share at `/Volumes/My Shared Files/out`. Grant the guest Python app Microphone and Accessibility access using the lab's `tcc-grant` helper. Run each script in the guest GUI session through `tart exec jarvis-macos /Users/admin/code/henryklunaris/hey-jev/.venv/bin/python -u /Users/admin/<probe>.py`. Transcribe the saved synthetic ambient WAV with the lab's `transcribe` command. Inspect the screenshots rather than trusting a launch log.

Start: `lab/macos/vm.sh start` (or keep `tart run jarvis-macos --no-graphics --no-audio --dir=out:<evidence-dir>` alive in a tracked foreground session). Stop: `lab/macos/vm.sh stop`. Keep the VM and installed app for retesting; do not delete the lab image.

# Testing Methodology

How agents are scored for this list, and how to test a new one. The goal is a score anyone can reproduce from evidence, not from a project's README. Results live in [testing.md](testing.md); the scorecard is in [readme.md](readme.md#scorecard).

## Principles

- **Evidence over marketing.** A pillar counts only if it can be found in the code and, ideally, seen working. READMEs, demo videos and launch posts are leads, not proof.
- **Two independent reviews, the second blind.** The second reviewer never sees the first's scores. Where they disagree, the blind score wins unless hands-on testing settles it.
- **Run it when you can.** Hands-on results override code review in both directions.
- **BLOCKED is not FAIL.** When a feature needs a paid key or hardware the tester doesn't have, it is recorded as BLOCKED and scored from code, with the requirement disclosed.
- **Disclose risk.** Permission defaults, telemetry, credential handling and licenses go in the "Watch out" column even when the agent scores well.
- **Date everything.** Scores decay. Every result records when it was produced and at which commit or version.

## The Four Hallmarks

Score each hallmark ● (shipped and working), ◐ (partial, limited or experimental) or ○ (absent).

| Hallmark | ● | ◐ | ○ |
|---|---|---|---|
| **Voice** | Always listening or a wake word, spoken replies, and you can interrupt it by talking (barge-in) | Push-to-talk or click-to-talk, text-to-speech only, no barge-in, or voice that needs a separate app | No voice |
| **Hands-free** | The whole loop works by voice: wake, talk, interrupt, approve or deny an action, cancel a running task | Wake and talk work, but approving, denying or cancelling needs a click, key or tap | Push-to-talk only |
| **Visual** | An orb, HUD, avatar, overlay or dashboard that shows the assistant's state (listening, thinking, speaking) and the work in progress | A status indicator or a chat UI with tool cards | Plain transcript or nothing |
| **Oversight** | Dispatches other agents (sub-agents, coding agents, background workers) and shows them live, with approvals and cancel | One delegated agent at a time, or delegation without visibility or controls | Calls tools only |

**Jarvis Agents** must be ● on at least two of voice, visual and oversight, including voice or oversight. **Mission Control** entries must be ● on oversight. Everything else is a building block or doesn't belong.

## Pipeline for a New Entry

1. **Triage.** Confirm it's real and alive: the repository exists and isn't archived, it has commits in the last 90 days (a year for building blocks), and you know its license. Note stars, contributors and age, but don't score on them.
2. **Code review A.** A reviewer scores the four hallmarks from code using the brief below.
3. **Code review B, blind.** A second reviewer does the same with no access to review A or to this list's opinion of the project.
4. **Reconcile.** Where the two disagree, re-read the cited code. The blind score wins unless the evidence clearly says otherwise.
5. **Hands-on test.** Run it in the lab (below). Record PASS, PARTIAL, FAIL or BLOCKED per hallmark, with evidence.
6. **Safety audit.** Work through the checklist below.
7. **Place it.**
   - **Jarvis Agents or Mission Control:** meets the bar, has sustained activity, and more than one maintainer or a clear track record.
   - **Watch List:** a real Jarvis idea in working code that is young (under about three months), has a single maintainer, has gone quiet, or carries a serious unresolved risk.
   - **Building blocks:** the relevant section if it's a component.
   - **Reject:** the claims don't survive review, it's abandoned, or it's a chat UI with a microphone button.
8. **Publish.** Add or update the scorecard row, including its "Tested" level (Hands-on, Partial, Code or Docs) and "Watch out" notes, the entry description, and a dated row in [testing.md](testing.md).

## Code Review Brief

Give each reviewer this brief, a link to one project, and nothing else. It works for human reviewers and for AI agents.

> You are independently verifying whether a project is a real "Jarvis agent". Don't read any awesome list's opinion of it. Form your own judgment from primary evidence.
>
> Score each hallmark 0 (absent), 1 (partial, limited, experimental or claimed only) or 2 (shipped, working, evidenced in code): VOICE (wake word or always-on listening, spoken replies, barge-in), HANDS-FREE (approve, deny and cancel by voice), VISUAL (state and work shown in an orb, HUD, avatar, overlay or dashboard), OVERSIGHT (dispatches and supervises other agents with visibility, approvals and cancel).
>
> Read the code, not just the README. Shallow-clone the default branch and find the files that implement each hallmark; cite them as links. Check that features are on the default branch and wired up, not stubs, TODOs, roadmap items or a paid closed add-on. Record activity (last commit, commits in 90 days, contributors), license, supported platforms and required cloud services or API keys.
>
> Look for safety red flags: installers piped from unknown hosts, opaque prebuilt binaries, telemetry and whether it's opt-in, disabled permission checks (for example `--dangerously-skip-permissions` or `bypassPermissions`), auto-approval defaults, reuse of other tools' credentials, and auto-updating from an unpinned branch.
>
> Report per hallmark: the score, a one-line justification and evidence links. Then give a verdict (CORE, WATCH or REJECT), safety notes, and a one-sentence description stating only what you verified, including caveats about license, cloud dependencies and platforms.

## The Lab

Test on the platform the agent targets. The reference lab ran on an Apple silicon Mac mini (32 GB):

| Target | Environment |
|---|---|
| Linux agents and servers | Docker (Ubuntu or Arch Linux ARM) with a virtual audio graph and a headless X11 or Wayland display |
| Omarchy and Hyprland plugins | Omarchy M's ARM64 VM image under QEMU with Apple's hypervisor (`-accel hvf`), or real hardware; Hyprland won't run in Docker Desktop, which has no GPU device |
| macOS apps | A disposable macOS VM (Tart, from Cirrus Labs' base images) |
| Android apps | The Android emulator with an arm64 system image |
| iOS apps | Xcode's iOS Simulator |

### Model Access

- Use the tester's own subscription through the vendor's official CLI (for example the Claude Code CLI), or free local models through Ollama. Keep one login per lab and share it across environments rather than signing in to each one.
- Don't extract raw tokens into agents that call provider APIs directly while presenting themselves as another tool.
- If the agent needs a paid key the tester doesn't have, record BLOCKED. For apps that expect OpenAI's Realtime or speech APIs, try the free local voice stack described in [testing.md](testing.md#local-voice-instead-of-paid-keys). If the address is hardcoded, a clearly disclosed one-line change is acceptable, and the result is labelled "tested with a one-line URL change".

### Audio Loop

Voice is tested without a physical microphone. A text-to-speech engine speaks the test phrase into a virtual microphone, and whatever the agent says is recorded from a virtual speaker and transcribed. Prove the loop with no model first: a phrase injected into the microphone must transcribe exactly, and speaker output must not leak into the microphone.

**Linux (PulseAudio or PipeWire with pipewire-pulse):**

```sh
pactl load-module module-null-sink sink_name=speaker
pactl load-module module-null-sink sink_name=vmic_in
pactl load-module module-remap-source master=vmic_in.monitor source_name=vmic
pactl set-default-sink speaker && pactl set-default-source vmic

piper --model en_US-lessac-medium --output_file q.wav <<< "hey jarvis, what time is it?"
paplay -d vmic_in q.wav                                          # speak into the "microphone"
parec -d speaker.monitor --file-format=wav --rate=16000 out.wav  # record what the agent says
```

**macOS:** install BlackHole 2ch and 16ch and SwitchAudioSource, then make BlackHole 2ch the default input and BlackHole 16ch the default output. Speak with `sox q.wav -t coreaudio "BlackHole 2ch"` and record with `sox -t coreaudio "BlackHole 16ch" out.wav trim 0 30`.

**Transcribe** with faster-whisper or whisper.cpp (`base.en` is enough). The transcript of what the agent said is the voice evidence.

### Screenshots

Capture the agent's visual state at each phase and look at every image; an unviewed screenshot isn't evidence. On Wayland use `grim`; on X11 `ffmpeg -f x11grab`; on macOS `screencapture` from the GUI session; on Android `adb exec-out screencap -p`.

### macOS Privacy Prompts in a Disposable VM

Voice apps need Microphone, Speech Recognition, Accessibility and Screen Recording. In a throwaway VM with SIP disabled and SSH granted Full Disk Access (as in Cirrus Labs' images), write the grants into both TCC databases with each app's code-signing requirement, the same technique Cirrus Labs uses to build its images. Launch apps with `open` so the grants attach to their bundle. Never do this on a machine you care about.

## Hands-On Test Script

Run each step, save the evidence, and mark the result.

**Voice**
1. Say the wake word, then a simple factual question ("What is the capital of France?"). PASS if the transcript of its reply answers it.
2. Ask for a long answer and talk over it ("Stop. What is two plus two?"). PASS if it stops and answers the new question.
3. Note the time from the end of your speech to its first audio.

**Hands-free**
1. Ask for something that needs approval, such as a shell command or a file write. Answer "yes" by voice. PASS if it proceeds without a click.
2. Ask for the same again and answer "no" by voice. PASS if it doesn't run.
3. Start a long task and say "cancel that". PASS if the task actually stops (check its process or task list), not just the conversation.

**Visual**
1. Screenshot idle, listening, thinking and speaking. PASS if the states are visibly different.
2. Screenshot while a delegated task runs. PASS if the task and its progress are visible.

**Oversight**
1. Ask it by voice to start another agent (a sub-agent or a coding agent) on a small, checkable task, such as writing a file with known content. PASS if the task runs and the result can be verified on disk.
2. List the running agents, by voice if possible. Cancel one. PASS if it stops.
3. Confirm that approvals from the child agent reach you and that nothing ran without one unless you configured that.

## Safety Checklist

- **Permission defaults:** does it launch coding agents with permission checks skipped or in an auto-approve mode? Does its own approval policy default to "ask"? Can its voice agent approve its own sub-agents' actions? (Watch Claude Code's own defaults too: version 2.1.283 defaults to an "auto" mode.)
- **Telemetry:** is anything sent home by default, and can you turn it off, including from the installer?
- **Credentials:** does it read other tools' saved logins (for example Claude Code's Keychain entry) or present itself as another client?
- **Supply chain:** installers piped into a shell, unpinned `npx`/`@latest` backends, auto-updates from a branch, and prebuilt binaries in the repository.
- **Exposure:** dashboards or remote-control endpoints listening on all interfaces, plaintext key storage, keys in git history.
- **License:** non-commercial, source-available or missing licenses.

## Recording Results

- **Scorecard row:** agent, platform, the four hallmark scores, Tested (Hands-on, Partial, Code or Docs) and a short Watch out.
- **testing.md row:** PASS, PARTIAL, FAIL or BLOCKED per hallmark, with one or two sentences of specifics, the environment, the date and the version or commit tested.
- **Evidence:** keep transcripts, screenshots and logs named by agent and step (for example `paseo/step2-agent-speech.txt`). Link them from a pull request when contributing.

## Re-Verification

- Re-test scorecard agents every quarter and after any major release.
- Review the Watch List monthly: graduate entries that have shown sustained activity and a second maintainer, and drop entries that have gone quiet for six months.
- A scheduled staleness check flags dead links, archived or renamed repositories, and scores older than 90 days for re-testing.

## Lab Pitfalls

Lessons from the reference lab that will save a new tester hours:

- **VMs started from an agent's shell can run about 20 times slower** on macOS, because they inherit background CPU priority. Start them as a temporary launchd job instead.
- **Omarchy's idle lock** blanks the display after five minutes and breaks screenshots. Turn on stay-awake while testing.
- **Hyprland needs a GPU device.** Docker Desktop has none; use a VM (software rendering works) or real hardware.
- **macOS voice-processing capture (VPIO) returns silence from BlackHole,** so apps that use it can't be voice-tested with a virtual microphone.
- **The Android emulator's microphone** needs the host's microphone permission and a virtual audio device, and its built-in audio injection can crash it.
- **Small local models** often narrate tool calls instead of making them. Use a 7B or larger instruction-tuned model before blaming the agent.
- **Shared logins expire.** Access tokens last about eight hours; refresh the shared login before a long run.

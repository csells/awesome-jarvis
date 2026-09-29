# Evidence

A small, curated subset of what the September 2026 lab run produced, organized by agent. It backs the rows in [testing.md](../../testing.md). Transcripts are what [faster-whisper](https://github.com/SYSTRAN/faster-whisper) or whisper.cpp heard in the recorded audio, so they keep the transcriber's mishearings (for example "Pacio" for Paseo). Raw recordings, full logs and most screenshots were left out; account names, email addresses, host paths and device identifiers were removed from what remains.

| Agent | What the files show |
|---|---|
| [Lab self-tests](lab-selftest/) | The audio loop works with no model in Docker, the macOS VM and the Omarchy VM (mic loop, speaker capture, isolation). `hyprland-in-docker-probe.txt` is the exact reason Hyprland can't start in Docker Desktop. |
| [hey-jarvis](hey-jarvis/) | Wake word, speech-to-text, a Claude answer and the spoken reply on real Omarchy and Hyprland (`e2e-answer.txt`); the consent window approved with a click (`e2e-consent-approved-by-click.txt`, `consent-window.jpg`) and an unfocused request silently denied after 45 seconds (`e2e-consent-unfocused-autodenied.txt`); the idle lock and plugin reload test. |
| [Paseo](paseo/) | By voice: a Claude Code agent created (`step1`), listed (`step2`), killed (`step3`); the voice agent approving its own child's file-write permission (`voice-host-timeline.txt`, "Respond to permission"); `paseo ls` before and after; barge-in timeline. |
| [Hermes Agent](hermes/) | Command-line voice turn answered aloud; delegation to Claude Code by voice (`cli-voice-delegate-to-claude-code.txt`, `workspace-demo-ls.txt`); a kanban task interrupted by the operator; barge-in failing in the command-line mode; the desktop app's spawn tree; the "smart" approval mode letting the local model approve an `rm -rf` of a test folder with no human prompt (`desktop-smart-approval-rm-rf.log`); proof that the lab's Claude login was isolated from Hermes. |
| [OpenClaw](openclaw/) | Mac app: a sub-agent spawned by voice and a run cancelled from the CLI, an approval card resolved; browser Talk against the local voice server: spoken answers, the model asking for "spoken confirmation" that could only be given by click, voice cancel and barge-in. |
| [usejarvis](usejarvis/) | Wake word, then `delegate_task` to a "content-writer" sub-agent by voice with the result spoken (about 100 seconds on a 4B local model); the agents dashboard, with the pebble overlay at the top left of the screenshot. |
| [JARVIS for Claude Code](jarvis-for-claude-code/) | Speech understood and answered in text (spoken replies need a Fish Audio key); a live Claude Code session reported by voice; a run cancelled by voice; the Run Control dashboard. |
| [TapQ](tapq/) | Runtime banner (wake word, voice trust); a Claude Code tool call approved by voice (`DONE.`) and one denied by voice (`BLOCKED`). |
| [Happy](happy/) | Pairing, two sessions monitored from the phone, an edit approved from the phone, a run aborted from the phone, and the free voice allowance. |
| [Operit](operit/) | Local-model brain, default-assistant role and avatar overlay working; voice and the sub-agent tool call not reached, with the reasons. |
| [omavoice](omavoice/) | Tested with a one-line URL change: spoken turns, barge-in, the live trace panel, and the expired Claude login that blocked delegation. |
| [omarchy-voice](omarchy-voice/) | Tested with a one-line URL change: a desktop question answered aloud, barge-in, and the 7B model reading tool calls aloud instead of making them. |
| [Local voice server](voice-server/) | Latency, barge-in and `response.cancel` results for the local OpenAI-compatible Realtime server, and the REST speech-to-text and text-to-speech round trip. |

`macos-vm-transcripts.txt` summarizes what each Mac app said, from the recordings of the VM's virtual speaker.

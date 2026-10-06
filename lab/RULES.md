# Lab Rules

Rules for anyone (person or AI agent) running a test track in this lab. They exist so results are trustworthy, the tester's accounts stay safe, and one track doesn't break another. The scoring rubric itself is in [methodology.md](../methodology.md).

## What counts as evidence

A test verifies the four hallmarks: **voice** (wake word or always-on listening, spoken replies, barge-in), **hands-free** (approve, deny and cancel by voice), **visual** (an orb, HUD, avatar, overlay or dashboard that shows state and work) and **oversight** (dispatching and supervising other agents, with visibility, approvals and cancel).

- Record what the agent *said*: capture its audio output and transcribe it. A log line claiming it spoke is not enough.
- Look at every screenshot you cite. An unviewed screenshot isn't evidence.
- Keep the logs and transcripts that show each step, named by agent and step.
- A test that only proves "it launched" is not a pass.

## Model access

- Use your own subscription through the vendor's **official CLI** (for example `claude`, the Claude Code CLI), or free local models (Ollama and similar). Don't use or request any other paid API keys (OpenAI, ElevenLabs, Fish Audio, Gemini, DashScope, Deepgram and so on).
- If a hallmark needs a key you don't have, test everything else and record **BLOCKED: needs X key**. BLOCKED is not FAIL.
- An OpenAI-compatible local voice server (see [voice-server](README.md#local-openai-compatible-voice-stack)) may stand in for OpenAI's Realtime and audio APIs. For the [managed shared service](voice-server/managed/README.md), reserve a short-lived service key; never pass its administrative key to a test application. For a separately owned transient server, use a clearly fake key such as `sk-local-dummy`. If the address is hardcoded, a disclosed one-line patch is acceptable; label the result "tested with a one-line URL change".

## Credentials

- Never read, copy or print the host's own logins: `~/.claude`, `~/.codex`, the macOS Keychain or a password manager. Never extract tokens from them.
- The lab keeps **one** Claude login of its own, in the Docker volume `jarvis-lab-claude`. Create it with `login-claude.sh`; share it into VMs only with the helpers (`macos/share-claude-login.sh`, `omarchy-vm/share-claude-login-vm.sh`), which never print it.
- Signing in to a new environment needs a human with a browser. An agent running a track should prepare everything up to the sign-in, start the login with the helper (which prints only the URL), then stop and hand back the URL and the exact command to feed the one-time code from a file.
- Only one container should use `jarvis-lab-claude` at a time. Access tokens expire after about eight hours; refresh before a long run.
- Don't give an agent under test raw tokens so it can call a provider API directly while presenting itself as another tool. If an agent does that by default (for example by adopting Claude Code's saved login), turn it off and record it as a finding.
- Run agents in their safest documented mode unless a test specifically needs otherwise, and record any permission-bypass defaults you see.

## Safety and hygiene

- Install only from official sources. Pin versions and check checksums where they are published. No `curl | bash` from unknown hosts.
- Never `rm -rf` outside directories you created. Don't touch other tracks' VMs, containers or volumes.
- Memory budget on a 32 GB host: Docker VM 8 GB, macOS VM up to 8 GB, Omarchy VM up to 6 GB, Android emulator up to 4 GB. Stop what you aren't using; running several at once caused swapping and watchdog kills in the reference lab.
- Do disruptive things (writing TCC databases, disabling SIP, auto-approving dialogs) only inside disposable VMs.
- The managed voice service is persistent infrastructure: release your reservation; never stop its launchd job, backend processes, or Tailscale endpoint as test cleanup.
- When a track is done: **stop** (don't delete) every VM, emulator and container you started, keep images and volumes for re-testing, and write down the start and stop commands.

## Reporting

Per agent tested: a table of hallmark results (PASS, PARTIAL, FAIL or BLOCKED with the reason), the evidence paths, notable bugs and safety findings, the version or commit tested, and the date. Anything that needs a human (a sign-in URL, an admin prompt) goes at the top.

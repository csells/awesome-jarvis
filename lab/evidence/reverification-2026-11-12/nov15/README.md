# November 15 continuation — scoped native and privacy tests

These tests ran in disposable lab guests on November 15 Pacific time (November 16 UTC). They do not complete the [remaining campaign](../../../../specs/plans/0001-november-reverification.md), accept a submission, or refresh a full-release score. Source, private logs and recordings were preserved outside the guests; account sessions, phone details and credentials are excluded here.

## Sutando 0.13.0 native macOS core

Used [release commit 623c927](https://github.com/sonichi/sutando/tree/623c927afb6e3b9bd0b8faf19fb89f0f41fe392d), with its unmodified menu-bar app and native launcher in the owned macOS 26.6.2 guest, Swift 6.3.3, Node 24.20, tmux 3.8, fswatch 1.22.0 and official Codex 0.167.2. Chris explicitly approved the launcher's unrestricted core for bounded workspace file/process tests. A supported clone-local configuration selects Codex, the task workspace and an isolated Codex home; vault integration and self-development are disabled. No permission arguments were rewritten. The active native core reported YOLO permissions; these tests do not establish human approval enforcement.

| Actual path | Observation |
|---|---|
| Local Agent API → task file → native watcher → Codex → result | PASS: independent observer verified the exact requested proof file and native completion result after 21.07 seconds |
| Native menu Stop Core CLI, app launched with `open` | Did not stop the core. The app inherited `/usr/bin:/bin:/usr/sbin:/sbin`; Homebrew tmux was absent from that path. The unchanged stop script interpreted tmux command failure as no session and returned success. This is scoped to this launch environment |
| Native menu Stop Core CLI, app relaunched with actual Homebrew tools on PATH | FAIL for worker interruption: core/watcher/observer sessions disappeared, but the independently identified worker survived at 0, 1, 3 and 5 seconds and heartbeat bytes grew 1117→1285. No natural-completion marker existed. Only after recording this did the harness terminate the exact owned worker |
| Native menu Restart Core CLI, followed by a new API file task | PASS for restart/new work: sessions returned and exact new file/result completed after 33.07 seconds. The interrupted task was also replayed; its fixture refused a second launch. This is not an exactly-once or clean-cancellation pass |

See [sanitized native observations](sutando-native.json). The heartbeat fixture was bounded to 90 seconds and refused duplicate execution; observations use the actual guest PID/command and file growth, not a stopped UI badge. An earlier observer window expired before a stop action; that run is excluded from cancellation conclusions.

Afterward the native core and app were stopped, the surviving test worker was absent, and the copied guest `auth.json` was removed without logging out the source account. The DotDial guest remains separately retained for its authenticated profile-lookup investigation. Native Sutando voice still requires a compatible supported provider; no voice, screen-capture or spoken-approval qualification is claimed.

The unchanged production lock audit reported 16 affected packages:1 critical, 12 high, 2 moderate, 1 low. The critical dependency was protobufjs 7.5.4 through `@google/genai` 1.52.0 and through `bodhi-realtime-agent` 0.4.9 → `@google/genai` 2.30.0. The [upstream advisory](https://github.com/advisories/GHSA-xq3m-2v4x-88gg) requires attacker-controlled schema/descriptor data reaching runtime code generation; trusted application-defined schemas are outside its stated impact. Application exploitability was not demonstrated. The candidate lock was not upgraded. See [audit counts and chains](sutando-audit.json).

## OpenJarvis installer and running backend

Candidate source is `13706f2b5b5ba6cac9ad31bc575d9e115213784f`. The real Bash installer used its supported repository override pointing to a complete local Git clone of that pin, not a fabricated installer or checkout. It installed the actual package as `1.0.5.dev182+g13706f2b`, with Python 3.13.5 and UV 0.13.8. Supported `--minimal --no-bg-orchestrator` avoids background model/Rust installation. The actual official Ollama CLI connects through the task SSH forward to Chris's authorized Mac Ollama; no guest inference daemon or model substitute was used. The installer attempted an additional Ollama listener, failed because that forwarded port was already occupied, then used the working existing endpoint. Its background-work banner is misleading with this flag; background installation is not a pass.

Privacy instrumentation used a guest-only nftables reject rule for the configured analytics destination, `34.231.106.201:443`. Drivers verified DNS and a rejected TCP connection before running. There was no substitute analytics server. Automatic review declined consent-positive external metadata delivery; the kernel block kept those tests within the accepted non-egress alternative. Counts below mean blocked connection attempts, not received vendor events. Payload contents, successful delivery and all other possible destinations are outside this claim.

The [initial seven installer cases](openjarvis-installer.json) passed: one fresh `--no-analytics` installation, then reruns with `--analytics`, `--no-analytics`, unattended no flags, and actual PTY N, Enter and EOF. Off choices saved false and produced 0 attempts; explicit consent and Enter saved true and produced 2 blocked attempts each. All captures had 0 egress TCP packets to that destination.

The [six independent fresh installations](openjarvis-fresh-installer.json) also passed: explicit decline, explicit consent, unattended no flags, and PTY N, Enter and EOF. Each began with an absent install directory and ran the actual minimal installer. Off cases produced 0 blocked attempts; explicit consent and Enter produced 14 each, with 0 egress packets. Unattended and EOF saved disabled without recording a consent choice; explicit choices recorded one. These counts are connection attempts, not logical event totals. Two harness errors were excluded: an obsolete partial-clone path failed before installation, and a duplicate case name stopped the driver before that case ran. The full source passed Git fsck, the remaining cases used distinct absent directories, and the successful results are retained separately from setup-failure logs.

The [five actual server cases](openjarvis-server-privacy.json) passed through the normal HTTP preference and chat endpoints, each returning a real local-model answer:

| Case | Saved analytics | Blocked attempts |
|---|---|---|
| Cold start disabled | false | 0 |
| Cold start enabled, instrumentation control | true | 12 |
| Disable live before chat | false | 0 |
| Restart with saved disabled preference | false | 0 |
| Enable live, instrumentation control | true | 12 |

Four separate plain CLI turns answered correctly, but even the enabled control generated 0 analytics attempts. That control was inadequate for a CLI privacy conclusion; it is not a privacy pass or an application failure. The server tests above exercise the actual event-producing route. Final configuration was restored to disabled.

## Official OpenJarvis desktop 1.0.5

Verified official Debian artifact SHA256 `abea3b3744953ee1801185345e6e2be1107a86e90a1fc3265558a5f5f31e71f1`. Ran its unchanged native executable with real Xvfb/Openbox, DBus and Secret Service in the Linux guest. The keyring used a task-only password, with an actual store/lookup/delete control. This is the packaged client normally attaching to the running candidate API; it does not certify the desktop's own backend installer or Windows packaging.

Completed the native compatible-server chooser and selected Continue without sharing without entering personal details. The real desktop answered Four through cached Qwen2.5. Terminated and relaunched the native process with the same profile: no repeated consent prompt, prior chat retained, sharing badge OFF and saved analytics false. A new question returned Seven. The model selector returned to Qwen3 after restart; Qwen2.5 was explicitly reselected for that turn. No model-selection-persistence pass is claimed.

The destination counter stayed 0 before and after restart and the new chat. Minimal installation lacks the native Rust memory extension, and Settings correctly reported memory unavailable; neither memory nor desktop voice was qualified. [Sanitized desktop results](openjarvis-desktop.json) record these limits. The native process, API and Openbox were stopped and reaped; the task keyring password file was removed. No stable service changed.

## Fresh staleness follow-up

The November 16 UTC dry run found AIRI 0.15.4; existing runtime evidence remains pinned to 0.15.2 and must not be relabeled as the newer release. OpenYabby's current default branch still ends at [May 15 commit 5c2dcaf](https://github.com/OpenYabby/OpenYabby/commit/5c2dcafbb226494633828fe2c423b93000927eed), 185 days earlier. The repository is not archived. It moved to history under the existing six-month Watch List inactivity rule, with an inactivity qualification rather than an archival claim.

After that correction, the queue contains10 items:6 release re-tests,2 Watch List reviews and2 outstanding PR evaluations. The full run found no dead-link or repository-health findings;155 URLs were checked, including17 explicitly skipped by the existing allowlist. All52 offline tests, Awesome lint and whitespace checks passed. The report was not published, no submission was merged, and full-test scorecard dates remain unchanged. Test evidence is exported outside both VMs; the temporary model forward was removed after these tests. Remaining tests and retention expiries stay recorded in the plan and registry.

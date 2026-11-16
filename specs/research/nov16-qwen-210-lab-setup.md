# Native Linux setup proposal — Qwen Audio Agent v2.1.0

Source/setup evidence only. Later native outcomes and superseding qualifications are recorded in the [release follow-up](../../lab/evidence/reverification-2026-11-12/nov16/README.md#release-follow-up).

Prepared by source inspection only, 2026-11-16. **Nothing below was installed, built or run.** Qwen pin: `a9f4478da8df400d04facbb099ac2933ce8b11bc`, resolved from the [GitHub tag API](https://api.github.com/repos/QwenAudio/qwen-audio-agent/git/ref/tags/v2.1.0). This is a recipe for the parent to run in its authorized disposable staging VM. Keep source, workspace, config and state separate from stable installations. Do not copy existing login secrets without authorization.

## Setup gates

- Node engine is exactly `^22.22.2 || ^24.15.0 || >=26.0.0`; npm `>=10`, declared package manager `npm@10.9.4` ([package.json](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/package.json)). **Worker Node 24.8 is unsupported.** Select an approved compatible Node before npm install/build; do not treat an engine warning as passing this gate.
- An official Codex CLI must be installed/pinned on the VM and authenticated through its normal `codex login` workflow. Record `codex --version` and `codex login status`. Qwen declares that login workflow and launches the adapter around the official CLI ([catalog.mjs:233–264](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/shared/backend/catalog.mjs#L233-L264)). No raw-token API backend is proposed. Initial login is a human/account gate if no authorized authenticated installation exists.
- Keep speech frontend local, memory auto-processing off, and all input/output voice disabled during ACP tests. A separately available, real OpenAI Realtime-compatible speech server is a later voice-test gate. **Permanent Pocket OpenAI HTTP STT and TTS alone do not satisfy it.** Do not manufacture a bridge or fake speech service to make the gate appear passed.
- Approval requests must actually appear. Native mode only preserves the backend's policy. For the proposed adapter pin below, the default mode is automatic review, so an explicit human-review mode is necessary.

## Source, dependencies and adapter pin

Commands below run on the VM after the Node gate. Use an unprivileged account with a dedicated writable lab directory. Example uses `$HOME/qwen-210-lab`; HOME retains its original value.

```bash
# Start a clean shell: no inherited cloud API keys or Qwen settings.
env -i HOME="$HOME" PATH="$PATH" LANG=C.UTF-8 bash --noprofile --norc
export QWEN_LAB_ROOT="$HOME/qwen-210-lab"
mkdir -p "$QWEN_LAB_ROOT"
cd "$QWEN_LAB_ROOT"
git clone https://github.com/QwenAudio/qwen-audio-agent.git source
git -C source checkout --detach a9f4478da8df400d04facbb099ac2933ce8b11bc
git -C source rev-parse HEAD
cd source
npm ci
npm run build
```

`npm ci` runs the repository's `prepare` hook, which itself builds the web assets; the explicit build is a convenient separately recorded check ([prepare-build.mjs](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/scripts/prepare-build.mjs)). Save install/build output and the final source SHA; don't claim success before checking exits. No global Qwen install is needed.

Qwen's adapter launcher defaults to `@agentclientprotocol/codex-acp@latest` if it cannot find a binary. Avoid that implicit update. The primary npm registry inspected during this review resolves the adapter to **2.6.0** ([immutable version metadata](https://registry.npmjs.org/@agentclientprotocol%2Fcodex-acp/2.6.0)); this is a proposed compatibility pin, **not a version tested with Qwen here**. Install it into a dedicated local prefix and retain its lockfile:

```bash
mkdir -p "$QWEN_LAB_ROOT/adapter" "$QWEN_LAB_ROOT/bin"
cd "$QWEN_LAB_ROOT/adapter"
printf '%s\n' '{"private":true}' > package.json
npm install --save-exact @agentclientprotocol/codex-acp@2.6.0
npm ls @agentclientprotocol/codex-acp
```

The launcher supports `CODEX_ACP_RUNTIME=binary` with `CODEX_ACP_BIN`, or `CODEX_ACP_RUNTIME=package` with `CODEX_ACP_PACKAGE=@agentclientprotocol/codex-acp@2.6.0` ([codex-acp.mjs:5–48](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/scripts/runtime/codex-acp.mjs#L5-L48)). Binary mode below is deterministic and avoids npx fetching later.

**Approval mode detail:** reading the downloaded 2.6.0 npm package's `dist/index.js` found `AgentMode.DEFAULT_AGENT_MODE = AgentMode.Agent`, which uses `approvalsReviewer: auto_review`. Its `getInitialAgentMode` accepts `INITIAL_AGENT_MODE=read-only` or `workspace-write`. Qwen forwards only allowlisted backend environment and `CODEX_*`; simply exporting `INITIAL_AGENT_MODE` in Qwen's parent shell will not survive that projection ([environment.mjs:75–102](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/shared/backend/environment.mjs#L75-L102), [catalog.mjs:261–264](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/shared/backend/catalog.mjs#L261-L264)). Use a tiny operational launcher to set it immediately around the **real adapter**, without altering candidate source:

```bash
cat > "$QWEN_LAB_ROOT/bin/codex-acp-human" <<'SH'
#!/bin/sh
export INITIAL_AGENT_MODE=read-only
exec "$(dirname "$0")/../adapter/node_modules/.bin/codex-acp" "$@"
SH
chmod 700 "$QWEN_LAB_ROOT/bin/codex-acp-human"
```

Read-only mode should require human approval for modifications; the actual pending event remains the acceptance gate. A failed or silently ignored mode selection must not be treated as an approval pass. Switch to `workspace-write` later for normal workspace execution only after approval tests; record the change and restart the candidate so new sessions receive it.

## Isolated runtime configuration and loopback launch

In the same clean shell, with the official Codex CLI on PATH:

```bash
mkdir -p "$QWEN_LAB_ROOT/config" "$QWEN_LAB_ROOT/data" \
  "$QWEN_LAB_ROOT/state" "$QWEN_LAB_ROOT/cache" "$QWEN_LAB_ROOT/workspace"
export QWAUDIO_CONFIG_DIR="$QWEN_LAB_ROOT/config"
export QWAUDIO_DATA_DIR="$QWEN_LAB_ROOT/data"
export QWAUDIO_STATE_DIR="$QWEN_LAB_ROOT/state"
export QWAUDIO_CACHE_DIR="$QWEN_LAB_ROOT/cache"
export CODEX_PATH="$(command -v codex)"
export CODEX_WORKSPACE="$QWEN_LAB_ROOT/workspace"
export CODEX_ACP_RUNTIME=binary
export CODEX_ACP_BIN="$QWEN_LAB_ROOT/bin/codex-acp-human"
cat > "$QWAUDIO_CONFIG_DIR/config.env" <<'ENV'
HOST=127.0.0.1
PORT=3101
AGENT_PROTOCOL=codex
QWEN_AUDIO_AGENT_BACKEND_PERMISSION_MODE=native
QWEN_AUDIO_REALTIME_PROVIDER=speech-to-speech
QWEN_AUDIO_REALTIME_URL=ws://127.0.0.1:8765/v1/realtime
QWEN_AUDIO_REALTIME_API_KEY=
QWEN_AUDIO_MEMORY_AUTO=off
QWEN_AUDIO_AGENT_IDENTITY_MODE=personal
ENV
chmod 600 "$QWAUDIO_CONFIG_DIR/config.env"
cd "$QWEN_LAB_ROOT/source"
node cli/bin/qwenaudio.mjs setup --backend codex --json
node cli/bin/qwenaudio.mjs gateway run --backend codex --backend-permission-mode native
```

The local speech URL is the stock user-managed endpoint setting, **not a claim that a service exists there**. No voice traffic is needed for the ACP-only task protocol below; unavailable local speech may generate local connection errors if WebUI tries to activate it. Never substitute a fake responder. Do not use `--lan`, `--tailnet`, `--webrtc` or service installation for this first pass. Verify `ss -ltnp` shows Qwen bound to `127.0.0.1:3101`. Config loader automatically creates its own auth secret; don't print `config.env` after startup. Runtime directories and bootstrap loader are implemented in [runtime-environment.mjs:250–314](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/shared/runtime-environment.mjs#L250-L314). Native Codex driver launches the official adapter and CLI, without model URL/API adoption unless separately configured ([codex.mjs:29–56](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/server/src/backend/adapters/acp/drivers/codex.mjs#L29-L56)).

## Real file task, pending approve/deny, then executing cancellation

Use the Gateway's **GCP WebSocket** to create a direct task, without sending typed chat through the speech frontend. The following minimal harness uses the candidate's installed `ws` dependency. Save it as `source/lab-submit.mjs` on the VM (an untracked test harness, not a fake backend):

```js
import WebSocket from 'ws'
import { randomUUID } from 'node:crypto'
const text = process.argv[2]
if (!text) throw new Error('Pass a task objective')
const ws = new WebSocket('ws://127.0.0.1:3101/api/realtime?sessionId=lab210')
const send = message => ws.send(JSON.stringify({ event_id: randomUUID(), ...message }))
const timer = setTimeout(() => { ws.terminate(); process.exitCode = 1 }, 30000)
ws.on('error', error => { console.error(error.message); process.exitCode = 1 })
ws.on('open', () => send({
  type: 'session.hello', protocol: { min: '7.0.0', max: '7.0.0' },
  client: { type: 'cli', instance_id: randomUUID(), label: 'Linux ACP verification' },
  capabilities: ['tasks.commands', 'permissions.respond'],
  connection: { voice_enabled: false, input_enabled: false, output_enabled: false, text_only: true }
}))
ws.on('message', data => {
  const event = JSON.parse(String(data))
  if (event.type === 'session.ready') send({
    type: 'task.create', message: { parts: [{ type: 'text', text }] }
  })
  if (event.type === 'task.create.result' || event.type === 'error') {
    console.log(JSON.stringify(event))
    if (event.type === 'error') process.exitCode = 1
    ws.close()
  }
})
ws.on('close', () => clearTimeout(timer))
```

Schema/wiring: [hello fields:140–167](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/shared/protocol/gateway-client-protocol.mjs#L140-L167), [task.create:287–292](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/shared/protocol/gateway-client-protocol.mjs#L287-L292), [direct task submission:129–148](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/server/src/client/client-command-runtime.mjs#L129-L148). Loopback personal identity permits local requests; don't expose that identity mode directly to a remote interface.

1. **Deny case:** `node lab-submit.mjs 'Use your real file tools to create denied.txt containing exactly DENIED_TEST in the current project. Request the required native permission; do not bypass the sandbox, delegate to an unsandboxed mechanism, or continue after denial.'` Copy returned task ID. Fetch `curl -fsS http://127.0.0.1:3101/api/tasks/TASK_ID`; require a real pending `authorization.id`, then respond:

   ```bash
   curl -fsS -X POST -H 'Content-Type: application/json' \
     -d '{"decision":"reject"}' http://127.0.0.1:3101/api/permissions/PERMISSION_ID
   ```

   Observe denied authorization and confirm `$QWEN_LAB_ROOT/workspace/denied.txt` was not created. No pending request means **approval test not passed**, even if the task succeeds or fails otherwise.
2. **Approve case:** create a new task for `approved.txt` containing exactly `APPROVED_TEST` using the same instruction pattern. Wait for its own fresh pending ID; POST `{"decision":"task"}` to that ID. Confirm native operation resumes, task completes, and actual file content is correct. `task` authorizes all subsequent permissions for that task, not just one operation; never use `always` in these checks.
3. **Executing cancel:** create a separate task with this objective: “In the current project, run the real shell command `while :; do date -u +%FT%TZ >> heartbeat.txt; sleep 1; done` in the foreground. Keep it running until the user cancels. Do not background it or replace it with a simulated timer.” In read-only mode, approve the real pending command permission with `task` if requested. Independently verify the file grows across several seconds and identify the actual shell/sleep process under the Codex tree. Only then cancel:

   ```bash
   curl -fsS -X DELETE http://127.0.0.1:3101/api/tasks/TASK_ID
   ```

   Require terminal cancelled state, no further file growth over a suitable observation interval, and no remaining heartbeat command/process. A stopped audio stream, cancelling state, or success receipt alone is insufficient. Preserve task activity/events and process evidence; cancellation timeout or uncertain backend state is a failed/inconclusive check, not a pass.

REST paths and semantics are from [gateway-http-routes.mjs:442–498](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/server/src/app/gateway-http-routes.mjs#L442-L498). List tasks via `GET /api/tasks?sessionId=lab210`; inspect events via `GET /api/tasks/TASK_ID/events`. Task cancel awaits backend cancellation; ACP sends session.cancel and waits for settlement ([process-client.mjs:654–695](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/server/src/backend/adapters/acp/process-client.mjs#L654-L695)).

## WebUI and voice boundaries

Open the existing gateway with `node cli/bin/qwenaudio.mjs webui --url http://127.0.0.1:3101 --session lab210 --no-open`. It prints a URL; on-VM use is `http://127.0.0.1:3101/?session=lab210`. Keep one active GCP client at a time: the submit harness closes after receipt, allowing WebUI to connect and render the task/pending permission card. For a remotely viewed VM, use the parent thread's authorized authenticated relay/tunnel; loopback is not directly reachable from Chris's remote browser. WebUI has `PermissionActions` connected to real pending task requests ([App.jsx:1365–1385](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/web/src/App.jsx#L1365-L1385)). It is suitable for observing and clicking approve/deny during the direct API task experiment.

**Normal typed chat in WebUI still calls `ensureFrontend().sendUserInput`** ([realtime-input-runtime.mjs:318–335](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/server/src/voice/realtime-input-runtime.mjs#L318-L335)). Consequently, requesting tasks through its ordinary composer requires a functioning realtime frontend, even with microphone muted. Until a real local speech service is present, create tasks with the direct protocol harness, not the composer. WebUI may show a missing speech connection while still displaying gateway/backend task events; report that limitation explicitly.

The stock local adapter needs a **user-managed OpenAI Realtime GA WebSocket** service with conversation/session events, audio output, function tool calls/results and server VAD/barge-in; it does not compose separate OpenAI HTTP STT/TTS services ([s2s.mjs:28–99](https://github.com/QwenAudio/qwen-audio-agent/blob/a9f4478da8df400d04facbb099ac2933ce8b11bc/server/src/voice/providers/s2s.mjs#L28-L99)). Pocket's permanent OpenAI STT/TTS alone therefore leaves voice setup blocked. Existing real realtime service availability must be established before attempting voice tests; do not create replacement services under this task.

**Evidence separation:** passing file, approval, status or heartbeat cancellation checks establishes text/GCP/ACP integration only. It does not establish microphone capture, English recognition, audible replies, wake activation, barge-in, spoken approve/deny, or spoken executing-task cancellation. Those require a later real microphone/speaker session through the actual speech provider and independent process-effect checks. Report each as untested until observed.

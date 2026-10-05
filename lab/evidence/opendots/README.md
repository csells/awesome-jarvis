# OpenDots candidate test — 2026-10-05

**Later adapted test:** the [existing OSS voice stack and local CopilotKit runtime now have live call evidence](adapted/README.md), including recorded replies, interruption, page creation and same-chat text follow-up. The report below preserves the original stock/partial test and its blockers.

**Decision: add to the Watch List.** A browser call is a useful Jarvis interface, including on a phone: the implementation starts continuous duplex audio with one tap rather than requiring a tap for each utterance. The absence of a wake word does not disqualify this project. It is a young MIT-licensed workspace with real compute and document tools, but live calling remains blocked in this test environment, and spoken approvals/cancellation and automatic coordination between Dots are missing.

Tested [CopilotKit/OpenDots](https://github.com/CopilotKit/OpenDots/tree/71efd82cd883df7b107d663bd36435a1d8a2d12a) at `71efd82cd883df7b107d663bd36435a1d8a2d12a`, on Apple silicon macOS, Node 26.8.2 and Chrome for Testing 154.0.8037.92. The upstream checkout stayed clean. Desktop viewport: 1440 × 1000; touch-enabled phone viewport: 390 × 844. **This was mobile browser emulation, not a physical phone, cellular-network test or iOS Safari test.**

## Results

| Check | Result | Evidence |
|---|---|---|
| Install and production build | PASS | Lockfile install and `npm run build` succeeded. Vite reported large chunks. [Install log](install.log), [build log](build.log). |
| Upstream automated tests | PASS on serial rerun | First parallel run: 180 passed, two five-second timeouts. Rerun with `--maxWorkers=1`: all 182 tests across 37 files passed. These tests use fixtures and do not establish live voice or cloud integration. [First run](tests.log), [serial run](tests-serial.log). |
| Desktop document workflow | PASS | Created a page through the production UI, edited title/body, saved, and verified the exact content through the API. [Results](ui-workflows.json), [screenshot](desktop-page.png). |
| Phone-sized browser workflow | PASS for tested paths | Opened the saved page in a new touch-enabled browser page, verified content and title, checked no horizontal overflow (390-pixel viewport and document width), and exercised global pause/resume. [Results](ui-workflows.json), [mobile screenshot](mobile-page.png), [setup screen](mobile.png). |
| Real local-model answer | PASS, component only | Direct upstream `DotAgent` through the real TanStack adapter and local Ollama `qwen2.5:7b-instruct-q4_K_M` answered “Two plus two is four.” [Raw events](local-answer-events.json). |
| Real local-model tool execution | PASS, component only | The agent invoked `create_space_page`; SQLite contained title `Jarvis lab proof` and exact body `The violet notebook has seven pages.` Its reply linked the saved page. [Raw events](local-page-events.json), [verified result](live-component-results.json). |
| Stock browser conversation and call | BLOCKED | Both API attempts returned HTTP 503 with the missing Intelligence/model configuration. The UI disables starting a conversation. No successful call, audio capture, barge-in or voice-delegated job is claimed. [Setup screenshot](setup.png), [responses](ui-workflows.json). |
| Call approval, spoken cancellation and multiple-agent supervision | Not established | Code exposes `ask_compute` to speech, with no dedicated approve/deny/cancel tool. Automatic multi-Dot delegation remains future work. See source findings below. |

The local compute probe is deliberately narrower than a connected conversation. It constructs upstream `DotAgent` directly with an isolated SQLite store and a local Ollama endpoint. An `unused-component-probe` value satisfies the agent's Intelligence configuration presence check; **it is not a credential and no Intelligence service is contacted**. The probe rejects any network request outside the local Ollama endpoint. Thread binding is local test setup; thread persistence through Intelligence, the browser chat SDK, scheduling and voice delegation are not tested by it. No model responses or tool results are mocked. [Probe](live-component-probe.mts).

The first probe console summary expected `TEXT_MESSAGE_CONTENT`; upstream emitted `TEXT_MESSAGE_CHUNK`. The corrected summary was reconstructed from the retained original event stream, not a new model run or an invented answer. The reproducible probe now handles both event types. One initial browser script expected the conversation welcome heading instead of the setup heading and timed out; the corrected UI run passed. Neither harness issue is a product failure.

## Hallmarks and phone-call interpretation

| Hallmark | Source assessment | Hands-on coverage |
|---|---|---|
| Voice | Partial under the list's existing rubric: tap-to-start continuous calls, spoken replies and configured interruption; no wake listener | BLOCKED for actual calling. |
| Hands-free | Partial: voice during a call, with UI controls for approvals, cancellation and hangup | Global pause/resume tested by touch-style browser interaction, not voice. |
| Visual | Full from code: assistant states, captions, activity and computer panels | PARTIAL: actual desktop/mobile workspace and documents inspected; active call/work states remain code-reviewed. |
| Oversight | Partial: speech-to-specialist compute and scheduled work controls, not automatic teams | Direct agent tool execution verified; end-to-end voice/background supervision blocked. |

Two source assessments underpin this decision. The independent review initially received the project and hallmark questions without the first review's scores; its later phone-focused follow-up was informed by the discussion and is not an additional blind review. Source scores are not runtime passes.

## Verified source findings

- **Continuous browser call:** `getUserMedia`, WebRTC audio, captions, mute, speaker mute and call minimization are wired to the conversation. Speech configuration requests semantic VAD and interruption. This is stronger than a transcription microphone button. [Client lifecycle](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/src/client/useVoice.ts), [call UI](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/src/client/CallView.tsx).
- **Browser calling, not a telephone number:** no PSTN/incoming-call or native phone integration was found. Mobile browser calling needs HTTPS and microphone permission. Phone lock-screen, background audio, Bluetooth and network handoff are untested. [Call setup](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/docs/SETUP.md#calls).
- **Call bounds:** the service caps a call at 15 minutes and six delegated compute requests. Ending a call aborts pending compute; interrupting the spoken reply is not itself a compute-cancellation command. [Voice service](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/src/server/voice.ts).
- **Navigation and recovery:** changing away from the keyed chat unmounts its voice hook and ends the call. A WebRTC disconnect/failure or call-status polling error ends it; no automatic reconnect was found. Inference: changing mobile networks may be disruptive. This was not reproduced on a physical phone. [Chat mounting](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/src/client/App.tsx), [cleanup and polling](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/src/client/useVoice.ts).
- **Approvals:** the page-review card is an optional browser tool. Ordinary permitted page writes execute directly, as the local-model probe demonstrated. Speech exposes `ask_compute`, not a spoken approval/denial/cancel tool. Computer capability permissions default off; once enabled, they authorize actions rather than prompting for every command. [Page tools](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/src/server/page-tools.ts), [computer defaults](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/src/server/computer-store.ts).
- **Supervision:** speech delegates to the selected specialist in the same conversation. The scheduled runner serializes tasks, and model turns are bounded to 90 seconds. The README explicitly leaves automatic delegation and multi-Dot group conversations for future work. [Runner](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/src/server/runner.ts), [agent](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/src/server/dot-agent.ts), [README](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/README.md#features).

## Dependencies, privacy and limits

The app is self-hosted, but its shipped conversation path uses CopilotKit Intelligence; model access is through an OpenAI-compatible API, and speech uses a separately configured OpenAI Realtime endpoint hardcoded in the voice service. `OPENAI_BASE_URL` changes compute, not speech. The existing local model successfully covered compute; there is no native Claude/Codex subscription CLI adapter. A local speech URL substitution alone would not remove the Intelligence dependency. We did not create a cloud account, retrieve provider credentials, extract subscription tokens, or replace conversation services with a mock. [Configuration](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/.env.example).

Conversation history resides in Intelligence; pages and application metadata reside in SQLite. Research defaults to Parallel and sends queries/selected URLs and a session identifier; it was disabled in this lab run. Optional OpenBot computers use a pinned source version but give the supervisor access to Docker's engine socket. They were not provisioned in this run. [Setup](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/docs/SETUP.md), [computer deployment](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/compose.computers.yml).

GitHub metadata on the test date: created September 29, 2026; active and not archived; 32 default-branch commits in the preceding 90 days and 11 returned contributors. Those live activity counts may include changes beyond the pinned test commit. MIT license is present. Age and incomplete connected-service validation justify Watch List placement, not the main Jarvis Agents scorecard. [License](https://github.com/CopilotKit/OpenDots/blob/71efd82cd883df7b107d663bd36435a1d8a2d12a/LICENSE).

## Reproduce and cleanup

Clone the pinned repository, run `npm ci --no-audit --no-fund`, `npm run build`, then `npm test -- --reporter=verbose --maxWorkers=1`. The host's npm policy did not run dependency lifecycle scripts; the build succeeded without overriding that policy.

Run `HOST=127.0.0.1 PORT=14310 DATABASE_PATH=<lab-directory>/app.sqlite WEB_SEARCH_PROVIDER=disabled npm start`. The [initial UI driver](ui-probe.mjs) and [workflow driver](ui-workflows.mjs) use the installed Playwright package and isolated Chrome for Testing. Adjust their absolute checkout, evidence and browser paths on another machine. The [component probe](live-component-probe.mts) likewise expects local Ollama with the named model and writes its own `component.sqlite`; run it with `node --import <checkout>/node_modules/tsx/dist/loader.mjs <probe>`.

Every cited screenshot was visually inspected. Retained evidence omits databases and dependencies. The app server and every task-owned browser were stopped. The clean source checkout and isolated lab databases are retained for retesting. The pre-existing Ollama service was left running. No virtual machines, public shares or optional computer containers were started.

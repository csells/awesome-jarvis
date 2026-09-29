# Lab Patches

Small, disclosed changes the lab made to third-party projects so they could be tested without paid keys or full Xcode. None of them changes how an agent behaves beyond what is described. Results obtained with a patch are labelled as such in [testing.md](../../testing.md).

| Patch | Project and commit | What it changes | Why |
|---|---|---|---|
| [omavoice-local-realtime-url.patch](omavoice-local-realtime-url.patch) | [baranskyi/omavoice](https://github.com/baranskyi/omavoice) @ `d91962f` | One line in `daemon/omavoice/realtime.py`: the hardcoded `wss://api.openai.com/v1/realtime` becomes `ws://10.0.2.2:8765/v1/realtime`. | Points the app at the lab's local OpenAI-compatible Realtime server instead of OpenAI. `10.0.2.2` is QEMU user networking's fixed alias for the host; change it for other setups. |
| [omarchy-voice-local-realtime-url.patch](omarchy-voice-local-realtime-url.patch) | [wombatoperator/omarchy-voice](https://github.com/wombatoperator/omarchy-voice) @ `8ef9d60` | One line in `src/omarchy_voice/realtime.py`: `REALTIME_URL` becomes `ws://10.0.2.2:8765/v1/realtime`. | Same as above. Its planner, browser and task workers still call OpenAI and were not patched, so those features stay BLOCKED. |
| [tapq-clt.patch](tapq-clt.patch) | [spaceamoeba-t/tapq](https://github.com/spaceamoeba-t/tapq) @ `f2fc0db` | Wraps every `#if canImport(FoundationModels)` in six files with `&& TAPQ_WITH_FOUNDATION_MODELS`, so the Foundation Models code paths compile out unless that flag is defined. | The FoundationModels macros need full Xcode; with this patch TapQ builds with only the Command Line Tools. It loses the on-device Apple Intelligence reasoner, classifier and summarizer, which the voice tests didn't use. |

Apply one with `git apply <patch>` inside a checkout at the listed commit, and check `git diff` afterwards. For the two URL patches, a copy of the applied diff was saved with the evidence (`git diff` inside the VM matched the patch exactly).

The local voice server has its own compatibility patches, applied at runtime by `voice-server/bin/s2s_serve.py` and `voice-server/bin/audio_serve.py` rather than as diff files; they are listed in the [README](../README.md#local-openai-compatible-voice-stack).

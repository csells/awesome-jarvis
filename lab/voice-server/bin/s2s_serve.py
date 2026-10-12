"""Pocket realtime adapter with client lifecycle and playback compatibility."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 3. Honour turn_detection.create_response == false (OpenAI GA semantics): the server still commits the
#    turn and emits the transcription, but it does not start a response until the client sends
#    response.create. Stock speech-to-speech always answers, so clients that drive responses themselves
#    (omavoice's first turn, TapQ, OpenClicky push-to-talk) got "Cannot create response while another
#    response is in progress".
from speech_to_speech.api.openai_realtime import service as rt_service  # noqa: E402

_orig_otc = rt_service.RealtimeService._on_transcription_completed


def _create_response_disabled(st):
    try:
        td = st.runtime_config.session.audio.input.turn_detection
    except AttributeError:
        return False
    if td is None:
        return False
    val = td.get("create_response") if isinstance(td, dict) else getattr(td, "create_response", None)
    return val is False


def _on_transcription_completed(self, conn_id, event):
    if _create_response_disabled(self._state(conn_id)):
        queue, self.text_prompt_queue = self.text_prompt_queue, None
        try:
            return _orig_otc(self, conn_id, event)
        finally:
            self.text_prompt_queue = queue
    return _orig_otc(self, conn_id, event)


rt_service.RealtimeService._on_transcription_completed = _on_transcription_completed

# 4. Small local LLMs (4-7B) follow the stock voice rule "you may give one brief acknowledgement before the
#    first call" by saying "one sec" and then stopping without the tool call. One extra rule fixes it for
#    qwen2.5:7b-instruct (tool call 6/9 -> 9/9 on omavoice/OpenClaw prompts, see README section 7).
from speech_to_speech.LLM import voice_prompt as _vp  # noqa: E402

_vp.VOICE_SYSTEM_PROMPT_TAIL = _vp.VOICE_SYSTEM_PROMPT_TAIL.rstrip() + (
    "\n- An acknowledgement is never a complete reply: if you say one, the tool call MUST follow in the same "
    "reply. Never end a reply with only an acknowledgement or a promise to look something up.\n"
)

# 5. Accept two GA client events the server does not implement, instead of answering them with an error
#    that clients (omarchy-voice) surface as a fatal status: input_audio_buffer.clear (the server's VAD owns
#    the buffer; nothing uncommitted is kept) and conversation.item.delete (history pruning; ignored).
from speech_to_speech.api.openai_realtime import websocket_router as _wr  # noqa: E402

_orig_dispatch = _wr._dispatch_client_event
_IGNORED_EVENTS = {"input_audio_buffer.clear", "conversation.item.delete"}


async def _dispatch_client_event(unit, session_id, raw, transport, **kw):
    if isinstance(raw, dict) and raw.get("type") in _IGNORED_EVENTS:
        return None
    return await _orig_dispatch(unit, session_id, raw, transport, **kw)


_wr._dispatch_client_event = _dispatch_client_event

# 6. Client-supplied conversation item ids: OpenAI accepts any id (<=32 chars); speech-to-speech insists on
#    its own prefixes (sys_/msg_/fc_/...) and rejects e.g. omarchy-voice's "item_omastate..." system items.
from speech_to_speech.LLM import chat as _chat  # noqa: E402

_orig_ensure_id = _chat._ensure_id


def _ensure_id(value, prefix):
    if value is not None and prefix != "call":
        return value
    return _orig_ensure_id(value, prefix)


_chat._ensure_id = _ensure_id

# 7. LLM request timeout: 20 s is too short for a local 7B model on the first turn of clients with large
#    prompts (omarchy-voice sends a ~9 kB desktop manifest plus dozens of tools; Ollama prefill ~25 s).
from speech_to_speech.LLM import base_openai_compatible_language_model as _bocl  # noqa: E402

_orig_setup = _bocl.BaseOpenAICompatibleHandler.setup
_LLM_TIMEOUT = float(os.environ.get("VOICE_LLM_TIMEOUT", "90"))


def _setup(self, *args, **kwargs):
    kwargs.setdefault("request_timeout_s", _LLM_TIMEOUT)
    return _orig_setup(self, *args, **kwargs)


_bocl.BaseOpenAICompatibleHandler.setup = _setup

# 8. OpenAI-compatible playback lifecycle: generation completion is not audio drain.
from playback_events import install as _install_playback_events  # noqa: E402
from speech_to_speech.api.openai_realtime.webrtc_session import WebRTCSession  # noqa: E402

_install_playback_events(WebRTCSession)

from speech_to_speech.cli import main  # noqa: E402

sys.exit(main())

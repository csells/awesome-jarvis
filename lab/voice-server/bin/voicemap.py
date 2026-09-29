"""Shared OpenAI -> local model/voice aliases for the lab voice servers (no dependencies)."""
import os
import re

# OpenAI voice names -> Kokoro-82M voices. Unknown names fall back to VOICE_DEFAULT_VOICE.
OPENAI_TO_KOKORO = {
    "alloy": "af_alloy", "ash": "am_adam", "ballad": "bm_lewis", "coral": "af_heart",
    "echo": "am_echo", "fable": "bm_fable", "onyx": "am_onyx", "nova": "af_nova",
    "sage": "af_sarah", "shimmer": "af_bella", "verse": "am_michael",
    "marin": "af_heart", "cedar": "bm_george",
}
KOKORO_VOICE_RE = re.compile(r"^[abefhijpz][fm]_[a-z]+$")
DEFAULT_VOICE = os.environ.get("VOICE_DEFAULT_VOICE", "bm_fable")


def kokoro_voice(name):
    n = (name or "").strip().lower()
    if KOKORO_VOICE_RE.match(n):
        return n
    return OPENAI_TO_KOKORO.get(n, DEFAULT_VOICE)

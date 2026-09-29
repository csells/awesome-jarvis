"""mlx-audio API server + an OpenAI Audio API compatibility layer (lab wrapper).

Stock mlx-audio (`mlx_audio.server`) serves /v1/audio/transcriptions and /v1/audio/speech, but it expects
Hugging Face model ids, Kokoro voice names, defaults transcriptions to NDJSON and cannot emit raw `pcm`.
Stock OpenAI clients send model "whisper-1"/"gpt-4o-mini-transcribe"/"tts-1"/"gpt-4o-mini-tts", voices
"alloy"/"marin"/..., omit response_format (OpenAI default: json / mp3) and sometimes ask for pcm/opus/aac.
This wrapper registers two routes in front of mlx-audio's own that normalise those requests and then call
mlx-audio's handlers. Every other route (models, voices, /v1/realtime transcription WS, ...) is unchanged.

Usage: python audio_serve.py --host 127.0.0.1 --port 8766
Env:   VOICE_STT_MODEL (default mlx-community/parakeet-tdt-0.6b-v3)
       VOICE_TTS_MODEL (default mlx-community/Kokoro-82M-bf16)
       VOICE_DEFAULT_VOICE (default bm_fable), VOICE_CORS_ORIGINS (space separated; default: no CORS)
"""
import argparse
import asyncio
import io
import os
import sys
import wave
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voicemap import kokoro_voice  # noqa: E402

import uvicorn  # noqa: E402
from fastapi import File, Form, HTTPException, Request, UploadFile  # noqa: E402
from fastapi.responses import JSONResponse, Response  # noqa: E402
from fastapi.routing import APIRoute  # noqa: E402

import mlx_audio.server as S  # noqa: E402

STT_MODEL = os.environ.get("VOICE_STT_MODEL", "mlx-community/parakeet-tdt-0.6b-v3")
TTS_MODEL = os.environ.get("VOICE_TTS_MODEL", "mlx-community/Kokoro-82M-bf16")
MIME = {"mp3": "audio/mpeg", "opus": "audio/ogg", "aac": "audio/aac", "flac": "audio/flac",
        "wav": "audio/wav", "pcm": "audio/pcm"}
FFMPEG_OUT = {"mp3": ["-f", "mp3", "-b:a", "96k"], "opus": ["-f", "ogg", "-c:a", "libopus", "-b:a", "48k"],
              "aac": ["-f", "adts", "-c:a", "aac", "-b:a", "96k"], "flac": ["-f", "flac"]}


def _hf_id(name: Optional[str], default: str) -> str:
    return name if name and "/" in name else default


async def transcriptions(
    request: Request,
    file: UploadFile = File(...),
    model: str = Form("whisper-1"),
    language: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None),
    response_format: str = Form("json"),
    temperature: Optional[float] = Form(None),
    stream: bool = Form(False),
    timestamp_granularities: Optional[List[str]] = Form(None, alias="timestamp_granularities[]"),
):
    fmt = response_format if response_format in ("json", "text", "verbose_json", "ndjson") else "json"
    return await S.stt_transcriptions(
        request=request, file=file, model=_hf_id(model, STT_MODEL), language=language or None,
        verbose=False, max_tokens=1024, chunk_duration=30.0, frame_threshold=25, stream=False,
        context=None, prefill_step_size=2048, text=None, response_format=fmt,
        word_timestamps=False, timestamp_granularities=None,
    )


async def _ffmpeg(wav: bytes, args: List[str]) -> bytes:
    p = await asyncio.create_subprocess_exec(
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", "pipe:0", *args, "pipe:1",
        stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await p.communicate(wav)
    if p.returncode != 0:
        raise HTTPException(500, f"ffmpeg: {err.decode(errors='replace')[-300:]}")
    return out


async def speech(request: Request):
    body = await request.json()
    text = body.get("input")
    if not text:
        raise HTTPException(400, "input is required")
    voice = kokoro_voice(body.get("voice"))
    fmt = (body.get("response_format") or "mp3").lower()
    if fmt not in MIME:
        fmt = "mp3"
    req = S.SpeechRequest(model=_hf_id(body.get("model"), TTS_MODEL), input=text, voice=voice,
                          speed=float(body.get("speed") or 1.0), lang_code=voice[0],
                          response_format="wav", stream=False)
    resp = await S.tts_speech(req, request)
    wav = b"".join([c if isinstance(c, bytes) else c.encode() async for c in resp.body_iterator])
    if fmt == "wav":
        data = wav
    elif fmt == "pcm":  # OpenAI pcm = raw 24 kHz mono s16le (Kokoro's native rate)
        data = await _ffmpeg(wav, ["-f", "s16le", "-ac", "1", "-ar", "24000"])
    else:
        data = await _ffmpeg(wav, FFMPEG_OUT[fmt])
    return Response(content=data, media_type=MIME[fmt])


async def health():
    return JSONResponse({"ok": True, "stt_model": STT_MODEL, "tts_model": TTS_MODEL})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8766)
    a = ap.parse_args()
    S.app.router.routes[0:0] = [
        APIRoute("/v1/audio/transcriptions", transcriptions, methods=["POST"]),
        APIRoute("/v1/audio/speech", speech, methods=["POST"]),
        APIRoute("/health", health, methods=["GET"]),
    ]
    origins = os.environ.get("VOICE_CORS_ORIGINS", "").split()
    if origins:
        S.setup_cors(S.app, origins)
    uvicorn.run(S.app, host=a.host, port=a.port, log_level="info")


if __name__ == "__main__":
    main()

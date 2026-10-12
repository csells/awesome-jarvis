"""Pocket service's Parakeet transcription worker."""
import argparse
import os
from typing import List, Optional
import uvicorn
from fastapi import File, Form, Request, UploadFile
import mlx_audio.server as S
from transcription_app import create_app
STT_MODEL=os.environ.get('VOICE_STT_MODEL','mlx-community/parakeet-tdt-0.6b-v3')
def _hf_id(name, default):
    return name if name and '/' in name else default

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


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--host',default='127.0.0.1')
    ap.add_argument('--port',type=int,default=8766)
    args=ap.parse_args()
    uvicorn.run(create_app(transcriptions,STT_MODEL,S.app_lifespan),host=args.host,port=args.port)
if __name__=='__main__':main()

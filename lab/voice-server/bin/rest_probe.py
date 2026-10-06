"""STT + TTS round-trip against the local OpenAI Audio API using the stock OpenAI Python SDK.

Usage: rest_probe.py OUTDIR WAV [WAV...]   (env VOICE_AUDIO_BASE, default http://127.0.0.1:8766/v1)
"""
import json
import os
import sys
import time

from openai import OpenAI

base = os.environ.get("VOICE_AUDIO_BASE", "http://127.0.0.1:8766/v1")
out, wavs = sys.argv[1], sys.argv[2:]
os.makedirs(out, exist_ok=True)
session_file = os.environ.get("VOICE_SESSION_FILE")
key = json.load(open(session_file))["api_key"] if session_file else "sk-local-dummy"
c = OpenAI(base_url=base, api_key=key)
res = {"base_url": base, "stt": [], "tts": []}


def stt(path, model="whisper-1", **kw):
    t = time.perf_counter()
    with open(path, "rb") as f:
        r = c.audio.transcriptions.create(model=model, file=f, **kw)
    dt = time.perf_counter() - t
    text = r if isinstance(r, str) else r.text
    return text.strip(), round(dt, 3)


for w in wavs:
    for i in range(2):  # first call may include model load
        text, dt = stt(w, model="gpt-4o-mini-transcribe" if i else "whisper-1")
        res["stt"].append({"file": w, "run": i, "text": text, "seconds": dt})
        print(f"STT {os.path.basename(w)} run{i}: {dt:.3f}s  {text!r}")

phrases = [("fable", "mp3", "Good evening, sir. All systems are online and the lab is ready for testing."),
           ("alloy", "wav", "The quick brown fox jumps over the lazy dog."),
           ("marin", "pcm", "Barge in whenever you like; I will stop talking.")]
for voice, fmt, text in phrases:
    t = time.perf_counter()
    r = c.audio.speech.create(model="tts-1", voice=voice, input=text, response_format=fmt)
    data = r.read()
    dt = time.perf_counter() - t
    p = os.path.join(out, f"tts-{voice}.{fmt}")
    open(p, "wb").write(data)
    if fmt == "pcm":  # wrap raw 24 kHz s16le for the round trip
        import wave
        p2 = p + ".wav"
        with wave.open(p2, "wb") as ww:
            ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(24000); ww.writeframes(data)
        p = p2
    back, dt2 = stt(p)
    res["tts"].append({"voice": voice, "format": fmt, "bytes": len(data), "seconds": round(dt, 3),
                       "input": text, "roundtrip_transcript": back, "stt_seconds": dt2, "file": p})
    print(f"TTS {voice}/{fmt}: {len(data)} B in {dt:.3f}s -> STT {dt2:.3f}s: {back!r}")

json.dump(res, open(os.path.join(out, "rest-probe.json"), "w"), indent=2)

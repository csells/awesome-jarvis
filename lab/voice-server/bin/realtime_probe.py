"""Scripted OpenAI Realtime (GA) WebSocket client: speaks WAVs like a microphone, records what comes back.

Usage: realtime_probe.py URL OUTDIR SCENARIO
  URL       e.g. ws://127.0.0.1:8765/v1/realtime?model=gpt-realtime
  SCENARIO  turn     : q1 -> one spoken answer
            bargein  : q2 (long story) -> 2 s into the answer, speak q3 -> first response cancelled by
                       server VAD (turn_detected), second response answers q3
            cancel   : q2 -> 1 s into the answer, client sends response.cancel
Mic emulation: 24 kHz pcm16 in 20 ms chunks at real-time pace, silence between utterances (like a live mic).
Writes OUTDIR/<scenario>-events.jsonl, <scenario>-resp<N>.wav (assistant audio), <scenario>-summary.json.
"""
import asyncio
import base64
import json
import os
import sys
import time
import wave

import websockets

URL, OUT, SCEN = sys.argv[1], sys.argv[2], sys.argv[3]
UTT = os.environ.get("UTT_DIR", os.path.join(os.path.dirname(__file__), "../../out/voice-server/utts"))
RATE, CH = 24000, 480  # 20 ms
os.makedirs(OUT, exist_ok=True)


def pcm(name):
    with wave.open(os.path.join(UTT, name + ".wav")) as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1
        return w.readframes(w.getnframes())


SILENCE = b"\0\0" * CH


async def main():
    t0 = time.perf_counter()
    now = lambda: round(time.perf_counter() - t0, 3)  # noqa: E731
    ev_log = open(os.path.join(OUT, f"{SCEN}-events.jsonl"), "w")
    marks, responses, cur = {}, [], None
    state = {"first_audio": asyncio.Event(), "done": 0, "want_done": 1 if SCEN != "bargein" else 2}
    all_done = asyncio.Event()
    # sk-local-dummy is a placeholder, not a real key; the local server ignores it.
    async with websockets.connect(URL, additional_headers={"Authorization": "Bearer sk-local-dummy"},
                                  max_size=None) as ws:
        await ws.send(json.dumps({"type": "session.update", "session": {
            "type": "realtime", "model": "gpt-realtime", "output_modalities": ["audio"],
            "instructions": "You are JARVIS, a concise voice assistant. Answer briefly and speak naturally.",
            "audio": {
                "input": {"format": {"type": "audio/pcm", "rate": RATE},
                          "transcription": {"model": "gpt-4o-mini-transcribe"},
                          "turn_detection": {"type": "server_vad", "create_response": True,
                                             "interrupt_response": True}},
                "output": {"format": {"type": "audio/pcm", "rate": RATE}, "voice": "cedar"}}}}))

        async def reader():
            nonlocal cur
            async for raw in ws:
                e = json.loads(raw)
                t = e["type"]
                rec = {"t": now(), "type": t}
                if t == "response.output_audio.delta":
                    b = base64.b64decode(e["delta"])
                    if cur is None:
                        cur = {"audio": bytearray(), "transcript": "", "first_audio": now()}
                        responses.append(cur)
                    cur["audio"] += b
                    rec["bytes"] = len(b)
                    state["first_audio"].set()
                else:
                    rec.update({k: v for k, v in e.items() if k not in ("type", "delta", "audio")} if t != "session.created" and t != "session.updated" else {})
                    if "delta" in e and t.endswith("transcript.delta"):
                        rec["delta"] = e["delta"]
                if t == "response.created":
                    cur = {"audio": bytearray(), "transcript": "", "created": now(), "first_audio": None}
                    responses.append(cur)
                    marks.setdefault("response_created", []).append(now())
                elif t == "response.output_audio.delta" and cur.get("first_audio") is None:
                    cur["first_audio"] = now()
                elif t == "response.output_audio_transcript.done":
                    cur["transcript"] = e.get("transcript", "")
                elif t == "response.done":
                    r = e.get("response", {})
                    cur["status"] = r.get("status")
                    cur["status_details"] = r.get("status_details")
                    cur["done"] = now()
                    cur = None
                    state["done"] += 1
                    if state["done"] >= state["want_done"]:
                        all_done.set()
                elif t in ("input_audio_buffer.speech_started", "input_audio_buffer.speech_stopped",
                           "conversation.item.input_audio_transcription.completed", "session.created",
                           "session.updated", "error"):
                    marks.setdefault(t, []).append({"t": now(), **({"transcript": e.get("transcript")} if "transcript" in e else {}),
                                                    **({"error": e.get("error")} if t == "error" else {})})
                ev_log.write(json.dumps(rec) + "\n")

        rtask = asyncio.create_task(reader())
        mic_q: asyncio.Queue = asyncio.Queue()

        async def mic():  # real-time paced: one 20 ms chunk every 20 ms, silence when nothing queued
            nxt = time.perf_counter()
            buf = b""
            while True:
                if not buf and not mic_q.empty():
                    name = mic_q.get_nowait()
                    buf = pcm(name)
                    marks.setdefault("speech_begin", []).append({"t": now(), "utt": name})
                chunk, buf = (buf[:CH * 2], buf[CH * 2:]) if buf else (SILENCE, b"")
                if chunk is not SILENCE and not buf:
                    marks.setdefault("speech_end", []).append(now() + 0.02)
                chunk = chunk.ljust(CH * 2, b"\0")
                await ws.send(json.dumps({"type": "input_audio_buffer.append",
                                          "audio": base64.b64encode(chunk).decode()}))
                nxt += 0.02
                await asyncio.sleep(max(0, nxt - time.perf_counter()))

        mtask = asyncio.create_task(mic())
        await asyncio.sleep(1.0)
        if SCEN == "turn":
            mic_q.put_nowait("q1")
        else:
            mic_q.put_nowait("q2")
            await asyncio.wait_for(state["first_audio"].wait(), 60)
            if SCEN == "bargein":
                await asyncio.sleep(2.0)
                mic_q.put_nowait("q3")
            else:
                await asyncio.sleep(1.0)
                marks["client_cancel"] = now()
                await ws.send(json.dumps({"type": "response.cancel"}))
        try:
            await asyncio.wait_for(all_done.wait(), 90)
        except asyncio.TimeoutError:
            marks["timeout"] = True
        await asyncio.sleep(1.5)
        mtask.cancel(); rtask.cancel()
    ev_log.close()
    summary = {"url": URL, "scenario": SCEN, "marks": marks, "responses": []}
    for i, r in enumerate(responses):
        if not r.get("audio") and r.get("status") is None:
            continue
        p = os.path.join(OUT, f"{SCEN}-resp{i}.wav")
        with wave.open(p, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(bytes(r["audio"]))
        summary["responses"].append({k: v for k, v in r.items() if k != "audio"} |
                                    {"audio_seconds": round(len(r["audio"]) / 2 / RATE, 2), "wav": p})
    se = marks.get("speech_end", [])
    if se:
        # latency: end of the user's last utterance before each response -> first audio byte of that response
        for r in summary["responses"]:
            prior = [s for s in se if r.get("first_audio") and s <= r["first_audio"]]
            if prior and r.get("first_audio"):
                r["latency_speech_end_to_first_audio_s"] = round(r["first_audio"] - prior[-1], 3)
    json.dump(summary, open(os.path.join(OUT, f"{SCEN}-summary.json"), "w"), indent=2)
    print(json.dumps(summary, indent=2))


asyncio.run(main())

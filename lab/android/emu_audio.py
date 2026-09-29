#!/usr/bin/env python3
"""Emulator audio I/O over the Android Emulator gRPC API (no host mic, no virtual audio driver).

  emu_audio.py say "text" [--voice Samantha] [--keep f.wav] [--pad 0.4]   macOS `say` -> 16 kHz WAV -> emulator mic
  emu_audio.py inject f.wav [--pad 0.4]                                    WAV (16-bit PCM) -> emulator mic (injectAudio)
  emu_audio.py record <seconds> out.wav                                    what the emulator plays (streamAudio) -> WAV
  emu_audio.py transcribe f.wav                                            faster-whisper base.en (CPU int8)
  emu_audio.py mic-state                                                   is host-mic passthrough on? (should be False)

gRPC endpoint: localhost:$EMU_GRPC (default 8600), started by emu-start.sh with `-grpc 8600`.
Needs the generated gRPC stubs in ./grpc (see the Android section of ../README.md) and
`pip install grpcio protobuf faster-whisper`.
"""
import os, sys, time, wave, subprocess, tempfile, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "grpc"))


def stub():
    import grpc
    import emulator_controller_pb2_grpc as g
    ch = grpc.insecure_channel(f"localhost:{os.environ.get('EMU_GRPC', '8600')}",
                               options=[("grpc.max_receive_message_length", 64 << 20)])
    return g.EmulatorControllerStub(ch)


def pb():
    import emulator_controller_pb2 as p
    return p


def read_wav(path):
    with wave.open(path, "rb") as w:
        assert w.getsampwidth() == 2, "need 16-bit PCM"
        return w.getframerate(), w.getnchannels(), w.readframes(w.getnframes())


def inject(path, pad=0.4):
    p = pb()
    rate, ch, data = read_wav(path)
    fmt = p.AudioFormat(samplingRate=rate, format=p.AudioFormat.AUD_FMT_S16,
                        channels=p.AudioFormat.Mono if ch == 1 else p.AudioFormat.Stereo,
                        mode=p.AudioFormat.MODE_UNSPECIFIED)
    bpf = 2 * ch
    silence = b"\0" * int(rate * pad) * bpf
    data = silence + data + silence
    chunk = int(rate * 0.02) * bpf  # 20 ms packets, paced in real time

    def gen():
        t0 = time.time()
        for i in range(0, len(data), chunk):
            yield p.AudioPacket(format=fmt, audio=data[i:i + chunk], timestamp=int(time.time() * 1e6))
            target = t0 + (i + chunk) / bpf / rate
            d = target - time.time()
            if d > 0:
                time.sleep(d)
    stub().injectAudio(gen())
    print(f"injected {len(data) / bpf / rate:.2f}s from {path}")


def say(text, voice=None, keep=None, pad=0.4):
    out = keep or tempfile.mktemp(suffix=".wav")
    cmd = ["say", "-o", out, "--data-format=LEI16@16000", "--file-format=WAVE"]
    if voice:
        cmd += ["-v", voice]
    subprocess.run(cmd + [text], check=True)
    inject(out, pad)


def record(seconds, path, rate=16000):
    p = pb()
    fmt = p.AudioFormat(samplingRate=rate, format=p.AudioFormat.AUD_FMT_S16, channels=p.AudioFormat.Mono)
    buf = bytearray()
    end = time.time() + seconds
    it = stub().streamAudio(fmt, timeout=seconds + 2)
    try:
        for pkt in it:
            buf += pkt.audio
            if time.time() >= end:
                break
    except Exception as e:  # deadline is the normal way out when the device is silent
        if "DEADLINE_EXCEEDED" not in str(e):
            raise
    finally:
        it.cancel()
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(bytes(buf))
    import array
    a = array.array("h", bytes(buf))
    peak = max((abs(x) for x in a), default=0) / 32768
    print(f"recorded {len(a) / rate:.2f}s peak={peak:.3f} -> {path}")


def transcribe(path):
    from faster_whisper import WhisperModel
    m = WhisperModel("base.en", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(path, vad_filter=True)
    print(" ".join(s.text.strip() for s in segs))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("say"); a.add_argument("text"); a.add_argument("--voice"); a.add_argument("--keep"); a.add_argument("--pad", type=float, default=0.4)
    a = sp.add_parser("inject"); a.add_argument("wav"); a.add_argument("--pad", type=float, default=0.4)
    a = sp.add_parser("record"); a.add_argument("seconds", type=float); a.add_argument("wav")
    a = sp.add_parser("transcribe"); a.add_argument("wav")
    sp.add_parser("mic-state")
    o = ap.parse_args()
    if o.cmd == "say": say(o.text, o.voice, o.keep, o.pad)
    elif o.cmd == "inject": inject(o.wav, o.pad)
    elif o.cmd == "record": record(o.seconds, o.wav)
    elif o.cmd == "transcribe": transcribe(o.wav)
    elif o.cmd == "mic-state":
        from google.protobuf import empty_pb2
        print(stub().getMicrophoneState(empty_pb2.Empty()))


if __name__ == "__main__":
    main()

"""transcribe <file.wav> [--model base.en] — print the transcript (faster-whisper, CPU int8)."""
import os, sys
from faster_whisper import WhisperModel
args = [a for a in sys.argv[1:]]
model = os.environ.get("LAB_WHISPER_MODEL", "base.en")
if "--model" in args:
    i = args.index("--model"); model = args[i + 1]; del args[i:i + 2]
if len(args) != 1:
    sys.exit("usage: transcribe <file.wav> [--model NAME]")
m = WhisperModel(model, device="cpu", compute_type="int8",
                 download_root=os.environ.get("LAB_WHISPER_DIR", os.path.expanduser("~/.local/share/jarvis-lab/models")))
segs, _ = m.transcribe(args[0], beam_size=5, vad_filter=True)
print(" ".join(s.text.strip() for s in segs).strip())

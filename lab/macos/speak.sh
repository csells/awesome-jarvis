#!/bin/bash
# speak.sh "text" [name]  : host-side TTS (macOS `say`, 16 kHz WAV) -> copy into the guest -> play into
# the guest's virtual mic (BlackHole 2ch). The WAV is kept in $LAB_OUT/macos/tts/<name>.wav.
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"; OUT="${LAB_OUT:-$D/../out}/macos/tts"; mkdir -p "$OUT"
n=${2:-utt-$(date +%H%M%S)}; w="$OUT/$n.wav"
say -v "${LAB_SAY_VOICE:-Samantha}" -o "$w" --data-format=LEI16@16000 "$1"
"$D/vm.sh" put "$w" "/tmp/$n.wav" >/dev/null
"$D/vm.sh" ssh "source ~/lab/bin/lab-env; sox -q /tmp/$n.wav -t coreaudio \"\$LAB_MIC_DEV\" pad 0.3 0"
echo "spoke: $1"

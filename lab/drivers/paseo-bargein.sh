#!/bin/bash
# paseo-bargein.sh <outdir> — inside jl-paseo with pw-driver running on the voice-host page.
# Re-enables voice mode, asks for a long spoken answer, and speaks over it once TTS playback starts.
set -u; out=${1:-/lab/out/paseo-claude}; L=/tmp/lab-logs/paseo-daemon.log
pw click name="^Stop realtime voice and interrupt turn$" w=3000 >/dev/null 2>&1
pw click name="Enable Voice mode" w=5000 >/dev/null
record-out 150 $out/bargein-speaker.wav & recpid=$!
record-mic 150 $out/bargein-mic.wav & micpid=$!
t0=$(date +%s%3N); echo "t0=$t0"
n0=$(grep -c "TTS segment 0 synthesis ready" $L)
say "Please explain in detail, in about two hundred words, everything that Paseo voice mode can do for a developer."
for i in $(seq 1 100); do
  [ "$(grep -c 'TTS segment 0 synthesis ready' $L)" -gt "$n0" ] && break
  [ "$(paseo permit ls -q 2>/dev/null | wc -l)" -gt 0 ] && pw click name="^Accept$" w=1000 >/dev/null
  sleep 1
done
sleep 5; tb=$(date +%s%3N); echo "barge-in at +$(( (tb-t0)/1000 ))s"
pw shot f=$out/09-bargein-speaking.png >/dev/null
say "Stop. Stop talking please, that is enough."
sleep 12; pw shot f=$out/10-bargein-after.png >/dev/null
wait $recpid $micpid
awk -F'"time":' -v t0=$t0 '{split($2,a,","); if (a[1]>=t0) print}' $L | grep -v "Voice input chunk\|ws_runtime\|Client connected\|Client disconnected" \
 | grep -oE '"time":[0-9]+|"msg":"[^"]*"|"transcript":"[^"]*"' | paste -sd' ' | sed 's/"time"/\n&/g' > $out/bargein-daemon-timeline.txt
echo "--- speaker (what the agent said):"; transcribe $out/bargein-speaker.wav
echo "--- mic (what the user said):"; transcribe $out/bargein-mic.wav

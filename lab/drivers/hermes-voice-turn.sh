#!/bin/bash
# hermes-voice-turn.sh <out-prefix> <question> [record-seconds]
# Inside jl-hermes with the Hermes CLI running in tmux session `hermes` (wake word armed):
# says "hey hermes", then the question, records the speaker for the whole turn, snapshots the
# CLI pane when the turn ends, and transcribes what Hermes said.
set -u; out=$1; q=$2; secs=${3:-240}
n0=$(tmux capture-pane -p -t hermes -S -3000 | grep -c "╭─ ☤ Hermes")
record-out "$secs" "$out-speaker.wav" & rec=$!
record-mic "$secs" "$out-mic.wav" & mic=$!
sleep 0.5; say "hey hermes"; sleep 2.5; say "$q"
t0=$(date +%s)
# turn is over when the status line shows no spinner for a while after a reply box appeared
for i in $(seq 1 $((secs/3))); do
  tmux capture-pane -p -t hermes -S -200 > "$out-pane.txt"
  [ "$(tmux capture-pane -p -t hermes -S -3000 | grep -c "╭─ ☤ Hermes")" -gt "$n0" ] && { sleep ${TTS_WAIT:-25}; break; }
  sleep 3
done
tmux capture-pane -p -t hermes -S -200 | grep -v '^\s*$' > "$out-pane.txt"
kill $rec $mic 2>/dev/null; wait $rec $mic 2>/dev/null
echo "== user (mic):";  transcribe "$out-mic.wav"
echo "== hermes (speaker):"; transcribe "$out-speaker.wav"

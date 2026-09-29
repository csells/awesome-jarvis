#!/bin/bash
# lab-happy.sh: Happy CLI (slopus/happy) in the jl-happy container, paired to the Android emulator's Chrome.
#   ./happy/lab-happy.sh build          build jarvis-lab-happy (FROM jarvis-lab-base + happy@1.2.5 + tmux)
#   ./happy/lab-happy.sh up             start jl-happy (creates it if missing) - refuses if another lab container holds jarvis-lab-claude
#   ./happy/lab-happy.sh auth           happy auth login (web flow) in tmux "auth"; prints the connect URL to open on the phone
#   ./happy/lab-happy.sh sessions       start two `happy claude` sessions (tmux sess-a in /workspace/demo-a, sess-b in /workspace/demo-b)
#   ./happy/lab-happy.sh show <tmux>    print a tmux pane (auth | sess-a | sess-b)
#   ./happy/lab-happy.sh down           stop jl-happy (container, volumes and Happy login in jarvis-lab-happy-home are kept)
set -euo pipefail
cd "$(dirname "$0")/.."
LAB=$PWD
LAB_OUT=${LAB_OUT:-$LAB/out}; mkdir -p "$LAB_OUT"
case ${1:-help} in
  build) docker build -f happy/Dockerfile -t jarvis-lab-happy:latest happy ;;
  up)
    others=$(docker ps --filter volume=jarvis-lab-claude --format '{{.Names}}' | grep -v '^jl-happy$' || true)
    [ -z "$others" ] || { echo "jarvis-lab-claude is in use by: $others (one container at a time)" >&2; exit 1; }
    if docker ps -a --format '{{.Names}}' | grep -qx jl-happy; then docker start jl-happy >/dev/null
    else docker run -d --name jl-happy --shm-size=512m -v jarvis-lab-claude:/lab-claude -e CLAUDE_CONFIG_DIR=/lab-claude \
           -v "$LAB_OUT:/lab/out" -v jarvis-lab-happy-home:/root/.happy jarvis-lab-happy:latest >/dev/null; fi
    echo "jl-happy up" ;;
  auth)
    docker exec jl-happy bash -c 'tmux kill-session -t auth 2>/dev/null; tmux new-session -d -s auth -x 200 -y 50 "happy auth login; sleep 3600"; sleep 6; tmux send-keys -t auth 2; sleep 1; tmux send-keys -t auth Enter; sleep 6; tmux capture-pane -p -J -t auth | grep -oE "https://app.happy.engineering/terminal/connect#key=[A-Za-z0-9_-]+" | head -1' ;;
  sessions)
    docker exec jl-happy bash -c 'for s in a b; do tmux kill-session -t sess-$s 2>/dev/null || true; tmux new-session -d -s sess-$s -x 200 -y 50 -c /workspace/demo-$s "happy claude; sleep 3600"; done; sleep 20; for s in a b; do echo "== sess-$s"; tmux capture-pane -p -J -t sess-$s | grep -v "^$" | tail -6; done' ;;
  show) docker exec jl-happy tmux capture-pane -p -J -t "${2:?tmux session}" ;;
  down) docker stop jl-happy ;;
  *) sed -n 2,9p "$0" ;;
esac

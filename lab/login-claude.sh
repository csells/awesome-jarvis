#!/bin/bash
# login-claude.sh <container> [user]                       start a Claude subscription login
# login-claude.sh <container> [user] --code-file <file>    finish it with the one-time code
#
# Logs the official Claude Code CLI in to your Claude subscription INSIDE a lab container, so the
# login lands in the Docker volume `jarvis-lab-claude` (mounted at /lab-claude, CLAUDE_CONFIG_DIR).
# Every lab container that mounts that volume then shares this one login; nothing is read from the
# host's ~/.claude or Keychain.
#
# Step 1 runs `claude auth login --claudeai` in a tmux session named `claude-login` and prints only
# the sign-in URL. Open it in a browser, approve, and save the one-time code it shows to a file.
# Step 2 types the code from that file into the waiting login (it is never echoed or put in argv),
# then prints `claude auth status` with anything that looks like a token filtered out.
#
# Security: the resulting OAuth credentials sit in plaintext in the volume (/lab-claude/.credentials.json),
# readable by root in any container that mounts it. Use it only for the lab, one container at a time,
# and sign out (`claude auth logout` in a container, or revoke the session on claude.ai) when done.
set -euo pipefail
c=${1:?usage: login-claude.sh <container> [user] [--code-file FILE]}; u=${2:-root}
if [ "${3:-}" = "--code-file" ]; then
  code=$(tr -d '[:space:]' < "${4:?code file}")
  docker exec -u "$u" "$c" tmux send-keys -t claude-login -l "$code"
  docker exec -u "$u" "$c" tmux send-keys -t claude-login Enter
  sleep 5
  docker exec -u "$u" -e CLAUDE_CONFIG_DIR=/lab-claude "$c" claude auth status 2>&1 | grep -viE "token|key|email" || true
  exit 0
fi
docker exec -u 0 "$c" sh -c "mkdir -p /lab-claude && chown $( [ "$u" = root ] && echo 0 || echo 1000 ) /lab-claude"
docker exec -u "$u" "$c" sh -c 'command -v tmux >/dev/null' || { echo "tmux missing in $c" >&2; exit 1; }
docker exec -u "$u" "$c" tmux kill-session -t claude-login 2>/dev/null || true
docker exec -u "$u" -e CLAUDE_CONFIG_DIR=/lab-claude "$c" tmux new-session -d -s claude-login -x 400 -y 50 \
  "env CLAUDE_CONFIG_DIR=/lab-claude claude auth login --claudeai; sleep 600"
sleep 6
docker exec -u "$u" "$c" tmux capture-pane -p -t claude-login -J | grep -oE 'https://[^ ]+' | head -1

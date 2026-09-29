#!/bin/bash
# login-claude-vm.sh              start `claude auth login --claudeai` in guest tmux session `claude-login`, print ONLY the URL
# login-claude-vm.sh --code-file F feed the one-time code from file F (never echoed), then show `claude auth status`
# The guest keeps the login in the default ~/.claude of the Omarchy owner. Nothing is read from the host.
# To reuse the lab's existing login instead of signing in again, see share-claude-login-vm.sh.
set -euo pipefail
V="$(cd "$(dirname "$0")" && pwd)/vmctl"
if [ "${1:-}" = "--code-file" ]; then
  code=$(tr -d '[:space:]' < "${2:?code file}")
  printf '%s' "$code" | "$V" ssh 'c=$(cat); tmux send-keys -t claude-login -l "$c"; tmux send-keys -t claude-login Enter' >/dev/null
  sleep 6
  "$V" ssh 'bash -lc "claude auth status"' 2>&1 | grep -viE "token|key|email" || true
  exit 0
fi
"$V" ssh 'tmux kill-session -t claude-login 2>/dev/null; tmux new-session -d -s claude-login -x 400 -y 50 "bash -lc \"claude auth login --claudeai; sleep 900\""' >/dev/null
for _ in $(seq 20); do
  url=$("$V" ssh 'tmux capture-pane -p -J -t claude-login' 2>/dev/null | grep -oE 'https://[^ ]+' | head -1 || true)
  [ -n "$url" ] && { echo "$url"; exit 0; }
  sleep 2
done
echo "no URL yet; inspect with: $V ssh tmux capture-pane -p -t claude-login" >&2; exit 1

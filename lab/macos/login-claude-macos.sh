#!/bin/bash
# login-claude-macos.sh               start `claude auth login --claudeai` in guest tmux session
#                                     `claude-login` and print ONLY the sign-in URL
# login-claude-macos.sh --url         re-print the URL from the running session
# login-claude-macos.sh --code-file F feed the one-time code from host file F (never echoed; sent over
#                                     SSH stdin into a tmux paste buffer), then show `claude auth status`
# Runs against the lab's Tart VM (must be started: macos/vm.sh start). The login is stored in the guest
# user's own ~/.claude; nothing is read from the host.
set -euo pipefail
VMSH="$(cd "$(dirname "$0")" && pwd)/vm.sh"
G='source ~/lab/bin/lab-env;'
url() { "$VMSH" ssh "$G tmux capture-pane -p -J -t claude-login -S -200" | tr -d '\r' | grep -oE 'https://claude\.(ai|com)/[^ ]+' | tail -1; }
case "${1:-}" in
  --url) url ;;
  --code-file)
    f=${2:?code file}
    tr -d '[:space:]' < "$f" | "$VMSH" ssh "$G tmux load-buffer -b code - && tmux paste-buffer -d -b code -t claude-login && tmux send-keys -t claude-login Enter"
    sleep 8
    "$VMSH" ssh "$G tmux capture-pane -p -J -t claude-login | tail -5; claude auth status 2>&1" | grep -viE 'token|secret|key' || true
    ;;
  "")
    "$VMSH" ssh "$G tmux kill-session -t claude-login 2>/dev/null; tmux new-session -d -s claude-login -x 400 -y 50 'source ~/lab/bin/lab-env; claude auth login --claudeai; sleep 900'"
    for _ in $(seq 1 20); do sleep 2; u=$(url || true); [ -n "$u" ] && { echo "$u"; exit 0; }; done
    echo "no URL yet; pane:" >&2; "$VMSH" ssh "$G tmux capture-pane -p -t claude-login" >&2; exit 1
    ;;
  *) sed -n '2,7p' "$0"; exit 1 ;;
esac

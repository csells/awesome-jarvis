#!/bin/bash
# share-claude-login.sh — reuse the lab's one Claude Code login inside the disposable macOS test VM.
#
# Source: the Docker volume `jarvis-lab-claude` that ../login-claude.sh logged in (never the host's
# ~/.claude or Keychain). The credentials file is read by a throwaway alpine container into a 0600 temp
# file on the host, streamed over SSH stdin into the guest, and deleted. Nothing is printed except the
# remaining lifetime and `claude auth status` (loggedIn / authMethod / subscriptionType).
#
# In the guest only the short-lived ACCESS token is kept (not the refresh token): it is written to
# ~/.claude-lab-token (0600) and exported as CLAUDE_CODE_OAUTH_TOKEN for SSH shells (~/.zshenv) and for
# the GUI session (launchctl setenv), so the official `claude` CLI works there. It expires after about
# eight hours and is not refreshed here; re-run this script to re-sync.
#
# Trade-offs, stated plainly:
#  * launchctl setenv makes the token visible to EVERY app started in the guest's GUI session, not just
#    Claude Code. Start agents that must not see it with `env -u CLAUDE_CODE_OAUTH_TOKEN ...`, and never
#    configure an agent to call Anthropic's API directly with it (see ../RULES.md).
#  * The token is plaintext on the guest's disk. Use this only in a throwaway VM you control, and delete
#    the VM (or ~/.claude-lab-token and the launchctl variable) when done.
#  * Anyone with a copy of the token can use your subscription until it expires; revoke by signing the
#    lab login out (`claude auth logout` in a lab container) if the VM is ever exposed.
set -euo pipefail
LAB=$(cd "$(dirname "$0")/.." && pwd)
VOL=${LAB_CLAUDE_VOLUME:-jarvis-lab-claude}
umask 077
tmp=$(mktemp "${TMPDIR:-/tmp}/cc.XXXXXX"); trap 'rm -f "$tmp"' EXIT
docker run --rm -v "$VOL:/c:ro" alpine:3 cat /c/.credentials.json > "$tmp"
"$LAB/macos/vm.sh" ssh true   # make sure SSH is ready before feeding stdin
"$LAB/macos/vm.sh" ssh < "$tmp" '
set -e; umask 077
/usr/bin/python3 -c "
import json, sys, time, os
d = json.load(sys.stdin)[\"claudeAiOauth\"]
p = os.path.expanduser(\"~/.claude-lab-token\")
open(p, \"w\").write(d[\"accessToken\"])
print(\"token stored; valid for about\", round((d[\"expiresAt\"] / 1000 - time.time()) / 3600, 1), \"h\")
"
grep -q claude-lab-token ~/.zshenv 2>/dev/null || echo "[ -r ~/.claude-lab-token ] && export CLAUDE_CODE_OAUTH_TOKEN=\$(cat ~/.claude-lab-token)" >> ~/.zshenv
sudo launchctl asuser "$(id -u)" launchctl setenv CLAUDE_CODE_OAUTH_TOKEN "$(cat ~/.claude-lab-token)"
export PATH=$HOME/.local/bin:/opt/homebrew/bin:$PATH
CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude-lab-token) claude auth status 2>&1 | grep -E "loggedIn|authMethod|subscriptionType"
'

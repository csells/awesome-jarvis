#!/bin/bash
# share-claude-login-vm.sh — copy the lab's one Claude Code login into the Omarchy VM guest.
#
# Source: the Docker volume `jarvis-lab-claude` that ../login-claude.sh logged in (never the host's
# ~/.claude or Keychain). A throwaway alpine container reads .credentials.json into a 0600 temp file on
# the host; it is streamed over SSH stdin to the guest owner's ~/.claude/.credentials.json (0600) and the
# temp file is deleted. Nothing is printed except `claude auth status` with token-like lines removed.
#
# Trade-offs, stated plainly:
#  * This copies the full OAuth credential, including the refresh token. The guest's Claude Code and the
#    volume's copy will each refresh it; when one rotates the refresh token the other copy stops working
#    after its access token expires (about eight hours). Re-run this script, or log the guest in on its own
#    with login-claude-vm.sh, when that happens. Don't copy it into more places than you need.
#  * The credential is plaintext on the guest disk. Use a throwaway VM you control, and sign out
#    (`claude auth logout`) or delete the VM when you are done.
#  * Only the official `claude` CLI should use it. Don't let agents under test read ~/.claude or call
#    Anthropic's API with it (see ../RULES.md).
set -euo pipefail
D=$(cd "$(dirname "$0")" && pwd)
VOL=${LAB_CLAUDE_VOLUME:-jarvis-lab-claude}
umask 077
tmp=$(mktemp "${TMPDIR:-/tmp}/cc.XXXXXX"); trap 'rm -f "$tmp"' EXIT
docker run --rm -v "$VOL:/c:ro" alpine:3 cat /c/.credentials.json > "$tmp"
"$D/vmctl" ssh 'umask 077; mkdir -p ~/.claude && cat > ~/.claude/.credentials.json' < "$tmp"
"$D/vmctl" ssh 'bash -lc "claude auth status"' 2>&1 | grep -viE "token|key|email" || true

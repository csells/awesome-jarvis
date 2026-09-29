#!/bin/bash
# login-codex.sh <container>
# Device-code login for the Codex CLI INSIDE a running lab container. The token is written to
# /root/.codex, i.e. the shared named volume `jarvis-lab-codex`, so every lab container sees the same
# login afterwards. Prints the verification URL and one-time user code, then waits until the code is
# approved in a browser. The lab never runs this by itself. The token sits in plaintext in the volume
# (/root/.codex/auth.json); sign out with `codex logout` when you are done.
set -euo pipefail
c=${1:?usage: login-codex.sh <container>   (e.g. jl-base, jl-omarchy, jl-paseo, jl-hermes, jl-openclaw)}
tty=-i; [ -t 0 ] && tty=-it
docker exec $tty -e CODEX_HOME=/root/.codex "$c" codex login --device-auth
# Hermes' supervised services run as the non-root `hermes` user: hand it the volume.
docker exec "$c" sh -c 'if [ -x /lab/bin/hermes-lab-codex-perms ]; then /lab/bin/hermes-lab-codex-perms; fi'
docker exec "$c" codex login status || true

#!/bin/bash
# jarvis-lab Docker driver. Usage (run from anywhere; paths are relative to this script):
#   ./lab.sh build [base|omarchy|omarchy-m|paseo|hermes|openclaw|all]   build image(s), log + time in out/
#   ./lab.sh up    <base|omarchy|omarchy-m|paseo|hermes|openclaw>  start the lab container (jl-<name>; omarchy-m: CODEX=1 to mount the Codex volume)
#   ./lab.sh test  <base|omarchy|omarchy-m|paseo|hermes|openclaw>  run that target's no-login smoke test
#   ./lab.sh shell <name>                                       bash inside jl-<name>
#   ./lab.sh down  [name|all]                                   remove lab container(s) (volumes kept)
#   ./lab.sh sizes                                              image sizes
# Every container mounts the named volume jarvis-lab-codex at /root/.codex; most also mount the Claude
# login volume jarvis-lab-claude at /lab-claude. Model logins are never done by the lab itself:
# ./login-claude.sh jl-<name>  or  ./login-codex.sh jl-<name>
# Evidence is written to $LAB_OUT (default: ./out, git-ignored), mounted at /lab/out in every container.
set -euo pipefail
cd "$(dirname "$0")"
LAB=$PWD
LAB_OUT=${LAB_OUT:-$LAB/out}
mkdir -p "$LAB_OUT"
CODEX_MOUNT=(-v jarvis-lab-codex:/root/.codex)
OUT=(-v "$LAB_OUT:/lab/out")
# Claude subscription login lives only in this volume (never the host ~/.claude); shared by lab containers, one at a time.
CLAUDE_MOUNT=(-v jarvis-lab-claude:/lab-claude -e CLAUDE_CONFIG_DIR=/lab-claude)

dockerfile() { case $1 in base) echo base/Dockerfile;; omarchy) echo hey-jarvis/Dockerfile;; omarchy-m) echo omarchy-m/Dockerfile;; *) echo "$1/Dockerfile";; esac; }
context() { case $1 in base) echo base;; *) echo .;; esac; }

build() {
  local n=$1 start rc
  start=$(date +%s)
  set +e; docker build ${NO_CACHE:+--no-cache} -f "$(dockerfile "$n")" -t "jarvis-lab-$n:latest" "$(context "$n")" >"$LAB_OUT/build-$n.log" 2>&1; rc=$?; set -e
  echo "exit=$rc seconds=$(( $(date +%s) - start ))" | tee -a "$LAB_OUT/build-$n.log"
  return $rc
}

up() {
  local n=$1
  docker volume create jarvis-lab-codex >/dev/null
  docker volume create jarvis-lab-claude >/dev/null
  docker rm -f "jl-$n" >/dev/null 2>&1 || true
  case $n in
    base)     docker run -d --name jl-base --shm-size=512m "${CODEX_MOUNT[@]}" "${CLAUDE_MOUNT[@]}" "${OUT[@]}" jarvis-lab-base:latest ;;
    omarchy)  docker run -d --init --name jl-omarchy --shm-size=512m -e OMARCHY_SHELL=1 "${CODEX_MOUNT[@]}" "${OUT[@]}" jarvis-lab-omarchy:latest ;;
    omarchy-m) # Codex volume only when asked (CODEX=1): the entrypoint chowns it to uid 1000 for the `lab` user
              docker run -d --init --name jl-omarchy-m --shm-size=512m ${CODEX:+${CODEX_MOUNT[@]}} "${CLAUDE_MOUNT[@]}" "${OUT[@]}" jarvis-lab-omarchy-m:latest ;;
    paseo)    docker volume create jarvis-lab-paseo-models >/dev/null
              docker run -d --name jl-paseo --shm-size=1g -p 127.0.0.1:6767:6767 "${CODEX_MOUNT[@]}" "${CLAUDE_MOUNT[@]}" "${OUT[@]}" \
                -v jarvis-lab-paseo-models:/root/.paseo/models jarvis-lab-paseo:latest ;;
    hermes)   docker volume create jarvis-lab-hermes-data >/dev/null
              # Claude volume WITHOUT CLAUDE_CONFIG_DIR: Hermes' `anthropic` provider auto-adopts Claude Code
              # logins it can see. The image gives /lab-claude to user `claude` (0700) and exposes Claude only
              # through the `claude` CLI wrapper (sudo -u claude). Local model: host Ollama (Metal) via
              # host.docker.internal:11434.
              docker run -d --name jl-hermes --shm-size=1g -e HERMES_DASHBOARD=1 -e HERMES_DASHBOARD_HOST=127.0.0.1 \
                "${CODEX_MOUNT[@]}" -v jarvis-lab-claude:/lab-claude "${OUT[@]}" -v jarvis-lab-hermes-data:/opt/data jarvis-lab-hermes:latest gateway run ;;
    openclaw) docker volume create jarvis-lab-openclaw-data >/dev/null
              docker run -d --name jl-openclaw --shm-size=1g "${CODEX_MOUNT[@]}" "${CLAUDE_MOUNT[@]}" "${OUT[@]}" \
                -v jarvis-lab-openclaw-data:/root/.openclaw jarvis-lab-openclaw:latest ;;
    *) echo "unknown target $n" >&2; exit 2 ;;
  esac >/dev/null
  echo "jl-$n started"
}

wait_for() { # container, command, seconds
  for _ in $(seq "$3"); do docker exec "$1" bash -c "$2" >/dev/null 2>&1 && return 0; sleep 1; done
  echo "timeout waiting for: $2" >&2; return 1
}

test_target() {
  local n=$1
  case $n in
    base)
      wait_for jl-base "pactl info" 30
      docker exec jl-base lab-selftest /lab/out/base ;;
    omarchy)
      wait_for jl-omarchy "grep -q pronto /tmp/lab-logs/voice-launcher.service.log" 90
      docker exec jl-omarchy bash -c 'systemctl --user stop voice-launcher; LAB_X11=0 lab-selftest /lab/out/omarchy-selftest; systemctl --user start voice-launcher'
      docker exec jl-omarchy jarvis-smoketest /lab/out/omarchy ;;
    omarchy-m)
      wait_for jl-omarchy-m "runuser -u lab -- omarchy-shell shell ping" 120
      docker exec -u lab jl-omarchy-m bash -c 'cat /lab/out/omarchy-m/hyprland-probe.txt | grep -E "== attempt|RESULT|CONCLUSION|scanGPUs|Cannot open backend|Missing protocols"; LAB_X11=0 lab-selftest /lab/out/omarchy-m/selftest'
      docker exec -u lab jl-omarchy-m jarvis-m-smoketest /lab/out/omarchy-m ;;
    paseo)
      wait_for jl-paseo "test -d /root/.paseo/models/local-speech/kokoro-en-v0_19 && ls /root/.paseo/models/local-speech | grep -q parakeet && curl -sf http://127.0.0.1:6767/ -o /dev/null" 600
      sleep 5
      docker exec jl-paseo bash -c '
        set -e; eval "$(lab-env)"; mkdir -p /lab/out/paseo /workspace/demo; cd /workspace/demo
        [ -d .git ] || { git init -q; git -c user.email=lab@local -c user.name=lab commit -q --allow-empty -m init; }
        paseo project ls --host 127.0.0.1:6767 | grep -q /workspace/demo || paseo project create /workspace/demo --host 127.0.0.1:6767 >/dev/null
        echo "== 1. daemon dictation STT (Parakeet via sherpa-onnx), WAV over the websocket protocol"
        say --keep /lab/out/paseo/utt.wav --sink speaker "create a new agent that fixes the failing tests"
        node /lab/bin/paseo-dictate-wav.mjs /lab/out/paseo/utt.wav
        echo "== 2. web client in Chromium (Xvfb, PulseAudio mic = vmic): Start dictation -> say -> Insert transcription"
        node /lab/bin/paseo-web.mjs dictate /lab/out/paseo/dictate-vmic
        echo "== 3. same, headless Chromium with --use-file-for-fake-audio-capture"
        HEADLESS=1 node /lab/bin/paseo-web.mjs dictate /lab/out/paseo/dictate-fakewav /lab/out/paseo/utt.wav' ;;
    hermes)
      wait_for jl-hermes "pactl info && curl -sf http://127.0.0.1:9119/ -o /dev/null" 90
      docker exec jl-hermes bash -c 'LAB_X11=0 lab-selftest /lab/out/hermes-selftest' || echo "!! lab-selftest failed (continuing)"
      docker exec jl-hermes hermes-voice-test /lab/out/hermes ;;
    openclaw)
      wait_for jl-openclaw "pactl info && curl -sf http://127.0.0.1:18789/ -o /dev/null" 90
      docker exec jl-openclaw bash -c 'LAB_X11=0 lab-selftest /lab/out/openclaw-selftest' || echo "!! lab-selftest failed (continuing)"
      docker exec jl-openclaw bash -c 'eval "$(lab-env)"; mkdir -p /lab/out/openclaw
        node /lab/bin/openclaw-ui.mjs shot /lab/out/openclaw/control-ui.png /
        node /lab/bin/openclaw-ui.mjs click Talk /lab/out/openclaw/talk-settings.png >/dev/null && echo /lab/out/openclaw/talk-settings.png
        node /lab/bin/openclaw-ui.mjs click Agents /lab/out/openclaw/agents.png >/dev/null && echo /lab/out/openclaw/agents.png' ;;
    *) echo "unknown target $n" >&2; exit 2 ;;
  esac
}

cmd=${1:-help}; shift || true
case $cmd in
  build)
    t=${1:-all}
    if [ "$t" = all ]; then for n in base omarchy omarchy-m paseo hermes openclaw; do echo "== build $n"; build $n; done; else build "$t"; fi ;;
  up) up "${1:?name}" ;;
  test) test_target "${1:?name}" ;;
  shell) docker exec -it "jl-${1:?name}" bash ;;
  down)
    t=${1:-all}
    if [ "$t" = all ]; then docker rm -f jl-base jl-omarchy jl-omarchy-m jl-paseo jl-hermes jl-openclaw 2>/dev/null || true; else docker rm -f "jl-$t"; fi ;;
  sizes) docker images --format '{{.Repository}}:{{.Tag}}\t{{.Size}}' | grep '^jarvis-lab' ;;
  *) sed -n '2,14p' "$0" ;;
esac

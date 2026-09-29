#!/bin/bash
# guest-setup.sh : provision the jarvis-macos guest (run INSIDE the guest as the guest user, via vm.sh).
# Idempotent. Installs: Homebrew pkgs (node@22, python@3.12, tmux, sox, ffmpeg, whisper-cpp,
# switchaudio-osx), BlackHole 2ch + 16ch (official casks -> existential.audio pkgs),
# whisper.cpp base.en model (sha256 checked), Claude Code CLI (official installer, pinned).
set -euo pipefail
eval "$(/opt/homebrew/bin/brew shellenv)"
export HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_CLEANUP=1 HOMEBREW_NO_ANALYTICS=1
CLAUDE_VERSION=${CLAUDE_VERSION:-2.1.283}

brew update --quiet
brew install node@22 python@3.12 tmux sox ffmpeg whisper-cpp switchaudio-osx jq
brew install --cask blackhole-2ch blackhole-16ch
# coreaudiod must reload to see the new HAL drivers
sudo killall coreaudiod 2>/dev/null || true; sleep 3

mkdir -p ~/lab/models ~/lab/out ~/lab/bin
m=~/lab/models/ggml-base.en.bin
want=a03779c86df3323075f5e796cb2ce5029f00ec8869eee3fdfb897afe36c6d002   # HF LFS sha256 (ggerganov/whisper.cpp)
if ! echo "$want  $m" | shasum -a 256 -c --status 2>/dev/null; then
  curl -fL -o "$m" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
  echo "$want  $m" | shasum -a 256 -c
fi

# Claude Code CLI, official native installer (https://claude.ai/install.sh), pinned version
if ! ~/.local/bin/claude --version 2>/dev/null | grep -q "$CLAUDE_VERSION"; then
  curl -fsSL https://claude.ai/install.sh -o /tmp/claude-install.sh
  bash /tmp/claude-install.sh "$CLAUDE_VERSION"
fi

grep -q 'lab/bin/lab-env' ~/.zprofile 2>/dev/null || echo 'source $HOME/lab/bin/lab-env' >> ~/.zprofile
source ~/lab/bin/lab-env
node --version; python3 --version; tmux -V; sox --version; ~/.local/bin/claude --version
SwitchAudioSource -a

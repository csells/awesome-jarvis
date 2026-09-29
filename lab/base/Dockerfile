# jarvis-lab-base — headless audio/display test bench for voice agents.
# Ubuntu 24.04 arm64. No credentials are baked in; /root/.codex is a named
# volume (jarvis-lab-codex) mounted at run time.
FROM ghcr.io/astral-sh/uv:0.12.19 AS uv

FROM ubuntu:24.04@sha256:008173c23f95b170204355c12626cb5a965d779a7e1283b09e9cffbb1bf33ca3

ARG NODE_VERSION=22.23.3
ARG NODE_SHA256=a44aeb94849a299b22df10b9e622ec2f605c2183501bc40590705131de7c740f
ARG CODEX_VERSION=0.157.1
ARG CLAUDE_CODE_VERSION=2.1.283
ARG PIPER_VERSION=1.8.0
ARG FASTER_WHISPER_VERSION=1.2.1
# rhasspy/piper-voices revision + hashes (same pin hey-jarvis uses)
ARG PIPER_VOICES_REV=39ab474be869e9181350af6a65e4953eef67aaa0
ARG WHISPER_MODEL=base.en

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    XDG_RUNTIME_DIR=/run/user/0 \
    PULSE_SERVER=unix:/run/user/0/pulse/native \
    DISPLAY=:99 \
    LAB_HOME=/lab \
    PATH=/lab/bin:/opt/lab/venv/bin:/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin \
    HF_HUB_DISABLE_TELEMETRY=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates curl git xz-utils jq procps less tini \
      pulseaudio pulseaudio-utils libasound2-plugins alsa-utils libportaudio2 \
      sox libsox-fmt-pulse libsox-fmt-alsa ffmpeg espeak-ng \
      python3.12 python3.12-venv \
      xvfb x11-utils xdotool \
      sway grim swaybg foot wl-clipboard wtype \
      fonts-dejavu-core fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*

# Node 22 from the official tarball, checksum-verified.
RUN curl -fsSL -o /tmp/node.tar.xz https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-arm64.tar.xz \
 && echo "${NODE_SHA256}  /tmp/node.tar.xz" | sha256sum -c - \
 && tar -xJf /tmp/node.tar.xz -C /usr/local --strip-components=1 --exclude='*.md' --exclude=LICENSE \
 && rm /tmp/node.tar.xz && node --version

COPY --from=uv /uv /uvx /usr/local/bin/

# Codex CLI and Claude Code CLI, pinned, NOT logged in.
RUN npm install -g --no-fund --no-audit @openai/codex@${CODEX_VERSION} @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} \
 && npm cache clean --force && codex --version && claude --version

# Lab Python env: Piper TTS + faster-whisper STT.
RUN uv venv -p /usr/bin/python3.12 /opt/lab/venv \
 && VIRTUAL_ENV=/opt/lab/venv uv pip install --no-cache "piper-tts==${PIPER_VERSION}" "faster-whisper==${FASTER_WHISPER_VERSION}"

# Voice + STT model baked in (no network needed at test time).
RUN mkdir -p /opt/lab/voices /opt/lab/models \
 && base=https://huggingface.co/rhasspy/piper-voices/resolve/${PIPER_VOICES_REV}/en/en_US/lessac/medium \
 && curl -fsSL -o /opt/lab/voices/en_US-lessac-medium.onnx      $base/en_US-lessac-medium.onnx \
 && curl -fsSL -o /opt/lab/voices/en_US-lessac-medium.onnx.json $base/en_US-lessac-medium.onnx.json \
 && echo "5efe09e69902187827af646e1a6e9d269dee769f9877d17b16b1b46eeaaf019f  /opt/lab/voices/en_US-lessac-medium.onnx" | sha256sum -c - \
 && echo "efe19c417bed055f2d69908248c6ba650fa135bc868b0e6abb3da181dab690a0  /opt/lab/voices/en_US-lessac-medium.onnx.json" | sha256sum -c - \
 && /opt/lab/venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('${WHISPER_MODEL}', device='cpu', compute_type='int8', download_root='/opt/lab/models')" \
 && rm -rf /root/.cache

ENV LAB_VOICE=/opt/lab/voices/en_US-lessac-medium.onnx \
    LAB_WHISPER_MODEL=${WHISPER_MODEL} \
    LAB_WHISPER_DIR=/opt/lab/models

COPY etc/ /lab/etc/
COPY bin/ /lab/bin/
RUN chmod +x /lab/bin/* && mkdir -p /lab/out /root/.codex && cp /lab/etc/asound.conf /etc/asound.conf

VOLUME ["/root/.codex"]
WORKDIR /lab
ENTRYPOINT ["/usr/bin/tini", "--", "/lab/bin/lab-entrypoint"]
CMD ["sleep", "infinity"]

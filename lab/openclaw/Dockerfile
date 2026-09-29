# jarvis-lab-openclaw — OpenClaw Gateway + Control UI (official -browser image,
# pinned; bundles the `codex` plugin and a Playwright Chromium + Xvfb) with the
# lab's PulseAudio virtual mic/speaker + Piper/faster-whisper helpers so the
# Control UI's browser Talk can be driven headlessly. Runs as root in the lab
# so the Codex home can be the shared /root/.codex volume.
FROM ghcr.io/astral-sh/uv:0.12.19 AS uv
FROM openclaw/openclaw:2026.9.6-browser@sha256:62832668e3e5e139f745f7d3df892c9251eb53318b7d14a76c410dde1f25d730

ARG PIPER_VOICES_REV=39ab474be869e9181350af6a65e4953eef67aaa0
USER root
ENV HOME=/root \
    CODEX_HOME=/root/.codex \
    XDG_RUNTIME_DIR=/run/user/0 \
    PULSE_SERVER=unix:/run/user/0/pulse/native \
    DISPLAY=:99 LAB_WAYLAND=0 \
    PATH=/lab/bin:/opt/lab/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LAB_VOICE=/opt/lab/voices/en_US-lessac-medium.onnx \
    LAB_WHISPER_MODEL=base.en LAB_WHISPER_DIR=/opt/lab/models \
    OPENCLAW_BROWSER_HEADLESS=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      pulseaudio pulseaudio-utils libasound2-plugins alsa-utils sox libsox-fmt-pulse \
      x11-utils ffmpeg jq curl procps \
 && rm -rf /var/lib/apt/lists/*
COPY --from=uv /uv /usr/local/bin/uv

RUN uv venv -p 3.12 --python-preference only-managed /opt/lab/venv \
 && VIRTUAL_ENV=/opt/lab/venv uv pip install --no-cache "piper-tts==1.8.0" "faster-whisper==1.2.1" \
 && mkdir -p /opt/lab/voices \
 && base=https://huggingface.co/rhasspy/piper-voices/resolve/${PIPER_VOICES_REV}/en/en_US/lessac/medium \
 && curl -fsSL -o /opt/lab/voices/en_US-lessac-medium.onnx      $base/en_US-lessac-medium.onnx \
 && curl -fsSL -o /opt/lab/voices/en_US-lessac-medium.onnx.json $base/en_US-lessac-medium.onnx.json \
 && echo "5efe09e69902187827af646e1a6e9d269dee769f9877d17b16b1b46eeaaf019f  /opt/lab/voices/en_US-lessac-medium.onnx" | sha256sum -c - \
 && /opt/lab/venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('base.en', device='cpu', compute_type='int8', download_root='/opt/lab/models')" \
 && rm -rf /root/.cache/huggingface /root/.cache/uv

# Claude Code CLI (same pin as jarvis-lab-base) for OpenClaw's bundled `claude-cli` runtime.
# Its login lives only in the jarvis-lab-claude volume (CLAUDE_CONFIG_DIR=/lab-claude); OpenClaw
# talks to the executable and never reads the tokens.
ARG CLAUDE_CODE_VERSION=2.1.283
RUN npm install -g --no-fund --no-audit --allow-scripts=@anthropic-ai/claude-code @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} && npm cache clean --force && claude --version

COPY base/etc/ /lab/etc/
COPY base/bin/ /lab/bin/
COPY openclaw/bin/ /lab/bin/
RUN chmod +x /lab/bin/* && cp /lab/etc/asound.conf /etc/asound.conf && mkdir -p /lab/out /root/.codex /root/.openclaw

VOLUME ["/root/.codex", "/root/.openclaw"]
EXPOSE 18789
ENTRYPOINT ["tini", "-s", "--", "/lab/bin/lab-entrypoint"]
CMD ["/lab/bin/openclaw-gateway"]

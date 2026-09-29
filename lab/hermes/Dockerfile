# jarvis-lab-hermes — Hermes Agent gateway + dashboard (official image, pinned)
# with the Linux voice stack pre-installed (Docker disables Hermes' lazy
# installs): faster-whisper STT, sounddevice/PortAudio mic, openWakeWord
# ("hey hermes"), Piper TTS; Codex CLI for the codex app-server runtime; and
# the lab's PulseAudio virtual mic/speaker helpers. Build context: the lab/ directory.
FROM nousresearch/hermes-agent:v2026.9.24@sha256:fca358f12efd65bfaaca05884166f15c0e2788375ca30d77061ac1ebc96452b7

ARG CODEX_VERSION=0.157.1
ARG PIPER_VOICES_REV=39ab474be869e9181350af6a65e4953eef67aaa0
USER root
ENV PULSE_SERVER=unix:/tmp/lab-pulse/native \
    PATH=/lab/bin:/opt/hermes/bin:/opt/hermes/.venv/bin:/opt/data/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LAB_WAYLAND=0 LAB_X11=0 LAB_QUIET=1 \
    CODEX_HOME=/root/.codex \
    LAB_VOICE=/opt/lab/voices/en_US-lessac-medium.onnx \
    LAB_WHISPER_MODEL=base.en LAB_WHISPER_DIR=/opt/lab/models

RUN apt-get update && apt-get install -y --no-install-recommends \
      pulseaudio pulseaudio-utils libasound2-plugins libportaudio2 alsa-utils \
      sox libsox-fmt-pulse tmux procps \
 && rm -rf /var/lib/apt/lists/*

# Voice extras at the versions pinned in this release's pyproject.toml ([voice],
# [wake] openWakeWord part) + Piper for the local `piper` TTS provider.
# openwakeword 0.6.0 declares tflite-runtime on Linux, which has no cp313 wheel,
# so Hermes' own lazy install fails on Linux; install it --no-deps with its
# real runtime deps (it runs on onnxruntime here) and prefetch its models.
RUN uv pip install --python /opt/hermes/.venv/bin/python --no-cache \
      "faster-whisper==1.2.1" "sounddevice==0.5.5" "numpy==2.4.3" "onnxruntime==1.27.0" "piper-tts==1.8.0" \
      "tqdm<5" "scipy<2" "scikit-learn<2" "requests<3" \
 && uv pip install --python /opt/hermes/.venv/bin/python --no-cache --no-deps "openwakeword==0.6.0" \
 && /opt/hermes/.venv/bin/python -c "import openwakeword.utils as u; u.download_models()" \
 && /opt/hermes/.venv/bin/python -c "import onnxruntime, openwakeword; print('onnxruntime', onnxruntime.__version__)"

RUN npm install -g --no-fund --no-audit @openai/codex@${CODEX_VERSION} && npm cache clean --force && codex --version

# Claude Code CLI (same pin as jarvis-lab-base) for Hermes' claude-code delegation skill, isolated
# from Hermes: it runs as user `claude` (uid 1000) via a single sudo rule, and only that user can
# read the login volume /lab-claude. Hermes (user `hermes`) never sees CLAUDE_CONFIG_DIR or the tokens.
ARG CLAUDE_CODE_VERSION=2.1.283
RUN apt-get update && apt-get install -y --no-install-recommends sudo && rm -rf /var/lib/apt/lists/* \
 && npm install -g --no-fund --no-audit --allow-scripts=@anthropic-ai/claude-code @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} \
 && npm cache clean --force && claude --version \
 && mkdir -p /usr/local/libexec && ln -s "$(readlink -f /usr/local/bin/claude)" /usr/local/libexec/claude-real && rm /usr/local/bin/claude \
 && groupadd -g 1000 claude && useradd -u 1000 -g claude -m -d /home/claude -s /bin/bash claude \
 && groupadd work && usermod -aG work hermes && usermod -aG work claude
COPY hermes/claude-isolation/claude /usr/local/bin/claude
COPY hermes/claude-isolation/claude-as-claude /usr/local/libexec/claude-as-claude
COPY hermes/claude-isolation/sudoers-claude /etc/sudoers.d/claude
COPY hermes/claude-isolation/010-claude-isolation /etc/cont-init.d/010-claude-isolation
RUN chmod 755 /usr/local/bin/claude /usr/local/libexec/claude-as-claude /etc/cont-init.d/010-claude-isolation \
 && chmod 440 /etc/sudoers.d/claude && visudo -cf /etc/sudoers.d/claude

# Lab helpers (reuse the Hermes venv for Piper/faster-whisper).
COPY base/etc/ /lab/etc/
COPY base/bin/ /lab/bin/
COPY hermes/bin/ /lab/bin/
RUN chmod +x /lab/bin/* && cp /lab/etc/asound.conf /etc/asound.conf \
 && mkdir -p /opt/lab/voices /lab/out /root/.codex && ln -s /opt/hermes/.venv /opt/lab/venv \
 && base=https://huggingface.co/rhasspy/piper-voices/resolve/${PIPER_VOICES_REV}/en/en_US/lessac/medium \
 && curl -fsSL -o /opt/lab/voices/en_US-lessac-medium.onnx      $base/en_US-lessac-medium.onnx \
 && curl -fsSL -o /opt/lab/voices/en_US-lessac-medium.onnx.json $base/en_US-lessac-medium.onnx.json \
 && echo "5efe09e69902187827af646e1a6e9d269dee769f9877d17b16b1b46eeaaf019f  /opt/lab/voices/en_US-lessac-medium.onnx" | sha256sum -c - \
 && /opt/lab/venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('base.en', device='cpu', compute_type='int8', download_root='/opt/lab/models')" \
 && chmod -R a+rX /opt/lab && rm -rf /root/.cache \
 && printf '#!/command/with-contenv bash\n/lab/bin/lab-init\n/lab/bin/hermes-lab-codex-perms\n' > /etc/cont-init.d/005-jarvis-lab \
 && chmod +x /etc/cont-init.d/005-jarvis-lab

VOLUME ["/root/.codex"]

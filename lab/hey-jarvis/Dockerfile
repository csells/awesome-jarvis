# jarvis-lab-omarchy — Omarchy-like target for the hey-jarvis Omarchy plugin.
# Arch Linux ARM (aarch64) — same package names/versions line as Omarchy's Arch
# x86_64 (pacman, python 3.14, quickshell, hyprland, pipewire), run natively on
# Apple Silicon. Build context: the lab/ directory.
FROM menci/archlinuxarm:base-20260926.36223892169@sha256:30546b37ce9a2209af064bd5f722236e0fc4b72d6e52a14799ed0cc6caf55560

ARG HEY_JARVIS_COMMIT=d6ebaa6ca0097082480d9486d8219c7a98be041f
ARG OMARCHY_COMMIT=c5b4db77d68e7fbce5cf11120712ea322557e967
ARG CODEX_VERSION=0.157.1
ARG CLAUDE_CODE_VERSION=2.1.283
ARG LAB_WHISPER_MODEL=base.en

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    HOME=/root \
    XDG_RUNTIME_DIR=/run/user/0 \
    PULSE_SERVER=unix:/run/user/0/pulse/native \
    LAB_AUDIO=pipewire LAB_X11=0 \
    PATH=/usr/local/bin:/lab/bin:/root/.local/bin:/opt/lab/venv/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/bin \
    HF_HUB_DISABLE_TELEMETRY=1 \
    QT_QUICK_BACKEND=software \
    OMARCHY_PATH=/root/.local/share/omarchy

# pacman 7's landlock sandbox cannot run inside Docker Desktop's VM.
RUN sed -i 's/^#DisableSandbox/DisableSandbox/' /etc/pacman.conf \
 && pacman -Syu --noconfirm --needed \
      git curl jq which procps-ng sox dbus \
      python portaudio pipewire pipewire-pulse pipewire-alsa wireplumber libpulse alsa-utils \
      hyprland quickshell sway swaybg grim alacritty foot wl-clipboard wtype mesa \
      nodejs-lts-jod npm \
      ttf-dejavu noto-fonts ttf-jetbrains-mono-nerd \
 && pacman -Scc --noconfirm && rm -rf /var/cache/pacman/pkg/* /var/lib/pacman/sync/* \
 && setcap -r /usr/bin/sway \
 && ldconfig

RUN npm install -g --no-fund --no-audit --allow-scripts=@anthropic-ai/claude-code @openai/codex@${CODEX_VERSION} @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} \
 && npm cache clean --force && codex --version && claude --version

# Lab helpers (same scripts as jarvis-lab-base) + systemd --user shims.
COPY base/etc/ /lab/etc/
COPY base/bin/ /lab/bin/
COPY hey-jarvis/shims/ /usr/local/bin/
COPY hey-jarvis/bin/ /lab/bin/
RUN chmod +x /lab/bin/* /usr/local/bin/* && mkdir -p /lab/out /root/.codex /tmp/lab-logs

# hey-jarvis at a pinned commit, placed where `omarchy plugin add` clones it.
RUN git clone https://github.com/Atzingen/hey-jarvis.git /root/.config/omarchy/plugins/atzingen.jarvis \
 && cd /root/.config/omarchy/plugins/atzingen.jarvis && git checkout -q ${HEY_JARVIS_COMMIT} \
 && git log -1 --format='hey-jarvis %H %cd'

# Run the project's own installer (hash-locked venv, Piper voices, openWakeWord
# models, scripts, unit file). The systemctl shim keeps it from starting the
# service at build time.
RUN cd /root/.config/omarchy/plugins/atzingen.jarvis && LAB_SVC_NOSTART=1 bash install.sh </dev/null \
 && rm -rf /root/.cache/pip

# Pre-fetch the Whisper weights hey-jarvis uses on CPU ("small", pinned revision)
# and the lab's own base.en for `transcribe`; the lab helpers reuse the Jarvis venv.
RUN /root/.local/share/jarvis/venv/bin/python -c "import sys; sys.path.insert(0,'/root/.local/bin'); import jarvis_stt; from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8', **jarvis_stt.whisper_kwargs('small'))" \
 && mkdir -p /opt/lab && ln -s /root/.local/share/jarvis/venv /opt/lab/venv \
 && /opt/lab/venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('${LAB_WHISPER_MODEL}', device='cpu', compute_type='int8', download_root='/opt/lab/models')" \
 && rm -rf /root/.cache/huggingface
ENV LAB_VOICE=/root/.local/share/piper-voices/en_US-lessac-medium.onnx \
    LAB_WHISPER_MODEL=${LAB_WHISPER_MODEL} LAB_WHISPER_DIR=/opt/lab/models

# omarchy-shell (Quickshell config) from Omarchy 4 "quattro", pinned — to host
# the plugin's bar widget the way Omarchy does.
RUN git clone --filter=blob:none https://github.com/omacom/omarchy.git /root/.local/share/omarchy \
 && cd /root/.local/share/omarchy && git checkout -q ${OMARCHY_COMMIT} && git log -1 --format='omarchy %H %cd' \
 && rm -rf .git

VOLUME ["/root/.codex"]
WORKDIR /lab
ENTRYPOINT ["/lab/bin/lab-entrypoint"]
CMD ["sleep", "infinity"]

# jarvis-lab-omarchy-m — Omarchy 4 as Omarchy Mac (Apple Silicon) installs it,
# in an Arch Linux ARM container. Build context: the lab/ directory.
#   * pacman configured exactly as Omarchy Mac does on Apple Silicon:
#     [omarchy] Usage = Sync (pkgs.omarchy.org edge/aarch64; only the named
#     Hyprland targets are installed from it) + [omarchy-aarch64] install repo
#     + [asahi-alarm] + ALARM core/extra/alarm/aur.
#   * Omarchy Mac's own install.sh (pinned commit) run step by step by
#     omarchy-m-install; hardware/boot/systemd-only steps are stubbed and listed
#     in /usr/share/omarchy-m-lab/skipped.txt.
FROM menci/archlinuxarm:base-20260926.36223892169@sha256:30546b37ce9a2209af064bd5f722236e0fc4b72d6e52a14799ed0cc6caf55560

ARG OMARCHY_MAC_REPO=https://github.com/omacom/omarchy-mac.git
ARG OMARCHY_MAC_COMMIT=ba546a61f881c1fe9d79d75ec050eab048b8cb63
ARG CODEX_VERSION=0.157.1
ARG CLAUDE_CODE_VERSION=2.1.283
# 0 = default package set minus heavy end-user apps (see omarchy-m-install); 1 = everything
ARG OMARCHY_FULL_PACKAGES=0

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# 1. Asahi-Alarm-like starting point: ALARM + [asahi-alarm] (the repo the Asahi
#    Alarm installer ships; Omarchy Mac expects it). pacman 7's landlock/syscall
#    sandbox cannot run in Docker Desktop's VM, so it is disabled (container-only).
RUN echo 'Server = https://github.com/asahi-alarm/asahi-alarm/releases/download/$arch' > /etc/pacman.d/mirrorlist.asahi-alarm \
 && sed -i 's/^#DisableSandbox/DisableSandbox/' /etc/pacman.conf \
 && sed -i '0,/^\[core\]/s//[asahi-alarm]\nInclude = \/etc\/pacman.d\/mirrorlist.asahi-alarm\n\n[core]/' /etc/pacman.conf \
 && pacman-key --init && pacman-key --populate archlinuxarm \
 && pacman-key --recv-keys 12CE6799A94A3F1B5DDFFE88F576553597FB8FEB --keyserver hkps://keyserver.ubuntu.com \
 && pacman-key --lsign-key 12CE6799A94A3F1B5DDFFE88F576553597FB8FEB \
 && pacman -Syu --noconfirm --needed asahi-alarm-keyring sudo git base-devel which procps-ng \
 && pacman -Scc --noconfirm

# 2. The regular user the Omarchy installer insists on (it refuses root), with sudo.
RUN useradd -m -u 1000 -G wheel -s /bin/bash lab \
 && echo 'lab ALL=(ALL:ALL) NOPASSWD: ALL' > /etc/sudoers.d/lab && chmod 440 /etc/sudoers.d/lab

# Container shims (systemd user session, journald, udev) + lab tooling.
COPY omarchy-m/shims/ /usr/local/bin/
COPY hey-jarvis/shims/systemctl hey-jarvis/shims/systemd-run hey-jarvis/shims/journalctl hey-jarvis/shims/notify-send /usr/local/bin/
COPY omarchy-m/bin/omarchy-m-install /lab/bin/omarchy-m-install
RUN chmod +x /usr/local/bin/* /lab/bin/* && mkdir -p /lab/out /tmp/lab-logs && chmod 1777 /tmp/lab-logs

# 3. Omarchy Mac at a pinned commit, installed by its own installer (step by step).
USER lab
WORKDIR /home/lab
RUN git clone --filter=blob:none "$OMARCHY_MAC_REPO" omarchy-mac && git -C omarchy-mac checkout -q "$OMARCHY_MAC_COMMIT" \
 && git -C omarchy-mac log -1 --format='omarchy-mac %H %cd (version %(describe:tags))'; cat omarchy-mac/version
RUN OMARCHY_FULL_PACKAGES=$OMARCHY_FULL_PACKAGES /lab/bin/omarchy-m-install 2>&1 | tee /tmp/omarchy-m-install.log; \
    test "${PIPESTATUS[0]}" = 0
USER root
# Lab additions (not part of Omarchy): headless sway as the fallback compositor
# (sway ships cap_sys_nice, which a container cannot grant), sox for the lab
# audio tools, npm for the pinned CLIs, pipewire-pulse/-alsa (on Omarchy's ISO list
# install/omarchy-other.packages; hey-jarvis would `omarchy pkg add` it anyway).
RUN pacman -S --needed --noconfirm sway swaybg sox nodejs npm pipewire-pulse pipewire-alsa \
 && { getcap /usr/bin/sway >/dev/null && setcap -r /usr/bin/sway || true; } \
 && { getcap /usr/bin/Hyprland 2>/dev/null; true; }
RUN cp /tmp/omarchy-m-install.log /usr/share/omarchy-m-lab/install.log \
 && pacman -Q > /usr/share/omarchy-m-lab/packages.txt \
 && pacman -Scc --noconfirm; rm -rf /home/lab/.cache/yay /home/lab/.cache/omarchy-build/sources /var/cache/pacman/pkg/*

# 4. Pinned model CLIs (Omarchy itself installs unpinned codex/claude via mise;
#    see skipped.txt) and the lab's STT for `transcribe`.
RUN npm install -g --no-fund --no-audit --allow-scripts=@anthropic-ai/claude-code \
      @openai/codex@${CODEX_VERSION} @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} \
 && npm cache clean --force && codex --version && claude --version \
 && python -m venv /opt/lab/venv && /opt/lab/venv/bin/pip install -q --no-cache-dir "faster-whisper==1.2.1" "piper-tts==1.8.0" \
 && mkdir -p /opt/lab/voices && base=https://huggingface.co/rhasspy/piper-voices/resolve/39ab474be869e9181350af6a65e4953eef67aaa0/en/en_US/lessac/medium \
 && curl -fsSL -o /opt/lab/voices/en_US-lessac-medium.onnx $base/en_US-lessac-medium.onnx \
 && curl -fsSL -o /opt/lab/voices/en_US-lessac-medium.onnx.json $base/en_US-lessac-medium.onnx.json \
 && echo "5efe09e69902187827af646e1a6e9d269dee769f9877d17b16b1b46eeaaf019f  /opt/lab/voices/en_US-lessac-medium.onnx" | sha256sum -c - \
 && /opt/lab/venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('base.en', device='cpu', compute_type='int8', download_root='/opt/lab/models')" \
 && /opt/lab/venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8', download_root='/home/lab/.local/share/jarvis/models/whisper', revision='536b0662742c02347bc0e980a01041f333bce120')" \
 && chown -R lab:lab /home/lab/.local \
 && chmod -R a+rX /opt/lab && rm -rf /root/.cache

# Runtime shims + lab tooling (after the install so edits don't re-run it).
# uwsm-app: Omarchy/hey-jarvis launch apps through uwsm, which needs a systemd --user session.
COPY omarchy-m/runtime-shims/ /usr/local/bin/
COPY base/etc/ /lab/etc/
COPY base/bin/ /lab/bin/
COPY omarchy-m/bin/ /lab/bin/
RUN chmod +x /usr/local/bin/* /lab/bin/*

ENV HOME=/home/lab USER=lab \
    XDG_RUNTIME_DIR=/run/user/1000 \
    PULSE_SERVER=unix:/run/user/1000/pulse/native \
    LAB_AUDIO=pipewire LAB_X11=0 \
    OMARCHY_PATH=/usr/share/omarchy \
    CODEX_HOME=/root/.codex \
    LAB_VOICE=/opt/lab/voices/en_US-lessac-medium.onnx \
    LAB_WHISPER_MODEL=base.en LAB_WHISPER_DIR=/opt/lab/models \
    QT_QUICK_BACKEND=software \
    PATH=/usr/local/bin:/lab/bin:/home/lab/.local/bin:/usr/share/omarchy/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/bin

WORKDIR /home/lab
ENTRYPOINT ["/lab/bin/omarchy-m-entrypoint"]
CMD ["sleep", "infinity"]

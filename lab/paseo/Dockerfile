# jarvis-lab-paseo — Paseo daemon + bundled web UI, local voice (Parakeet STT +
# Kokoro TTS via sherpa-onnx), Codex CLI as the agent/voice LLM, and a
# Playwright-managed Chromium to drive the web client headlessly.
FROM jarvis-lab-base:latest

ARG PASEO_VERSION=0.9.2
ARG PLAYWRIGHT_VERSION=1.63.0

ENV PASEO_HOME=/root/.paseo \
    PASEO_LISTEN=0.0.0.0:6767 \
    PASEO_WEB_UI_ENABLED=true PASEO_RELAY_ENABLED=false \
    PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright \
    NODE_PATH=/usr/local/lib/node_modules

RUN apt-get update && apt-get install -y --no-install-recommends lbzip2 bzip2 \
 && npm install -g --no-fund --no-audit @getpaseo/cli@${PASEO_VERSION} playwright@${PLAYWRIGHT_VERSION} \
 && npm cache clean --force && paseo --version \
 && playwright install --with-deps chromium \
 && rm -rf /var/lib/apt/lists/* /root/.cache

COPY paseo/config.json /root/.paseo/config.json
COPY paseo/bin/ /lab/bin/
RUN chmod +x /lab/bin/*

EXPOSE 6767
VOLUME ["/root/.codex", "/root/.paseo/models"]
CMD ["/lab/bin/paseo-daemon"]

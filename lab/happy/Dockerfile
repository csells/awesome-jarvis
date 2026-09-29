# jarvis-lab-happy: Happy CLI (slopus/happy) on top of jarvis-lab-base (Node 22, Claude Code 2.1.283, tmux).
FROM jarvis-lab-base:latest
# happy@1.2.5 == GitHub release cli-1.2.5 (2026-09-22); npm integrity sha512-dfSdKlEAKQiIoIBYb6E2ybkP508UkOk+4kzncUCWFCOMJp06iUn5HO+SnJeY6Rr/Wnla/SevW7PwTFC3E2JxRQ==
RUN apt-get update && apt-get install -y --no-install-recommends tmux qrencode && rm -rf /var/lib/apt/lists/*
RUN npm install -g happy@1.2.5
RUN mkdir -p /workspace/demo-a /workspace/demo-b && cd /workspace/demo-a && git init -q && \
    printf 'def add(a, b):\n    return a - b  # bug\n' > calc.py && \
    cd /workspace/demo-b && git init -q && printf '# demo-b\n' > README.md
WORKDIR /workspace

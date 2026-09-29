#!/bin/bash
# vm.sh: driver for the disposable macOS test VM (Tart, Cirrus Labs macOS base image).
#
#   vm.sh create          clone $LAB_MACOS_IMAGE -> $LAB_MACOS_VM, 4 CPU / 8 GB / 100 GB
#   vm.sh start           boot headless (--no-graphics --no-audio), share $LAB_OUT/macos at
#                         "/Volumes/My Shared Files/out" in the guest, install the lab SSH key
#   vm.sh stop            tart stop (keeps the VM)
#   vm.sh ip              print the guest IP
#   vm.sh host-ip         print the host's address as seen from the guest (for configs/*.yaml)
#   vm.sh ssh [cmd...]    SSH as the guest user with the lab key
#   vm.sh put SRC DST     scp host -> guest ;  vm.sh get SRC DST   scp guest -> host
#   vm.sh shot NAME       screencapture in the GUI session -> $LAB_OUT/macos/NAME.png
#   vm.sh vnc             print the VNC URL (guest Screen Sharing)
#   vm.sh recovery        boot into recoveryOS with a window
#
# Env: LAB_MACOS_VM (default jarvis-macos), LAB_MACOS_IMAGE (default ghcr.io/cirruslabs/macos-tahoe-base:latest;
#      pin a digest for reproducibility), LAB_GUEST_USER / LAB_GUEST_PASSWORD (the Cirrus Labs images ship
#      admin/admin; the password is used once, to install the lab key), LAB_OUT (default <lab>/out), TART.
# Tart must run outside any agent sandbox (it needs the Virtualization framework).
set -euo pipefail
VM=${LAB_MACOS_VM:-jarvis-macos}
IMAGE=${LAB_MACOS_IMAGE:-ghcr.io/cirruslabs/macos-tahoe-base:latest}
GUSER=${LAB_GUEST_USER:-admin}
GPASS=${LAB_GUEST_PASSWORD:-admin}
TART=${TART:-$(command -v tart || echo /opt/homebrew/bin/tart)}
LAB=$(cd "$(dirname "$0")/.." && pwd)
KEY=$LAB/macos/ssh/id_ed25519          # generated on first use; git-ignored
OUT=${LAB_OUT:-$LAB/out}/macos
SSHOPTS=(-i "$KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10 -o ServerAliveInterval=15)

ip() { "$TART" ip "$VM" --wait 120 </dev/null; }

ensure_key() {
  [ -f "$KEY" ] || { mkdir -p "$(dirname "$KEY")"; chmod 700 "$(dirname "$KEY")"; ssh-keygen -q -t ed25519 -N '' -C jarvis-lab -f "$KEY"; }
  local h; h=$(ip)
  if ssh -n "${SSHOPTS[@]}" -o BatchMode=yes "$GUSER@$h" true 2>/dev/null; then return 0; fi
  # First use: install the lab key with the image's default password.
  local k; k=$(cat "$KEY.pub")
  LAB_GP=$GPASS expect -c "
    set timeout 30
    spawn ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o PubkeyAuthentication=no $GUSER@$h {mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '$k' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys}
    expect -re {assword:} { send \"\$env(LAB_GP)\r\" }
    expect eof" >/dev/null
  ssh -n "${SSHOPTS[@]}" -o BatchMode=yes "$GUSER@$h" true
}

case "${1:-}" in
  create)
    "$TART" list | awk '{print $2}' | grep -qx "$VM" || "$TART" clone "$IMAGE" "$VM"
    "$TART" set "$VM" --cpu 4 --memory 8192 --disk-size 100
    ;;
  start)
    mkdir -p "$OUT"
    if "$TART" list | awk -v vm="$VM" '$2==vm{print $NF}' | grep -qx running; then echo "already running"; exit 0; fi
    nohup "$TART" run "$VM" --no-graphics --no-audio --dir="out:$OUT" >"$OUT/tart-run.log" 2>&1 &
    ip; ensure_key; echo "up: $(ip)"
    ;;
  stop) "$TART" stop "$VM" ;;
  ip) ip ;;
  host-ip) h=$(ip); ssh -n "${SSHOPTS[@]}" "$GUSER@$h" "route -n get default | awk '/gateway/{print \$2}'" ;;
  ssh) shift; h=$(ip); ensure_key >/dev/null; exec ssh "${SSHOPTS[@]}" "$GUSER@$h" "$@" ;;
  sshT) shift; h=$(ip); exec ssh -t "${SSHOPTS[@]}" "$GUSER@$h" "$@" ;;
  put) h=$(ip); scp -r "${SSHOPTS[@]}" "$2" "$GUSER@$h:$3" ;;
  get) h=$(ip); scp -r "${SSHOPTS[@]}" "$GUSER@$h:$2" "$3" ;;
  shot)
    n=${2:?name}
    # Screenshots go through the Tart Guest Agent (tart exec), which runs in the GUI session. Over SSH,
    # screencapture works but replayd raises a "com.apple.sshd-session is requesting to bypass the system
    # private window picker" alert EVERY time (its approval never persists); the agent's approval does.
    mkdir -p "$OUT"
    "$TART" exec "$VM" /usr/sbin/screencapture -x /tmp/shot.png
    h=$(ip); scp "${SSHOPTS[@]}" "$GUSER@$h:/tmp/shot.png" "$OUT/$n.png" && echo "$OUT/$n.png"
    ;;
  vnc) echo "vnc://$GUSER@$(ip):5900" ;;
  recovery) "$TART" run "$VM" --recovery ;;
  *) sed -n '2,20p' "$0"; exit 1 ;;
esac

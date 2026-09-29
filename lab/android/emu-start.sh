#!/bin/bash
# Start the lab AVD ($JL_AVD, default jarvis-android) headless (no window) with gRPC for mic injection / audio capture.
# Host audio output stays on (no -no-audio); the mic is fed only via gRPC injectAudio (no host mic).
set -euo pipefail
. "$(dirname "$0")/env.sh"
mkdir -p "$JL_OUT"
if adb -s $ANDROID_SERIAL get-state >/dev/null 2>&1; then echo "already running: $ANDROID_SERIAL"; exit 0; fi
# Host mic (CoreAudio record) is unavailable to a headless/agent-launched emulator (no TCC mic grant):
# "coreaudio: Could not initialize record" and the emulator crashes when a guest app opens the mic.
# Use the null input backend; speech is injected over gRPC (emu_audio.py).
export QEMU_AUDIO_IN_DRV=${QEMU_AUDIO_IN_DRV:-none}
nohup emulator -avd "$JL_AVD" -port $EMU_PORT -grpc $EMU_GRPC ${EMU_WINDOW:--no-window} -no-boot-anim \
  -gpu ${EMU_GPU:-swiftshader_indirect} -memory ${EMU_RAM:-4096} -cores ${EMU_CORES:-4} -no-snapshot-load "$@" > "$JL_OUT/emulator.log" 2>&1 &
echo "emulator pid $!"
adb -s $ANDROID_SERIAL wait-for-device
until [ "$(adb -s $ANDROID_SERIAL shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')" = 1 ]; do sleep 2; done
echo "booted: $ANDROID_SERIAL"

#!/bin/bash
# Stop the lab emulator (AVD and data are kept).
. "$(dirname "$0")/env.sh"
adb -s $ANDROID_SERIAL emu kill 2>/dev/null || echo "not running"

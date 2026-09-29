#!/bin/bash
# Keeps answering "Wait" on ANR dialogs while the starved emulator catches up (never "Close app").
. "$(dirname "$0")/env.sh"
while adb -s $ANDROID_SERIAL get-state >/dev/null 2>&1; do
  if adb shell dumpsys window 2>/dev/null | grep -q 'mCurrentFocus=.*Application Not Responding'; then
    timeout 60 adb shell uiautomator dump /sdcard/anr.xml >/dev/null 2>&1
    b=$(adb shell cat /sdcard/anr.xml 2>/dev/null | grep -oE 'resource-id="android:id/aerr_wait"[^>]*bounds="\[[0-9]+,[0-9]+\]\[[0-9]+,[0-9]+\]"' | grep -oE '\[[0-9]+,[0-9]+\]\[[0-9]+,[0-9]+\]')
    if [ -n "$b" ]; then set -- $(echo "$b" | head -1 | sed -E 's/\[([0-9]+),([0-9]+)\]\[([0-9]+),([0-9]+)\]/\1 \2 \3 \4/'); x=$(( ($1+$3)/2 )); y=$(( ($2+$4)/2 )); adb shell input tap $x $y; echo "$(date +%T) ANR -> Wait ($x,$y)"; fi
  fi
  sleep 5
done

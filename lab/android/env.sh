# source me: environment for the jarvis-lab Android track (paths default to Homebrew's layout)
_JL_HERE=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)
export ANDROID_SDK_ROOT=${ANDROID_SDK_ROOT:-$(brew --prefix 2>/dev/null || echo /opt/homebrew)/share/android-commandlinetools}
export ANDROID_HOME=$ANDROID_SDK_ROOT
export JAVA_HOME=${JAVA_HOME:-$(brew --prefix openjdk@17 2>/dev/null || echo /opt/homebrew/opt/openjdk@17)/libexec/openjdk.jdk/Contents/Home}
export PATH=$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/emulator:$JAVA_HOME/bin:$PATH
export JL_ANDROID=$_JL_HERE
export JL_OUT=${JL_OUT:-${LAB_OUT:-$_JL_HERE/../out}/android}
export JL_AVD=${JL_AVD:-jarvis-android}
export EMU_PORT=${EMU_PORT:-5600}      # console port; adb serial emulator-5600
export EMU_GRPC=${EMU_GRPC:-8600}      # gRPC (audio inject/capture)
export ANDROID_SERIAL=emulator-$EMU_PORT

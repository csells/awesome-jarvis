// speech-check: does SFSpeechRecognizer support on-device en-US recognition in this VM?
import Speech
let r = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))
print("auth:", SFSpeechRecognizer.authorizationStatus().rawValue, "(3=authorized)")
print("recognizer available:", r?.isAvailable ?? false)
print("supportsOnDeviceRecognition:", r?.supportsOnDeviceRecognition ?? false)

// live-stt <seconds>: on-device SFSpeechRecognizer on the default input (AVAudioEngine), prints partials.
import Speech; import AVFoundation
let secs = Double(CommandLine.arguments.dropFirst().first ?? "12") ?? 12
let rec = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))!
let req = SFSpeechAudioBufferRecognitionRequest(); req.requiresOnDeviceRecognition = true; req.shouldReportPartialResults = true
let eng = AVAudioEngine(); let node = eng.inputNode
if CommandLine.arguments.contains("vp") { try! node.setVoiceProcessingEnabled(true); print("voice processing ON") }
let fmt = node.outputFormat(forBus: 0)
print("input format:", fmt)
node.installTap(onBus: 0, bufferSize: 1024, format: fmt) { b, _ in req.append(b) }
try! eng.start()
let task = rec.recognitionTask(with: req) { r, e in
  if let r { print(r.isFinal ? "FINAL:" : "partial:", r.bestTranscription.formattedString); fflush(stdout) }
  if let e { print("error:", e.localizedDescription); fflush(stdout) }
}
RunLoop.main.run(until: Date().addingTimeInterval(secs)); req.endAudio(); RunLoop.main.run(until: Date().addingTimeInterval(2)); _ = task

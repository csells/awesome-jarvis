#!/usr/bin/env node
// paseo-dictate-wav <file.wav> [ws://127.0.0.1:6767/ws]
// Streams a WAV through the daemon's dictation pipeline (the same
// dictation_stream_* messages the web/mobile client sends) and prints the
// transcript produced by the daemon's local STT (Parakeet via sherpa-onnx).
// No model/LLM login needed.
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { DaemonClient } from "/usr/local/lib/node_modules/@getpaseo/cli/node_modules/@getpaseo/client/dist/daemon-client.js";

const [file, url = "ws://127.0.0.1:6767/ws"] = process.argv.slice(2);
if (!file) { console.error("usage: paseo-dictate-wav <file.wav> [ws-url]"); process.exit(2); }
// normalise to 16 kHz mono s16le raw PCM
const pcm = execFileSync("sox", [file, "-t", "raw", "-r", "16000", "-c", "1", "-b", "16", "-e", "signed-integer", "-"], { maxBuffer: 64 << 20 });
const client = new DaemonClient({ url, clientId: "jarvis-lab-dictation", clientType: "cli", password: process.env.PASEO_PASSWORD });
await client.connect();
const id = `lab-${Date.now()}`;
const format = "audio/pcm;rate=16000;bits=16";
const t0 = Date.now();
await client.startDictationStream(id, format);
const CHUNK = 3200; // 100 ms
let seq = 0;
for (let off = 0; off < pcm.length; off += CHUNK, seq++) {
  client.sendDictationStreamChunk(id, seq, pcm.subarray(off, off + CHUNK).toString("base64"), format);
  await new Promise((r) => setTimeout(r, 100)); // real-time pacing
}
const result = await client.finishDictationStream(id, seq - 1);
console.log(JSON.stringify({ transcript: result.text, audioSeconds: pcm.length / 32000, elapsedMs: Date.now() - t0 }));
await client.close?.();
process.exit(0);

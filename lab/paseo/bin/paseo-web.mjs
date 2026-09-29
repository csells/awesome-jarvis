#!/usr/bin/env node
// paseo-web.mjs <command> [...]  — drive the Paseo web client in Chromium on
// the lab's Xvfb display (headed, so it uses PulseAudio: mic = vmic, output =
// speaker; `record-out` hears the voice agent).
//   shot <out.png> [path]           screenshot of the web UI (default "/")
//   buttons [path]                  list accessible buttons (for exploring)
//   dictate <out-prefix> [wav]      open a composer, Start dictation, feed
//                                   speech (vmic via `say`, or a WAV through
//                                   Chromium's fake capture device), stop,
//                                   print composer text + screenshots
// Env: PASEO_URL (default http://127.0.0.1:6767), SAY_TEXT, HEADLESS=1 (uses
// --use-file-for-fake-audio-capture only).
import { chromium } from "/usr/local/lib/node_modules/playwright/index.mjs";
import { execFileSync, spawn } from "node:child_process";

const base = process.env.PASEO_URL || "http://127.0.0.1:6767";
const [cmd, a1, a2] = process.argv.slice(2);
const wav = cmd === "dictate" ? a2 : undefined;
const args = ["--use-fake-ui-for-media-stream", "--autoplay-policy=no-user-gesture-required", "--no-sandbox"];
if (wav) args.push("--use-fake-device-for-media-stream", `--use-file-for-fake-audio-capture=${wav}%noloop`);
const browser = await chromium.launch({ headless: process.env.HEADLESS === "1", args, ignoreDefaultArgs: ["--mute-audio"] });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, permissions: ["microphone"] });
const page = await ctx.newPage();
page.on("console", (m) => { if (process.env.DEBUG) console.error("[console]", m.type(), m.text()); });
const go = async (p = "/") => { await page.goto(base + p, { waitUntil: "networkidle" }); await page.waitForTimeout(2500); };

async function listButtons() {
  return page.evaluate(() => [...document.querySelectorAll('button,[role="button"],[aria-label]')]
    .map((e) => e.getAttribute("aria-label") || e.textContent.trim()).filter(Boolean).slice(0, 120));
}

if (cmd === "shot") { await go(a2 || "/"); await page.screenshot({ path: a1 }); console.log(a1); }
else if (cmd === "click") { // click "<name>|<name>..." <out.png>
  await go("/");
  for (const n of a1.split("|")) { await page.getByRole("button", { name: n }).first().click(); await page.waitForTimeout(1500); }
  await page.screenshot({ path: a2 }); console.log(JSON.stringify(await listButtons(), null, 1));
}
else if (cmd === "voice") { // voice <out-prefix> [workspace-button-regex]
  // Opens an existing agent's workspace, enables Voice mode, speaks SAY_TEXT
  // into the virtual mic and records what the voice agent says back.
  const out = a1 || "/lab/out/paseo/voice";
  await go("/");
  await page.getByRole("button", { name: new RegExp(a2 || "^master") }).first().click();
  await page.waitForTimeout(2000);
  await page.getByRole("button", { name: "Enable Voice mode" }).first().click();
  await page.waitForTimeout(4000);
  await page.screenshot({ path: `${out}-0-voice-on.png` });
  const rec = spawn("/lab/bin/record-out", [String(process.env.RECORD_SECONDS || 30), `${out}-agent-speech.wav`]);
  await page.waitForTimeout(500);
  execFileSync("/lab/bin/say", [process.env.SAY_TEXT || "start a new codex agent that adds a readme to this project"]);
  await new Promise((r) => rec.on("exit", r));
  await page.screenshot({ path: `${out}-1-after.png` });
  const text = execFileSync("/lab/bin/transcribe", [`${out}-agent-speech.wav`]).toString().trim();
  console.log(JSON.stringify({ agentSaid: text }));
}
else if (cmd === "buttons") { await go(a1 || "/"); console.log(JSON.stringify(await listButtons(), null, 1)); }
else if (cmd === "dictate") {
  const out = a1 || "/lab/out/paseo/dictate";
  await go("/");
  const composer = page.getByRole("textbox", { name: /Message agent/i }).first();
  if (!(await composer.isVisible().catch(() => false))) {
    // open a new-agent/workspace composer if the landing page has none
    for (const name of [/^New workspace/i, /New agent/i]) {
      const b = page.getByRole("button", { name }).first();
      if (await b.isVisible().catch(() => false)) { await b.click(); await page.waitForTimeout(1500); break; }
    }
  }
  await page.screenshot({ path: `${out}-0-composer.png` });
  await page.getByRole("button", { name: "Start dictation" }).first().click();
  await page.waitForTimeout(800);
  if (!wav) execFileSync("/lab/bin/say", [process.env.SAY_TEXT || "create a new agent that fixes the failing tests"]);
  else await page.waitForTimeout(Number(process.env.WAV_SECONDS || 5) * 1000);
  await page.waitForTimeout(1000);
  await page.screenshot({ path: `${out}-1-recording.png` });
  const btns = await listButtons();
  const stop = btns.find((b) => /^Insert transcription$/i.test(b)) || btns.find((b) => /transcri/i.test(b) && !/send/i.test(b));
  if (process.env.DEBUG) console.error(JSON.stringify(btns));
  await page.getByRole("button", { name: stop, exact: true }).first().click({ force: true });
  await page.waitForTimeout(4000);
  await page.screenshot({ path: `${out}-2-transcribed.png` });
  console.log(JSON.stringify({ composer: await composer.inputValue().catch(() => null), stopButton: stop }));
}
await browser.close();

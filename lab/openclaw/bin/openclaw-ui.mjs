#!/usr/bin/env node
// openclaw-ui.mjs <command> ...  — drive the OpenClaw Control UI in the image's
// Playwright Chromium, headed on the lab Xvfb (PulseAudio mic = vmic).
//   shot <out.png> [path]     screenshot (path e.g. "/", "/chat", "/sessions", "/agents")
//   buttons [path]            list accessible buttons / links
//   click "<a>|<b>" <out.png> click buttons/links by accessible name, screenshot
// The lab gateway token is read from /root/.openclaw/lab-gateway-token and passed as #token=.
import { chromium } from "/app/node_modules/playwright-core/index.mjs";
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
const token = (process.env.OPENCLAW_GATEWAY_TOKEN || readFileSync("/root/.openclaw/lab-gateway-token", "utf8")).trim();
const base = process.env.OPENCLAW_URL || "http://127.0.0.1:18789";
const [cmd, a1, a2] = process.argv.slice(2);
const exe = execFileSync("bash", ["-c", "ls /home/node/.cache/ms-playwright/chromium-*/chrome-linux*/chrome | head -1"]).toString().trim();
const browser = await chromium.launch({ executablePath: exe, headless: process.env.HEADLESS === "1",
  args: ["--no-sandbox", "--use-fake-ui-for-media-stream", "--autoplay-policy=no-user-gesture-required"], ignoreDefaultArgs: ["--mute-audio"] });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, permissions: ["microphone"] });
const page = await ctx.newPage();
const go = async (p = "/") => { await page.goto(`${base}${p}#token=${token}`, { waitUntil: "domcontentloaded" }); await page.waitForTimeout(Number(process.env.WAIT_MS || 5000)); };
const names = () => page.evaluate(() => [...document.querySelectorAll('button,a,[role="button"],[role="tab"]')]
  .map((e) => (e.getAttribute("aria-label") || e.textContent || "").trim().replace(/\s+/g, " ")).filter(Boolean).slice(0, 150));
if (cmd === "shot") { await go(a2 || "/"); await page.screenshot({ path: a1 }); console.log(a1); }
else if (cmd === "buttons") { await go(a1 || "/"); console.log(JSON.stringify(await names(), null, 1)); }
else if (cmd === "click") {
  await go("/");
  for (const n of a1.split("|")) {
    const loc = page.getByRole("button", { name: n }).or(page.getByRole("link", { name: n })).or(page.getByRole("tab", { name: n })).first();
    await loc.click(); await page.waitForTimeout(2000);
  }
  await page.screenshot({ path: a2 }); console.log(JSON.stringify(await names()));
}
await browser.close();

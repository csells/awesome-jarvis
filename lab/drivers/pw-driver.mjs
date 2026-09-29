#!/usr/bin/env node
// pw-driver.mjs <base-url> [port]  — long-lived headed Chromium (Xvfb + PulseAudio: mic = vmic,
// output = speaker) controlled over a tiny local HTTP API so a test can speak, wait, and
// screenshot across many steps while the page (and its voice session) stays open.
//   GET /goto?p=/path   /click?name=REGEX[&nth=0]   /clicktext?t=TEXT   /shot?f=/lab/out/x.png
//   /buttons   /text   /fill?sel=CSS&v=TEXT   /press?k=Enter   /url   /quit
import { createRequire } from "node:module";
import http from "node:http";
const require = createRequire(import.meta.url);
const pwPath = process.env.PW_MODULE || "/usr/local/lib/node_modules/playwright/index.mjs";
const { chromium } = await import(pwPath);
const base = process.argv[2] || "http://127.0.0.1:6767";
const port = Number(process.argv[3] || 7788);
const args = ["--use-fake-ui-for-media-stream", "--autoplay-policy=no-user-gesture-required", "--no-sandbox"];
const browser = await chromium.launch({ headless: process.env.HEADLESS === "1", args, ignoreDefaultArgs: ["--mute-audio"],
  executablePath: process.env.CHROME || undefined });
const ctx = await browser.newContext({ viewport: { width: 1400, height: 900 }, permissions: ["microphone"],
  ignoreHTTPSErrors: true });
const page = await ctx.newPage();
const logs = [];
page.on("console", (m) => { logs.push(`[${m.type()}] ${m.text()}`); if (logs.length > 500) logs.shift(); });
await page.goto(base, { waitUntil: "domcontentloaded" }).catch(() => {});
const ok = (res, v) => { res.writeHead(200, { "content-type": "application/json" }); res.end(JSON.stringify(v ?? { ok: true }, null, 1)); };
http.createServer(async (req, res) => {
  const u = new URL(req.url, "http://x"); const q = Object.fromEntries(u.searchParams);
  try {
    switch (u.pathname) {
      case "/goto": await page.goto(base + (q.p || "/"), { waitUntil: "domcontentloaded" }); await page.waitForTimeout(Number(q.w || 2500)); return ok(res, { url: page.url() });
      case "/click": await page.getByRole(q.role || "button", { name: new RegExp(q.name, "i") }).nth(Number(q.nth || 0)).click({ timeout: 8000, force: q.force === "1" }); await page.waitForTimeout(Number(q.w || 1500)); return ok(res);
      case "/clicktext": await page.getByText(q.t, { exact: q.exact === "1" }).nth(Number(q.nth || 0)).click({ timeout: 8000 }); await page.waitForTimeout(Number(q.w || 1500)); return ok(res);
      case "/clicksel": await page.locator(q.sel).nth(Number(q.nth || 0)).click({ timeout: 8000, force: q.force === "1" }); await page.waitForTimeout(Number(q.w || 1500)); return ok(res);
      case "/fill": await page.locator(q.sel).first().fill(q.v); return ok(res);
      case "/type": await page.keyboard.type(q.v, { delay: 10 }); return ok(res);
      case "/press": await page.keyboard.press(q.k); await page.waitForTimeout(Number(q.w || 800)); return ok(res);
      case "/shot": await page.screenshot({ path: q.f, fullPage: q.full === "1" }); return ok(res, { f: q.f });
      case "/buttons": return ok(res, await page.evaluate(() => [...document.querySelectorAll('button,[role="button"],a,[aria-label],[role="tab"],[role="treeitem"]')].map((e) => (e.getAttribute("aria-label") || e.textContent.trim()).slice(0, 80)).filter(Boolean).slice(0, 250)));
      case "/text": return ok(res, { text: await page.evaluate(() => document.body.innerText) });
      case "/html": return ok(res, { html: (await page.content()).slice(0, Number(q.n || 200000)) });
      case "/url": return ok(res, { url: page.url() });
      case "/logs": return ok(res, logs.slice(-Number(q.n || 50)));
      case "/eval": return ok(res, { v: await page.evaluate(q.js) });
      case "/quit": ok(res); await browser.close(); process.exit(0);
      default: res.writeHead(404); res.end();
    }
  } catch (e) { res.writeHead(500); res.end(String(e && e.message || e)); }
}).listen(port, "127.0.0.1", () => console.log(`pw-driver on :${port} -> ${base}`));

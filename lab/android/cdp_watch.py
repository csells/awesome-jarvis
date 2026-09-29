#!/usr/bin/env python3
"""cdp_watch.py <target-id> <seconds> [js-to-run-after-enable]: log console + network (URL, status) of a Chrome tab."""
import json, sys, time, urllib.request, websocket
tid, secs = sys.argv[1], float(sys.argv[2]); js = sys.argv[3] if len(sys.argv) > 3 else None
t = [x for x in json.load(urllib.request.urlopen("http://localhost:9333/json")) if x["id"] == tid][0]
ws = websocket.create_connection(t["webSocketDebuggerUrl"], timeout=5, suppress_origin=True)
i = 0
voice_ids = []; body_req = {}
def send(m, p=None):
    global i; i += 1; ws.send(json.dumps({"id": i, "method": m, "params": p or {}}))
send("Network.enable"); send("Runtime.enable"); send("Log.enable")
if js: send("Runtime.evaluate", {"expression": js})
end = time.time() + secs
while time.time() < end:
    try: m = json.loads(ws.recv())
    except Exception: continue
    meth = m.get("method", "")
    p = m.get("params", {})
    if meth == "Network.responseReceived":
        u = p["response"]["url"]
        if "posthog" not in u and "/messages" not in u: print("NET", p["response"]["status"], u[:140], flush=True)
        if "voice/conversations" in u: voice_ids.append(p["requestId"])
    elif meth == "Network.loadingFinished" and p.get("requestId") in voice_ids:
        send("Network.getResponseBody", {"requestId": p["requestId"]}); body_req[i] = p["requestId"]
    elif m.get("id") in body_req and "result" in m:
        try:
            b = json.loads(m["result"].get("body") or "{}")
            print("VOICE-GATE", json.dumps({k: b.get(k) for k in ("allowed", "reason", "usedSeconds", "limitSeconds")}), flush=True)
        except Exception as e: print("VOICE-GATE unparsed", e, flush=True)
    elif meth == "Network.loadingFailed": print("NETFAIL", p.get("errorText"), flush=True)
    elif meth == "Network.webSocketCreated": print("WS", p["url"][:140], flush=True)
    elif meth == "Runtime.consoleAPICalled":
        s = " ".join(str(a.get("value", a.get("description", "")))[:200] for a in p.get("args", []))
        if any(k in s.lower() for k in ("voice", "eleven", "livekit", "paywall", "realtime", "error", "microphone")): print("CONSOLE", p["type"], s[:300], flush=True)
    elif meth == "Runtime.exceptionThrown": print("EXC", p["exceptionDetails"].get("text"), str(p["exceptionDetails"].get("exception", {}).get("description", ""))[:200], flush=True)

#!/usr/bin/env python3
"""Drive Chrome on the emulator over DevTools (adb forward tcp:9333 localabstract:chrome_devtools_remote).
  cdp.py eval '<js>' [--url-sub session]   evaluate JS in the first page whose URL contains url-sub; prints the result
  cdp.py text [--url-sub ...]              print document.body.innerText
"""
import json, sys, argparse, urllib.request, websocket

def target(sub):
    ts = json.load(urllib.request.urlopen("http://localhost:9333/json", timeout=20))
    for t in ts:  # --url-sub id:N selects by target id; otherwise first page whose URL contains sub
        if t["type"] == "page" and ((sub.startswith("id:") and t["id"] == sub[3:]) or sub in t["url"]):
            return t
    sys.exit("no page matching " + sub)

def ev(t, js):
    ws = websocket.create_connection(t["webSocketDebuggerUrl"], timeout=120, suppress_origin=True)
    ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "awaitPromise": True, "returnByValue": True}}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == 1:
            ws.close()
            r = m.get("result", {}).get("result", {})
            return r.get("value", r.get("description"))

ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("js", nargs="?"); ap.add_argument("--url-sub", default="happy.engineering")
o = ap.parse_args(); t = target(o.url_sub)
print(ev(t, o.js if o.cmd == "eval" else "document.body.innerText"))

#!/usr/bin/env python3
"""Tiny adb UI driver for the lab's Android emulator.

  ui.py dump                      list visible nodes: text / content-desc / resource-id / bounds
  ui.py tap "Text"  [--n 0]       tap the node whose text or content-desc contains Text (case-insensitive)
  ui.py wait "Text" [--t 30]      wait until such a node exists
  ui.py type "text" [--chunk 1]  type slowly into the focused field
  ui.py shot out.png              full-res screenshot (+ out.small.png, 540 px wide, for quick viewing)
"""
import os, re, subprocess, sys, time, argparse, xml.etree.ElementTree as ET

SER = os.environ.get("ANDROID_SERIAL", "emulator-5600")


def adb(*a, **kw):
    kw.setdefault("timeout", 40)
    return subprocess.run(["adb", "-s", SER, *a], capture_output=True, **kw)


def nodes():
    waited = False
    for _ in range(6):
        try:
            r = adb("exec-out", "uiautomator", "dump", "/dev/tty", timeout=45)
        except subprocess.TimeoutExpired:
            adb("shell", "pkill", "-f", "uiautomator"); time.sleep(2); continue
        s = r.stdout.decode("utf-8", "replace")
        i, j = s.find("<?xml"), s.rfind("</hierarchy>")
        if i >= 0 and j > 0:
            root = ET.fromstring(s[i:j + len("</hierarchy>")])
            out = []
            for n in root.iter("node"):
                b = [int(x) for x in re.findall(r"\d+", n.get("bounds", "[0,0][0,0]"))]
                out.append(dict(text=n.get("text", ""), desc=n.get("content-desc", ""), rid=n.get("resource-id", ""),
                                cls=n.get("class", ""), click=n.get("clickable") == "true", b=b, pkg=n.get("package", ""),
                                checked=n.get("checked")))
            anr = [x for x in out if "isn't responding" in x["text"]]
            wait = [x for x in out if x["text"] == "Wait"]
            if anr and wait and not waited:  # slow emulator: answer "Wait" once on ANR dialogs, never kill the app
                waited = True
                print("(ANR dialog: " + anr[0]["text"] + " -> Wait)", file=sys.stderr)
                tap_node(wait[0]); time.sleep(1); continue
            return out
        time.sleep(1)
    raise SystemExit("uiautomator dump failed")


def find(q, n=0):
    ql = q.lower()
    ns = nodes()
    exact = [x for x in ns if ql in (x["text"].lower(), x["desc"].lower())]
    hits = exact + [x for x in ns if x not in exact and (ql in x["text"].lower() or ql in x["desc"].lower())]
    return hits[n] if len(hits) > n else None


def tap_node(x):
    b = x["b"]
    adb("shell", "input", "tap", str((b[0] + b[2]) // 2), str((b[1] + b[3]) // 2))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="c", required=True)
    sp.add_parser("dump")
    a = sp.add_parser("tap"); a.add_argument("q"); a.add_argument("--n", type=int, default=0)
    a = sp.add_parser("wait"); a.add_argument("q"); a.add_argument("--t", type=float, default=30)
    a = sp.add_parser("shot"); a.add_argument("out")
    a = sp.add_parser("type"); a.add_argument("text"); a.add_argument("--chunk", type=int, default=1)
    o = ap.parse_args()
    if o.c == "dump":
        for x in nodes():
            if x["text"] or x["desc"] or x["click"]:
                print(f'{x["b"]} {"C" if x["click"] else " "} {x["checked"] if x["checked"]=="true" else ""} '
                      f'text={x["text"]!r} desc={x["desc"]!r} id={x["rid"].split("/")[-1]} {x["cls"].split(".")[-1]}')
    elif o.c == "tap":
        x = find(o.q, o.n)
        if not x:
            sys.exit(f"not found: {o.q}")
        tap_node(x); print("tapped", x["text"] or x["desc"], x["b"])
    elif o.c == "wait":
        end = time.time() + o.t
        while time.time() < end:
            if find(o.q):
                print("found", o.q); return
            time.sleep(1)
        sys.exit(f"timeout: {o.q}")
    elif o.c == "type":  # Compose fields drop fast input on this slow emulator: type in small chunks
        t = o.text
        for i in range(0, len(t), o.chunk):
            part = t[i:i + o.chunk].replace(" ", "%s")
            for ch in "\\'\"()&;<>|$`*?#~":
                part = part.replace(ch, "\\" + ch)
            adb("shell", "input", "text", part); time.sleep(0.6)
        print("typed", len(t), "chars")
    elif o.c == "shot":
        with open(o.out, "wb") as f:
            f.write(adb("exec-out", "screencap", "-p").stdout)
        small = o.out[:-4] + ".small.png"
        subprocess.run(["sips", "-Z", "1000", o.out, "--out", small], capture_output=True)
        print(o.out)


if __name__ == "__main__":
    main()

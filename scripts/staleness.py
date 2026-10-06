#!/usr/bin/env python3
"""Weekly staleness report for awesome-jarvis.

Runs four checks and prints a Markdown report:

1. Dead links in README.md, blueprint.md, history.md, testing.md and methodology.md.
2. Health of every GitHub repository linked from README.md (archived, moved, stale).
3. The re-test queue for scorecard agents (data/scorecard.json).
4. Watch List review (promote and drop candidates).

With --publish it also keeps one GitHub issue labelled "staleness" in sync with the
report. Without it, nothing is written anywhere. GitHub is reached only through the
`gh` CLI, so the script works with a local `gh auth login` and with GH_TOKEN in CI.

Python 3.12+ standard library only. Exit status is non-zero only when the script
itself fails, never because it found something.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import http.client
import http.cookiejar
import json
import os
import re
import socket
import ssl
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK_FILES = ["README.md", "blueprint.md", "history.md", "testing.md", "methodology.md"]
MAIN_FILE = "README.md"

# The list's rules (contributing.md and methodology.md).
STRICT_SECTIONS = {"Jarvis Agents", "Mission Control", "Watch List"}
STRICT_STALE_DAYS = 183  # about 6 months
LENIENT_STALE_DAYS = 365  # 12 months
RETEST_DAYS = 90
WATCH_SECTION = "Watch List"
WATCH_ACTIVE_DAYS = 90
WATCH_MIN_CONTRIBUTORS = 2
WATCH_MIN_COMMITS_EACH = 3
WATCH_MIN_AGE_DAYS = 90  # about 3 months of history
WATCH_DROP_DAYS = 183

HTTP_TIMEOUT = 20
HTTP_WORKERS = 8
HTTP_PER_HOST = 2
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)
GRAPHQL_BATCH = 25
ISSUE_LABEL = "staleness"
ISSUE_TITLE = "Staleness report"
ISSUE_BODY_LIMIT = 60000
CHECKS = ("links", "repos", "retest", "watch")
CHECK_TITLES = {
    "links": "Dead links",
    "repos": "Repository health",
    "retest": "Re-test queue",
    "watch": "Watch List review",
}
SCORE_SYMBOLS = {"●": "full", "◐": "partial", "○": "none"}
HALLMARK_COLUMNS = {"Voice": "voice", "Hands-free": "handsFree", "Visual": "visual", "Oversight": "oversight"}
TESTED_LEVELS = {"hands-on", "partial", "code", "docs"}

# First path segments on github.com that are not repository owners.
GITHUB_RESERVED = {
    "about", "apps", "collections", "customer-stories", "enterprise", "events", "explore",
    "features", "login", "marketplace", "new", "notifications", "orgs", "organizations",
    "pricing", "security", "settings", "site", "sponsors", "topics", "trending", "users",
}
# Enough of the public suffix list for the domains this list links to.
MULTI_LABEL_SUFFIXES = {
    "co.uk", "org.uk", "ac.uk", "gov.uk", "com.au", "net.au", "org.au", "co.jp", "ne.jp",
    "or.jp", "com.br", "com.cn", "com.tw", "co.kr", "co.nz", "co.in", "com.sg", "com.hk",
    "github.io", "gitlab.io", "pages.dev", "vercel.app", "netlify.app", "herokuapp.com",
}


# --------------------------------------------------------------------------- model


@dataclass(frozen=True)
class Finding:
    check: str  # one of CHECKS
    key: str  # stable identity used for the fingerprint; no dates or counts
    name: str
    section: str
    url: str
    problem: str
    action: str


@dataclass
class Location:
    file: str
    line: int
    name: str  # entry name, or the nearest heading for links outside list entries
    section: str


@dataclass
class Entry:
    name: str
    url: str
    section: str  # H2 heading
    subsection: str | None  # H3 heading
    line: int
    urls: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.section} › {self.subsection}" if self.subsection else self.section


@dataclass
class Report:
    today: dt.date
    findings: list[Finding] = field(default_factory=list)
    notes: dict[str, list[str]] = field(default_factory=dict)  # check -> informational lines
    ran: list[str] = field(default_factory=list)
    ignored: list[tuple[Finding, str]] = field(default_factory=list)  # (finding, why it is ignored)

    def note(self, check: str, line: str) -> None:
        self.notes.setdefault(check, []).append(line)


class ScriptError(RuntimeError):
    """A failure of the script itself (as opposed to a finding)."""


# --------------------------------------------------------------------------- parsing


def extract_urls(text: str) -> list[str]:
    """Return http(s) URLs in text, keeping balanced parentheses (Her_(2013_film))."""
    urls: list[str] = []
    last_end = 0
    for m in re.finditer(r"https?://", text):
        if m.start() < last_end:  # e.g. the target inside a web.archive.org URL
            continue
        i, depth = m.end(), 0
        while i < len(text):
            c = text[i]
            if c.isspace() or c in "<>\"'`[]{}|\\^":
                break
            if c == "(":
                depth += 1
            elif c == ")":
                if depth == 0:
                    break
                depth -= 1
            i += 1
        last_end = i
        url = text[m.start():i]
        # A URL inside [text](url), <url> or href="url" ends at its delimiter, so a trailing
        # period is part of it (wiki/J.A.R.V.I.S.). Bare URLs lose trailing punctuation.
        if not text[:m.start()].endswith(("](", "<", '="')):
            url = url.rstrip(".,;:!?*_")
        if len(url) > len(m.group(0)):
            urls.append(url)
    return urls


def _markdown_lines(text: str):
    """Yield (line_number, line, h2, h3) outside fenced code blocks and HTML comments."""
    h2 = h3 = None
    in_fence = in_comment = False
    for n, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if stripped.startswith("<!--"):
            in_comment = "-->" not in stripped
            continue
        if line.startswith("## "):
            h2, h3 = line[3:].strip(), None
        elif line.startswith("### "):
            h3 = line[4:].strip()
        yield n, line, h2, h3


ENTRY_RE = re.compile(r"^\s*[-*] \[([^\]]+)\]\(")


def parse_entries(text: str) -> list[Entry]:
    """List entries of the form `- [Name](url) - Description.` with their headings."""
    entries = []
    for n, line, h2, h3 in _markdown_lines(text):
        m = ENTRY_RE.match(line)
        if not m or not h2:
            continue
        urls = extract_urls(line)
        if not urls:
            continue
        entries.append(Entry(m.group(1).strip(), urls[0], h2, h3, n, urls))
    return entries


def collect_link_locations(files: dict[str, str]) -> dict[str, list[Location]]:
    """Map every URL in the given files to where it appears."""
    found: dict[str, list[Location]] = {}
    for fname, text in files.items():
        for n, line, h2, h3 in _markdown_lines(text):
            urls = extract_urls(line)
            if not urls:
                continue
            m = ENTRY_RE.match(line)
            section = f"{h2} › {h3}" if h2 and h3 else (h2 or h3 or fname)
            for url in urls:
                name = m.group(1).strip() if m else (link_text(line, url) or h3 or h2 or fname)
                found.setdefault(url, []).append(Location(fname, n, name, section))
    return found


def link_text(line: str, url: str) -> str | None:
    """The text of the Markdown link that points at url, if any ([![alt](img)](url) gives alt)."""
    end = line.find("](" + url)
    if end < 0:
        return None
    depth, i = 0, end - 1
    while i >= 0:
        if line[i] == "]":
            depth += 1
        elif line[i] == "[":
            if depth == 0:
                break
            depth -= 1
        i -= 1
    text = line[i + 1:end]
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return text.strip() or None


def parse_scorecard_table(text: str) -> list[dict]:
    """Parse the Scorecard table in README.md into the data/scorecard.json shape."""
    rows: list[dict] = []
    header: list[str] | None = None
    in_scorecard = False
    for line in text.splitlines():
        if line.startswith("### ") or line.startswith("## "):
            if in_scorecard and rows:
                break
            in_scorecard = line.strip() == "### Scorecard"
            continue
        if not in_scorecard or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        row = dict(zip(header, cells, strict=False))
        rows.append({
            "name": row.get("Agent", ""),
            "platform": row.get("Platform", ""),
            "scores": {key: SCORE_SYMBOLS.get(row.get(col, ""), row.get(col, ""))
                       for col, key in HALLMARK_COLUMNS.items()},
            "tested": row.get("Tested", "").lower(),
            "watchOut": row.get("Watch out", ""),
        })
    return rows


def github_repo(url: str) -> tuple[str, str] | None:
    """Return (owner, name) for a github.com repository URL, else None."""
    parts = urllib.parse.urlsplit(url)
    if (parts.hostname or "").lower() not in ("github.com", "www.github.com"):
        return None
    segs = [s for s in parts.path.split("/") if s]
    if len(segs) < 2 or segs[0].lower() in GITHUB_RESERVED:
        return None
    name = segs[1][:-4] if segs[1].endswith(".git") else segs[1]
    return segs[0], name


def registrable_domain(host: str) -> str:
    labels = host.lower().rstrip(".").split(".")
    if len(labels) <= 2:
        return ".".join(labels)
    if ".".join(labels[-2:]) in MULTI_LABEL_SUFFIXES:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def load_json(path: Path) -> dict | list:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ScriptError(f"cannot read {path}: {e}") from e


def parse_date(value: str) -> dt.date:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).date()


# --------------------------------------------------------------------------- link check


@dataclass
class Allowlist:
    blocked_statuses: set[int]
    hosts: dict[str, str]  # host -> reason (matches subdomains too)
    urls: dict[str, str]  # URL prefix -> reason

    @classmethod
    def from_json(cls, data: dict) -> "Allowlist":
        return cls(
            set(data.get("blockedStatuses", [403, 429, 999])),
            {e["host"].lower(): e.get("reason", "") for e in data.get("hosts", [])},
            {e["url"]: e.get("reason", "") for e in data.get("urls", [])},
        )

    def match(self, url: str) -> str | None:
        for prefix, reason in self.urls.items():
            if url.startswith(prefix):
                return reason or prefix
        host = (urllib.parse.urlsplit(url).hostname or "").lower()
        for h, reason in self.hosts.items():
            if host == h or host.endswith("." + h):
                return reason or h
        return None


def is_dns_failure(error: object) -> bool:
    if not isinstance(error, socket.gaierror):
        return False
    permanent = {getattr(socket, n) for n in ("EAI_NONAME", "EAI_NODATA") if hasattr(socket, n)}
    return error.errno in permanent


def describe_error(error: object) -> str:
    if isinstance(error, socket.gaierror):
        return f"DNS error ({error.strerror or error})"
    if isinstance(error, (TimeoutError, socket.timeout)):
        return f"no response within {HTTP_TIMEOUT} s"
    if isinstance(error, ssl.SSLError):
        return f"TLS error ({getattr(error, 'reason', None) or error})"
    return f"{type(error).__name__}: {error}"


def classify_link(url: str, status: int | None, final_url: str | None, error: object,
                  allowlist: Allowlist) -> tuple[str, str]:
    """Return (kind, detail). kind: ok, dead, redirect, blocked, transient or skipped.

    dead, redirect and blocked become findings; transient and skipped are notes.
    404/410 and DNS failures are dead even for allow-listed hosts.
    """
    allowed = allowlist.match(url)
    if error is not None:
        if is_dns_failure(error):
            return "dead", "DNS lookup failed (domain gone)"
        return ("skipped" if allowed else "transient"), describe_error(error)
    assert status is not None
    if status in (404, 410):
        return "dead", f"HTTP {status}"
    if 200 <= status < 400:
        if final_url:
            src = urllib.parse.urlsplit(url).hostname or ""
            dst = urllib.parse.urlsplit(final_url).hostname or ""
            if dst and registrable_domain(src) != registrable_domain(dst):
                return ("skipped" if allowed else "redirect"), f"redirects to {final_url}"
        return "ok", ""
    if status >= 500:
        return ("skipped" if allowed else "transient"), f"HTTP {status}"
    return ("skipped" if allowed else "blocked"), f"HTTP {status}"


class _HostGate:
    def __init__(self, per_host: int):
        self._per_host = per_host
        self._lock = threading.Lock()
        self._sems: dict[str, threading.Semaphore] = {}

    def __call__(self, host: str) -> threading.Semaphore:
        with self._lock:
            return self._sems.setdefault(host, threading.Semaphore(self._per_host))


def _ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    if not ctx.get_ca_certs() and Path("/etc/ssl/cert.pem").exists():  # macOS Python builds
        ctx.load_verify_locations("/etc/ssl/cert.pem")
    return ctx


_SSL = None


def fetch(url: str, method: str) -> tuple[int | None, str | None, object]:
    global _SSL
    if _SSL is None:
        _SSL = _ssl_context()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
        urllib.request.HTTPSHandler(context=_SSL),
    )
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with opener.open(req, timeout=HTTP_TIMEOUT) as resp:
            if method == "GET":
                resp.read(2048)
            return resp.status, resp.geturl(), None
    except urllib.error.HTTPError as e:
        return e.code, e.geturl() or url, None
    except urllib.error.URLError as e:
        return None, None, e.reason
    except (OSError, http.client.HTTPException, ValueError) as e:
        return None, None, e


def check_url(url: str, allowlist: Allowlist, gate: _HostGate) -> tuple[str, str]:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    with gate(host):
        status, final, error = fetch(url, "HEAD")
        if error is not None or not (200 <= (status or 0) < 400):
            status, final, error = fetch(url, "GET")
        kind, detail = classify_link(url, status, final, error, allowlist)
        if kind in ("transient", "blocked", "dead") and not (kind == "dead" and error is None):
            time.sleep(2)
            status, final, error = fetch(url, "GET")
            kind, detail = classify_link(url, status, final, error, allowlist)
    return kind, detail


def link_findings(results: dict[str, tuple[str, str]], locations: dict[str, list[Location]],
                  report: Report) -> None:
    actions = {
        "dead": "Replace the link (try the Wayback Machine or the project's new home) or remove the entry.",
        "redirect": "Update the link to the new address if it is the same resource; if the redirect is expected, "
                    "add the URL to data/link-allowlist.json.",
        "blocked": "Open it in a browser. If it loads, add the host to data/link-allowlist.json; "
                   "otherwise fix the link.",
    }
    skipped, transient = [], []
    for url in sorted(results):
        kind, detail = results[url]
        first = locations[url][0]
        where = ", ".join(f"{loc.file}:{loc.line}" for loc in locations[url])
        if kind in actions:
            report.findings.append(Finding(
                "links", f"link:{kind}:{url}", first.name, first.section, url,
                f"{detail} ({where}).", actions[kind]))
        elif kind == "skipped":
            skipped.append(f"{url} ({detail})")
        elif kind == "transient":
            transient.append(f"{url}: {detail} ({where})")
    ok = sum(1 for k, _ in results.values() if k == "ok")
    report.note("links", f"Checked {len(results)} URLs over HTTP: {ok} fine, {len(skipped)} skipped as "
                         f"unverifiable (data/link-allowlist.json), {len(transient)} could not be reached this time.")
    for line in transient:
        report.note("links", f"Could not reach (not flagged; retried next week): {line}")
    for line in skipped:
        report.note("links", f"Skipped: {line}")


# --------------------------------------------------------------------------- GitHub via gh


def gh(args: list[str], stdin: str | None = None, ok_codes: tuple[int, ...] = (0,)) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(["gh", *args], input=stdin, capture_output=True, text=True, timeout=120)
    except FileNotFoundError as e:
        raise ScriptError("the GitHub CLI (gh) is not installed") from e
    except subprocess.TimeoutExpired as e:
        raise ScriptError(f"gh {' '.join(args[:2])} timed out") from e
    if proc.returncode not in ok_codes:
        raise ScriptError(f"gh {' '.join(args[:3])} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return proc.returncode, proc.stdout, proc.stderr


def graphql(query: str) -> dict:
    """Run a GraphQL query; NOT_FOUND errors are allowed (their data is null)."""
    _, out, err = gh(["api", "graphql", "-f", f"query={query}"], ok_codes=(0, 1))
    try:
        resp = json.loads(out)
    except json.JSONDecodeError as e:
        raise ScriptError(f"GraphQL call failed: {err.strip() or out[:200]}") from e
    errors = [e for e in resp.get("errors", []) if e.get("type") != "NOT_FOUND"]
    if errors or "data" not in resp:
        raise ScriptError(f"GraphQL error: {errors or resp}")
    return resp["data"]


BASE_FIELDS = "nameWithOwner url isArchived createdAt pushedAt"
HISTORY_FIELDS = ("recent: history(since: {since}, first: 100{after}) {{ pageInfo {{ hasNextPage endCursor }} "
                  "nodes {{ author {{ email name user {{ login }} }} }} }}")
RELEASE_FIELDS = (
    "releases(first: 30, orderBy: {field: CREATED_AT, direction: DESC}) "
    "{ nodes { tagName publishedAt isDraft isPrerelease } } "
    "tags: refs(refPrefix: \"refs/tags/\", first: 30, orderBy: {field: TAG_COMMIT_DATE, direction: DESC}) "
    "{ nodes { name target { __typename ... on Commit { committedDate } ... on Tag { tagger { date } } } } }"
)


def _repo_fields(history_since: str | None, releases: bool, after: str | None = None) -> str:
    commit = "committedDate"
    if history_since:
        commit += " " + HISTORY_FIELDS.format(
            since=json.dumps(history_since), after=f", after: {json.dumps(after)}" if after else "")
    fields = f"{BASE_FIELDS} defaultBranchRef {{ name target {{ ... on Commit {{ {commit} }} }} }}"
    if releases:
        fields += " " + RELEASE_FIELDS
    return fields


def fetch_repos(repos: dict[str, dict], today: dt.date) -> dict[str, dict | None]:
    """repos maps "owner/name" (as linked) to {"history": bool, "releases": bool}."""
    since = (dt.datetime.combine(today, dt.time()) - dt.timedelta(days=WATCH_ACTIVE_DAYS)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    keys = sorted(repos)
    out: dict[str, dict | None] = {}
    for start in range(0, len(keys), GRAPHQL_BATCH):
        batch = keys[start:start + GRAPHQL_BATCH]
        parts = []
        for i, key in enumerate(batch):
            owner, name = key.split("/", 1)
            opts = repos[key]
            parts.append(f"r{i}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) "
                         f"{{ {_repo_fields(since if opts.get('history') else None, opts.get('releases', False))} }}")
        data = graphql("query { " + " ".join(parts) + " }")
        for i, key in enumerate(batch):
            out[key] = data.get(f"r{i}")
    # Page through recent history where one page wasn't enough to find two regular authors.
    for key, repo in out.items():
        if not repo or not repos[key].get("history"):
            continue
        hist = ((repo.get("defaultBranchRef") or {}).get("target") or {}).get("recent")
        pages = 0
        while (hist and hist["pageInfo"]["hasNextPage"] and pages < 10
               and len(regular_authors(hist["nodes"])) < WATCH_MIN_CONTRIBUTORS):
            owner, name = repo["nameWithOwner"].split("/", 1)
            q = (f"query {{ repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) "
                 f"{{ {_repo_fields(since, False, hist['pageInfo']['endCursor'])} }} }}")
            more = graphql(q)["repository"]["defaultBranchRef"]["target"]["recent"]
            hist["nodes"].extend(more["nodes"])
            hist["pageInfo"] = more["pageInfo"]
            pages += 1
    return out


def recent_authors(nodes: list[dict]) -> dict[str, int]:
    """Commit counts by author (GitHub login, else name, else email), ignoring bots."""
    authors: dict[str, int] = {}
    for node in nodes:
        a = node.get("author") or {}
        login = ((a.get("user") or {}).get("login") or "").lower()
        email = (a.get("email") or "").lower()
        name = (a.get("name") or "").lower()
        if login.endswith("[bot]") or name.endswith("[bot]") or "[bot]@" in email:
            continue
        ident = login or (a.get("name") or "").strip() or email
        if ident:
            authors[ident] = authors.get(ident, 0) + 1
    return authors


def regular_authors(nodes: list[dict]) -> dict[str, int]:
    """Authors with at least WATCH_MIN_COMMITS_EACH commits, so one drive-by commit doesn't count."""
    return {a: n for a, n in recent_authors(nodes).items() if n >= WATCH_MIN_COMMITS_EACH}


def last_commit(repo: dict) -> dt.date | None:
    target = (repo.get("defaultBranchRef") or {}).get("target") or {}
    return parse_date(target["committedDate"]) if target.get("committedDate") else None


# --------------------------------------------------------------------------- repo health


def repo_findings(entries: list[Entry], repos: dict[str, dict | None], today: dt.date,
                  report: Report) -> None:
    seen = set()
    for entry in entries:
        for url in entry.urls:
            ref = github_repo(url)
            if not ref:
                continue
            key = f"{ref[0]}/{ref[1]}"
            if key.lower() in seen:
                continue
            seen.add(key.lower())
            repo = repos.get(key)

            def add(kind: str, problem: str, action: str, entry=entry, url=url, key=key) -> None:
                report.findings.append(Finding(
                    "repos", f"repo:{kind}:{key.lower()}", entry.name, entry.label, url, problem, action))

            if repo is None:
                add("missing", "Repository not found (deleted, renamed away or made private) "
                               f"(README.md:{entry.line}).",
                    "Find the project's new home or remove the entry (retired projects go in history.md).")
                continue
            if repo["nameWithOwner"].lower() != key.lower():
                add("moved", f"Repository moved to {repo['nameWithOwner']} (README.md:{entry.line}).",
                    f"Update the link to {repo['url']}.")
            if repo.get("isArchived"):
                add("archived", f"Repository is archived (README.md:{entry.line}).",
                    "Remove the entry or move it to history.md.")
                continue
            if entry.section == WATCH_SECTION:
                continue  # staleness of Watch List entries is reported as a drop candidate
            last = last_commit(repo)
            limit = STRICT_STALE_DAYS if entry.section in STRICT_SECTIONS else LENIENT_STALE_DAYS
            if last and (today - last).days > limit:
                months = "6 months" if limit == STRICT_STALE_DAYS else "12 months"
                add("stale", f"Last commit on the default branch was {last} ({(today - last).days} days ago); "
                             f"the limit for {entry.section} is {months} (README.md:{entry.line}).",
                    "Check whether it is still maintained; if not, move it to history.md or drop it.")


def other_file_repo_findings(locations: dict[str, list[Location]], repos: dict[str, dict | None],
                             readme_repos: set[str], report: Report) -> None:
    """Existence and rename checks for GitHub repos linked only outside README.md."""
    for url, locs in sorted(locations.items()):
        ref = github_repo(url)
        if not ref:
            continue
        key = f"{ref[0]}/{ref[1]}"
        if key.lower() in readme_repos:
            continue
        repo = repos.get(key)
        where = ", ".join(f"{loc.file}:{loc.line}" for loc in locs)
        if repo is None:
            report.findings.append(Finding(
                "links", f"link:dead:{url}", locs[0].name, locs[0].section, url,
                f"GitHub repository not found ({where}).",
                "Replace the link (try the Wayback Machine or the project's new home) or remove it."))
        elif repo["nameWithOwner"].lower() != key.lower():
            report.findings.append(Finding(
                "links", f"link:moved:{url}", locs[0].name, locs[0].section, url,
                f"Repository moved to {repo['nameWithOwner']} ({where}).", f"Update the link to {repo['url']}."))


# --------------------------------------------------------------------------- re-test queue

VERSION_RE = re.compile(r"(\d+)\.(\d+)(?:\.(\d+))?")
COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")
# Pre-release markers such as 1.2.5-beta.2, rc.14-v0.21.5 or v0.21.4+canary.20260928.
PRERELEASE_RE = re.compile(r"(?:^|[^a-z])(alpha|beta|rc|pre|preview|canary|nightly|dev)(?:[^a-z]|$)", re.I)


def parse_version(text: str | None) -> tuple[int, int, int] | None:
    if not text or COMMIT_RE.match(text):
        return None
    m = VERSION_RE.search(text)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)) if m else None


def release_candidates(repo: dict, tag_pattern: str | None) -> list[dict]:
    """Stable versioned releases (or tags when there are no releases): {tag, version, date}.

    Pre-releases are skipped: GitHub's prerelease flag, and pre-release suffixes in the tag name.
    """
    pattern = re.compile(tag_pattern) if tag_pattern else None
    out = []
    for r in (repo.get("releases") or {}).get("nodes", []):
        if r.get("isDraft") or r.get("isPrerelease") or not r.get("publishedAt"):
            continue
        if PRERELEASE_RE.search(r["tagName"]):
            continue
        if pattern and not pattern.search(r["tagName"]):
            continue
        v = parse_version(r["tagName"])
        if v:
            out.append({"tag": r["tagName"], "version": v, "date": parse_date(r["publishedAt"])})
    if out:
        return out
    for t in (repo.get("tags") or {}).get("nodes", []):
        if pattern and not pattern.search(t["name"]):
            continue
        if PRERELEASE_RE.search(t["name"]):
            continue
        v = parse_version(t["name"])
        target = t.get("target") or {}
        when = target.get("committedDate") or (target.get("tagger") or {}).get("date")
        if v and when:
            out.append({"tag": t["name"], "version": v, "date": parse_date(when)})
    return out


def _newest(candidates: list[dict]) -> dict | None:
    if not candidates:
        return None
    return max(candidates, key=lambda c: (c["version"], c["date"]))


def retest_findings(agent: dict, repo: dict | None, today: dt.date) -> list[Finding]:
    name, url = agent["name"], agent["url"]
    section = agent.get("section", "Jarvis Agents")
    tested_at = dt.date.fromisoformat(agent["testedAt"])
    level = agent["tested"]
    redo = ("Re-run the hands-on tests (methodology.md) and update the scorecard, testing.md and data/scorecard.json."
            if level in ("hands-on", "partial") else
            "Re-review it at the current version and update the scorecard and data/scorecard.json.")
    out = []
    age = (today - tested_at).days
    if age > RETEST_DAYS:
        out.append(Finding("retest", f"retest:age:{name}", name, section, url,
                           f"Last tested ({level}) on {tested_at}, {age} days ago; scores are re-checked quarterly.",
                           redo))
    if repo:
        candidates = release_candidates(repo, agent.get("tagPattern"))
        latest = _newest(candidates)
        tested = parse_version(agent.get("testedVersion"))
        basis = f"tested `{agent['testedVersion']}`" if tested else None
        if not tested:
            baseline = _newest([c for c in candidates if c["date"] <= tested_at])
            if baseline:
                tested = baseline["version"]
                what = (f"at commit `{agent['testedVersion']}`" if agent.get("testedVersion")
                        else "with no version recorded")
                basis = f"`{baseline['tag']}`, the newest release when it was tested {what} on {tested_at}"
        if latest and tested and latest["version"][:2] > tested[:2]:
            bump = "major" if latest["version"][0] > tested[0] else "minor"
            out.append(Finding("retest", f"retest:release:{name}", name, section, url,
                               f"Latest release `{latest['tag']}` ({latest['date']}) is a {bump} bump over {basis}.",
                               redo))
        elif latest and not tested and latest["date"] > tested_at:
            out.append(Finding("retest", f"retest:release:{name}", name, section, url,
                               f"First versioned release `{latest['tag']}` ({latest['date']}) came out after the "
                               f"test on {tested_at}.", redo))
    return out


def scorecard_sync_findings(table: list[dict], agents: list[dict]) -> list[Finding]:
    """Flag drift between the readme scorecard table and data/scorecard.json."""
    out = []
    by_name = {a["name"]: a for a in agents}
    table_names = {r["name"] for r in table}
    for row in table:
        agent = by_name.get(row["name"])
        if agent is None:
            out.append(Finding("retest", f"retest:sync:{row['name']}", row["name"], "Jarvis Agents › Scorecard",
                               "", "In the readme scorecard but missing from data/scorecard.json.",
                               "Add it to data/scorecard.json with its test date and version."))
            continue
        diffs = [f for f in ("platform", "tested", "watchOut") if agent.get(f) != row[f]]
        diffs += [f"scores.{k}" for k in row["scores"] if agent.get("scores", {}).get(k) != row["scores"][k]]
        if diffs:
            out.append(Finding("retest", f"retest:sync:{row['name']}", row["name"], agent.get("section", ""),
                               agent.get("url", ""),
                               f"data/scorecard.json disagrees with the readme on {', '.join(diffs)}.",
                               "Make data/scorecard.json and the readme scorecard agree."))
    for agent in agents:
        if agent["name"] not in table_names:
            out.append(Finding("retest", f"retest:sync:{agent['name']}", agent["name"], agent.get("section", ""),
                               agent.get("url", ""), "In data/scorecard.json but not in the readme scorecard.",
                               "Remove it from data/scorecard.json or add it back to the scorecard."))
    return out


def validate_scorecard(agents: list[dict]) -> None:
    for a in agents:
        for f in ("name", "url", "section", "scores", "tested", "testedAt", "watchOut"):
            if f not in a:
                raise ScriptError(f"data/scorecard.json: {a.get('name', '?')} is missing {f}")
        if a["tested"] not in TESTED_LEVELS:
            raise ScriptError(f"data/scorecard.json: {a['name']} has unknown tested level {a['tested']!r}")
        dt.date.fromisoformat(a["testedAt"])


# --------------------------------------------------------------------------- Watch List


def watch_findings(entry: Entry, repo: dict | None, today: dt.date) -> list[Finding]:
    if not repo or repo.get("isArchived"):
        return []  # missing and archived repos are reported under repository health
    out = []
    url = entry.url
    key = repo["nameWithOwner"].lower()
    last = last_commit(repo)
    if last and (today - last).days > WATCH_DROP_DAYS:
        out.append(Finding("watch", f"watch:drop:{key}", entry.name, entry.label, url,
                           f"Last commit {last} ({(today - last).days} days ago), over six months.",
                           "Drop it from the Watch List (or move it to history.md if it mattered)."))
        return out
    hist = ((repo.get("defaultBranchRef") or {}).get("target") or {}).get("recent") or {"nodes": []}
    authors = recent_authors(hist["nodes"])
    regulars = regular_authors(hist["nodes"])
    age = (today - parse_date(repo["createdAt"])).days
    if len(regulars) >= WATCH_MIN_CONTRIBUTORS and age >= WATCH_MIN_AGE_DAYS:
        counts = ", ".join(f"{a} {n}" for a, n in sorted(authors.items(), key=lambda kv: (-kv[1], kv[0])))
        truncated = hist.get("pageInfo", {}).get("hasNextPage")
        scope = f" (newest {len(hist['nodes'])} commits only)" if truncated else ""
        out.append(Finding("watch", f"watch:promote:{key}", entry.name, entry.label, url,
                           f"{len(regulars)} people made {WATCH_MIN_COMMITS_EACH} or more commits each in the last "
                           f"{WATCH_ACTIVE_DAYS} days (commits: {counts}){scope}, and the repository is "
                           f"{age} days old.",
                           "Review it for promotion: run the methodology.md pipeline and, if it meets the bar, move it "
                           "to Jarvis Agents or Mission Control."))
    return out


# --------------------------------------------------------------------------- report


def fingerprint(keys: set[str]) -> str:
    return "sha256:" + hashlib.sha256("\n".join(sorted(keys)).encode()).hexdigest()[:16]


def hidden_block(keys: set[str]) -> str:
    payload = json.dumps({"keys": sorted(keys)}, ensure_ascii=True).replace("--", "-\\u002d")
    return f"<!-- staleness-fingerprint: {fingerprint(keys)}\n{payload}\n-->"


HIDDEN_RE = re.compile(r"<!-- staleness-fingerprint: (\S+)\n(.*?)\n-->", re.S)


def parse_hidden_block(body: str | None) -> set[str] | None:
    """Finding keys recorded in an earlier report, or None if there is no block."""
    m = HIDDEN_RE.search(body or "")
    if not m:
        return None
    try:
        return set(json.loads(m.group(2))["keys"])
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def _no_mention(text: str) -> str:
    return text.replace("@", "&#64;")


def finding_line(f: Finding) -> str:
    url = f" <{f.url}>" if f.url else ""
    return (f"- [ ] **{_no_mention(f.name)}** ({_no_mention(f.section)}){url}: {_no_mention(f.problem)} "
            f"**Action:** {_no_mention(f.action)}")


def render_report(report: Report) -> str:
    keys = {f.key for f in report.findings}
    n = len(report.findings)
    lines = [
        "# Staleness report",
        "",
        f"Checked {report.today} by `scripts/staleness.py` against the rules in methodology.md (Re-Verification). "
        + (f"**{n} item{'s' if n != 1 else ''} need attention.** " if n else "**Nothing needs attention.** ")
        + (f"({len(report.ignored)} ignored.) " if report.ignored else "")
        + "Each weekly run rewrites this list, so fix items in pull requests and they drop off on the next run.",
    ]
    for check in CHECKS:
        if check not in report.ran:
            continue
        items = sorted((f for f in report.findings if f.check == check), key=lambda f: (f.section, f.name, f.key))
        lines += ["", f"## {CHECK_TITLES[check]} ({len(items)})", ""]
        lines += [finding_line(f) for f in items] or ["None."]
    if report.ignored:
        lines += ["", f"<details><summary>Ignored ({len(report.ignored)}, see data/staleness-ignore.json)</summary>",
                  ""]
        lines += [f"- {finding_line(f).removeprefix('- [ ] ')} **Ignored:** {_no_mention(why)}"
                  for f, why in sorted(report.ignored, key=lambda fw: fw[0].key)]
        lines += ["", "</details>"]
    notes = [(c, line) for c in CHECKS for line in report.notes.get(c, [])]
    if notes:
        lines += ["", "<details><summary>Notes (not flagged)</summary>", ""]
        lines += [f"- {CHECK_TITLES[c]}: {_no_mention(line)}" for c, line in notes]
        lines += ["", "</details>"]
    lines += ["", hidden_block(keys), ""]
    body = "\n".join(lines)
    if len(body) > ISSUE_BODY_LIMIT:  # GitHub caps issue bodies at 65,536 characters
        head = body[:ISSUE_BODY_LIMIT - 2000].rsplit("\n", 1)[0]
        body = f"{head}\n\n…truncated; run the script locally for the full report.\n\n{hidden_block(keys)}\n"
    return body


# --------------------------------------------------------------------------- publishing


@dataclass
class IssueAction:
    kind: str  # create, update, comment, close
    number: int | None = None
    title: str | None = None
    body: str | None = None
    assignee: str | None = None


def plan_publish(issue: dict | None, body: str, findings: list[Finding], owner: str) -> list[IssueAction]:
    """Decide what to do with the tracking issue. Pure, so it can be tested offline."""
    keys = {f.key for f in findings}
    if not keys:
        if issue is None:
            return []
        return [IssueAction("comment", issue["number"], body="All clear: the latest staleness check found nothing. "
                                                             "Closing; a new issue opens if something turns up."),
                IssueAction("close", issue["number"])]
    if issue is None:
        return [IssueAction("create", title=ISSUE_TITLE, body=body, assignee=owner)]
    actions = []
    if (issue.get("body") or "") != body:
        actions.append(IssueAction("update", issue["number"], body=body))
    previous = parse_hidden_block(issue.get("body")) or set()
    new = sorted((f for f in findings if f.key not in previous), key=lambda f: (f.check, f.section, f.name, f.key))
    if new:
        lines = [f"@{owner} {len(new)} new item{'s' if len(new) != 1 else ''} since the last report:", ""]
        lines += [finding_line(f) for f in new]
        actions.append(IssueAction("comment", issue["number"], body="\n".join(lines)))
    return actions


def find_issue(repo: str) -> dict | None:
    _, out, _ = gh(["api", f"repos/{repo}/issues?state=open&labels={ISSUE_LABEL}&per_page=100"])
    issues = [i for i in json.loads(out) if "pull_request" not in i]
    if len(issues) > 1:
        print(f"warning: {len(issues)} open '{ISSUE_LABEL}' issues; using the oldest", file=sys.stderr)
    return min(issues, key=lambda i: i["number"]) if issues else None


def ensure_label(repo: str) -> None:
    code, _, err = gh(["api", f"repos/{repo}/labels/{ISSUE_LABEL}"], ok_codes=(0, 1))
    if code == 0:
        return
    if "404" not in err:
        raise ScriptError(f"cannot read label {ISSUE_LABEL}: {err.strip()}")
    gh(["api", f"repos/{repo}/labels", "--method", "POST", "--input", "-"], stdin=json.dumps({
        "name": ISSUE_LABEL, "color": "c5def5",
        "description": "Weekly report of dead links, stale repos and overdue re-tests"}))


def apply_actions(repo: str, actions: list[IssueAction]) -> None:
    for a in actions:
        if a.kind == "create":
            ensure_label(repo)
            payload = {"title": a.title, "body": a.body, "labels": [ISSUE_LABEL], "assignees": [a.assignee]}
            _, out, _ = gh(["api", f"repos/{repo}/issues", "--method", "POST", "--input", "-"],
                           stdin=json.dumps(payload))
            print(f"created issue #{json.loads(out)['number']}", file=sys.stderr)
        elif a.kind == "update":
            gh(["api", f"repos/{repo}/issues/{a.number}", "--method", "PATCH", "--input", "-"],
               stdin=json.dumps({"body": a.body}))
            print(f"updated issue #{a.number}", file=sys.stderr)
        elif a.kind == "comment":
            gh(["api", f"repos/{repo}/issues/{a.number}/comments", "--method", "POST", "--input", "-"],
               stdin=json.dumps({"body": a.body}))
            print(f"commented on issue #{a.number}", file=sys.stderr)
        elif a.kind == "close":
            gh(["api", f"repos/{repo}/issues/{a.number}", "--method", "PATCH", "--input", "-"],
               stdin=json.dumps({"state": "closed", "state_reason": "completed"}))
            print(f"closed issue #{a.number}", file=sys.stderr)


# --------------------------------------------------------------------------- ignores


def load_ignores(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries = load_json(path).get("ignore", [])
    for e in entries:
        if not e.get("key") or not str(e.get("reason", "")).strip():
            raise ScriptError(f"{path.name}: every entry needs a key and a reason ({e})")
        if e.get("until"):
            try:
                dt.date.fromisoformat(e["until"])
            except ValueError as err:
                raise ScriptError(f"{path.name}: bad until date for {e['key']}: {e['until']}") from err
    return entries


def apply_ignores(report: Report, ignores: list[dict]) -> None:
    """Move ignored findings out of the open list. Expired or unused entries become notes."""
    active: dict[str, dict] = {}
    for e in ignores:
        until = dt.date.fromisoformat(e["until"]) if e.get("until") else None
        if until and until < report.today:
            report.note(_check_of(e["key"]), f"Ignore for {e['key']} expired on {until}; it is reported again. "
                                             "Remove or extend it in data/staleness-ignore.json.")
        else:
            active[e["key"]] = e
    kept, used = [], set()
    for f in report.findings:
        e = active.get(f.key)
        if e:
            used.add(f.key)
            report.ignored.append((f, e["reason"] + (f" (until {e['until']})" if e.get("until") else "")))
        else:
            kept.append(f)
    report.findings = kept
    for key in sorted(set(active) - used):
        if _check_of(key) in report.ran:
            report.note(_check_of(key), f"Ignore for {key} matched nothing; remove it from data/staleness-ignore.json.")


def _check_of(key: str) -> str:
    prefix = key.split(":", 1)[0]
    return {"link": "links", "repo": "repos"}.get(prefix, prefix if prefix in CHECKS else "links")


# --------------------------------------------------------------------------- driver


def run_checks(root: Path, today: dt.date, only: list[str]) -> Report:
    report = Report(today, ran=list(only))
    files = {name: (root / name).read_text(encoding="utf-8") for name in LINK_FILES if (root / name).exists()}
    readme = files.get(MAIN_FILE)
    if readme is None:
        raise ScriptError(f"{root / MAIN_FILE} not found")
    entries = parse_entries(readme)
    locations = collect_link_locations(files)
    agents = load_json(root / "data" / "scorecard.json")["agents"]
    validate_scorecard(agents)

    # One GraphQL pass for every GitHub repository the checks need.
    readme_repos = {f"{r[0]}/{r[1]}" for e in entries for u in e.urls if (r := github_repo(u))}
    wanted: dict[str, dict] = {}
    if "links" in only:
        for url in locations:
            if (r := github_repo(url)):
                wanted.setdefault(f"{r[0]}/{r[1]}", {})
    if "repos" in only:
        for key in readme_repos:
            wanted.setdefault(key, {})
    watch_entries = [e for e in entries if e.section == WATCH_SECTION]
    if "watch" in only:
        for e in watch_entries:
            if (r := github_repo(e.url)):
                wanted.setdefault(f"{r[0]}/{r[1]}", {})["history"] = True
    if "retest" in only:
        for a in agents:
            if a.get("repo"):
                wanted.setdefault(a["repo"], {})["releases"] = True
    print(f"querying {len(wanted)} GitHub repositories", file=sys.stderr)
    repos = fetch_repos(wanted, today) if wanted else {}
    readme_repo_keys = {k.lower() for k in readme_repos}

    if "links" in only:
        other_file_repo_findings(locations, repos, readme_repo_keys if "repos" in only else set(), report)
        http_urls = [u for u in locations if not github_repo(u)]
        allowlist = Allowlist.from_json(load_json(root / "data" / "link-allowlist.json"))
        gate = _HostGate(HTTP_PER_HOST)
        print(f"checking {len(http_urls)} URLs", file=sys.stderr)
        with concurrent.futures.ThreadPoolExecutor(HTTP_WORKERS) as pool:
            results = dict(zip(http_urls, pool.map(lambda u: check_url(u, allowlist, gate), http_urls), strict=True))
        link_findings(results, locations, report)
    if "repos" in only:
        repo_findings(entries, repos, today, report)
    if "retest" in only:
        for a in agents:
            report.findings.extend(retest_findings(a, repos.get(a["repo"]) if a.get("repo") else None, today))
        report.findings.extend(scorecard_sync_findings(parse_scorecard_table(readme), agents))
    if "watch" in only:
        for e in watch_entries:
            r = github_repo(e.url)
            if not r:
                report.note("watch", f"{e.name} is not on GitHub ({e.url}); review it by hand.")
                continue
            report.findings.extend(watch_findings(e, repos.get(f"{r[0]}/{r[1]}"), today))
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--publish", action="store_true",
                        help="create, update or close the 'staleness' issue (default: dry run, print only)")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "csells/awesome-jarvis"),
                        help="repository that holds the issue (default: $GITHUB_REPOSITORY or csells/awesome-jarvis)")
    parser.add_argument("--owner", default=os.environ.get("STALENESS_OWNER", "csells"),
                        help="login to assign and @mention (default: $STALENESS_OWNER or csells)")
    parser.add_argument("--only", default=",".join(CHECKS),
                        help=f"comma-separated checks to run (default: {','.join(CHECKS)})")
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.datetime.now(dt.timezone.utc).date(),
                        help="date to measure ages from, YYYY-MM-DD (default: today, UTC)")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    only = [c.strip() for c in args.only.split(",") if c.strip()]
    if unknown := set(only) - set(CHECKS):
        parser.error(f"unknown checks: {', '.join(sorted(unknown))}")
    if args.publish and set(only) != set(CHECKS):
        parser.error("--publish needs every check, or the issue would lose findings")
    try:
        report = run_checks(args.root, args.today, only)
        apply_ignores(report, load_ignores(args.root / "data" / "staleness-ignore.json"))
        body = render_report(report)
        print(body)
        if args.publish:
            actions = plan_publish(find_issue(args.repo), body, report.findings, args.owner)
            apply_actions(args.repo, actions)
            if not actions:
                print("no issue changes needed", file=sys.stderr)
    except ScriptError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

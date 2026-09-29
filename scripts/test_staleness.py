"""Offline tests for staleness.py. Run with: python3 -m unittest discover -s scripts"""

import datetime as dt
import json
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import staleness as s  # noqa: E402

TODAY = dt.date(2026, 9, 29)
ALLOW = s.Allowlist({403, 429, 999}, {"fandom.com": "bot wall"}, {"https://livekit.io/join-slack": "slack"})


def repo(name="o/r", archived=False, last="2026-09-01T00:00:00Z", created="2026-01-01T00:00:00Z",
         authors=(), releases=(), tags=(), more=False):
    return {
        "nameWithOwner": name, "url": f"https://github.com/{name}", "isArchived": archived, "createdAt": created,
        "defaultBranchRef": {"name": "main", "target": {"committedDate": last, "recent": {
            "pageInfo": {"hasNextPage": more, "endCursor": None},
            "nodes": [{"author": a} for a in authors]}}},
        "releases": {"nodes": [{"tagName": t, "publishedAt": d, "isDraft": False, "isPrerelease": False}
                               for t, d in releases]},
        "tags": {"nodes": [{"name": t, "target": {"__typename": "Commit", "committedDate": d}} for t, d in tags]},
    }


def user(login):
    return {"email": f"{login}@example.com", "name": login, "user": {"login": login}}


class ParsingTests(unittest.TestCase):
    def test_extract_urls_keeps_balanced_parens_and_link_periods(self):
        line = ("- [Her](https://en.wikipedia.org/wiki/Her_(2013_film)) - x. "
                "[J](https://marvelcinematicuniverse.fandom.com/wiki/J.A.R.V.I.S.) and see https://example.com/a.")
        self.assertEqual(s.extract_urls(line), [
            "https://en.wikipedia.org/wiki/Her_(2013_film)",
            "https://marvelcinematicuniverse.fandom.com/wiki/J.A.R.V.I.S.",
            "https://example.com/a",
        ])

    def test_extract_urls_does_not_split_wayback_urls(self):
        url = "https://web.archive.org/web/2016/https://www.facebook.com/notes/x"
        self.assertEqual(s.extract_urls(f"- [B]({url}) - y"), [url])

    def test_extract_urls_html_and_autolinks(self):
        self.assertEqual(s.extract_urls('<a href="https://a.io/x.">b</a> <https://b.io/y>'),
                         ["https://a.io/x.", "https://b.io/y"])

    def test_parse_entries_tracks_headings_and_skips_code_and_comments(self):
        text = "\n".join([
            "# Title", "## Watch List", "### Omarchy Contenders",
            "- [One](https://github.com/a/one) - Uses [Two](https://two.dev).",
            "```", "- [Fake](https://github.com/no/no) - in a fence", "```",
            "<!--", "- [Hidden](https://github.com/no/hidden) - comment", "-->",
            "## Ears", "- [Three](https://three.dev) - x.",
        ])
        entries = s.parse_entries(text)
        self.assertEqual([e.name for e in entries], ["One", "Three"])
        self.assertEqual(entries[0].label, "Watch List › Omarchy Contenders")
        self.assertEqual(entries[0].urls, ["https://github.com/a/one", "https://two.dev"])
        self.assertEqual(entries[1].label, "Ears")

    def test_link_locations_name_non_entry_links_by_link_text(self):
        text = '# A [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)\n## S\nSee [the market](https://m.dev).'
        locs = s.collect_link_locations({"readme.md": text})
        self.assertEqual(locs["https://awesome.re"][0].name, "Awesome")
        self.assertEqual(locs["https://m.dev"][0].name, "the market")
        self.assertEqual(locs["https://m.dev"][0].line, 3)

    def test_github_repo(self):
        self.assertEqual(s.github_repo("https://github.com/a/b#readme"), ("a", "b"))
        self.assertEqual(s.github_repo("https://github.com/a/b.git"), ("a", "b"))
        self.assertEqual(s.github_repo("https://github.com/a/b/tree/main/x"), ("a", "b"))
        self.assertIsNone(s.github_repo("https://github.com/orgs/a"))
        self.assertIsNone(s.github_repo("https://github.com/a"))
        self.assertIsNone(s.github_repo("https://github.blog/a/b"))

    def test_registrable_domain(self):
        self.assertEqual(s.registrable_domain("docs.openclaw.ai"), "openclaw.ai")
        self.assertEqual(s.registrable_domain("www.bbc.co.uk"), "bbc.co.uk")
        self.assertEqual(s.registrable_domain("os-world.github.io"), "os-world.github.io")

    def test_scorecard_table_matches_data_file_shape(self):
        text = (s.ROOT / "readme.md").read_text(encoding="utf-8")
        rows = s.parse_scorecard_table(text)
        self.assertGreater(len(rows), 0)
        for row in rows:
            self.assertIn(row["tested"], s.TESTED_LEVELS, row)
            self.assertTrue(set(row["scores"].values()) <= {"full", "partial", "none"}, row)

    def test_scorecard_data_file_is_valid(self):
        agents = json.loads((s.ROOT / "data" / "scorecard.json").read_text(encoding="utf-8"))["agents"]
        s.validate_scorecard(agents)

    def test_scorecard_sync_flags_drift(self):
        table = [{"name": "A", "platform": "Mac", "scores": {"voice": "full"}, "tested": "code", "watchOut": "x"},
                 {"name": "B", "platform": "Mac", "scores": {"voice": "full"}, "tested": "code", "watchOut": "x"}]
        agents = [{"name": "A", "platform": "Mac", "scores": {"voice": "partial"}, "tested": "code", "watchOut": "x",
                   "section": "S", "url": "u"},
                  {"name": "C", "platform": "Mac", "scores": {}, "tested": "code", "watchOut": "", "section": "S",
                   "url": "u"}]
        found = {f.key: f.problem for f in s.scorecard_sync_findings(table, agents)}
        self.assertIn("scores.voice", found["retest:sync:A"])
        self.assertIn("missing from data/scorecard.json", found["retest:sync:B"])
        self.assertIn("not in the readme", found["retest:sync:C"])


class LinkClassificationTests(unittest.TestCase):
    def test_dead_statuses_flagged_even_on_allowlisted_hosts(self):
        self.assertEqual(s.classify_link("https://x.fandom.com/a", 404, None, None, ALLOW)[0], "dead")
        self.assertEqual(s.classify_link("https://a.dev", 410, None, None, ALLOW)[0], "dead")

    def test_bot_walls(self):
        self.assertEqual(s.classify_link("https://x.fandom.com/a", 403, None, None, ALLOW)[0], "skipped")
        self.assertEqual(s.classify_link("https://a.dev", 403, None, None, ALLOW)[0], "blocked")

    def test_redirects(self):
        self.assertEqual(s.classify_link("https://a.dev/x", 200, "https://www.a.dev/y", None, ALLOW)[0], "ok")
        kind, detail = s.classify_link("https://a.ai/x", 200, "https://a.com/x", None, ALLOW)
        self.assertEqual((kind, detail), ("redirect", "redirects to https://a.com/x"))
        self.assertEqual(s.classify_link("https://livekit.io/join-slack", 200, "https://x.slack.com/j", None,
                                         ALLOW)[0], "skipped")

    def test_network_errors(self):
        nxdomain = socket.gaierror(socket.EAI_NONAME, "nodename nor servname provided")
        self.assertEqual(s.classify_link("https://gone.dev", None, None, nxdomain, ALLOW)[0], "dead")
        self.assertEqual(s.classify_link("https://a.dev", None, None, TimeoutError(), ALLOW)[0], "transient")
        self.assertEqual(s.classify_link("https://a.dev", 503, None, None, ALLOW)[0], "transient")
        self.assertEqual(s.classify_link("https://x.fandom.com", None, None, TimeoutError(), ALLOW)[0], "skipped")


class RepoHealthTests(unittest.TestCase):
    def entries(self, section):
        return [s.Entry("Thing", "https://github.com/Own/Thing", section, None, 7, ["https://github.com/Own/Thing"])]

    def run_check(self, section, data):
        report = s.Report(TODAY)
        s.repo_findings(self.entries(section), {"Own/Thing": data}, TODAY, report)
        return [f.key for f in report.findings]

    def test_healthy_and_case_only_rename(self):
        self.assertEqual(self.run_check("Ears", repo("own/thing")), [])

    def test_missing_moved_archived(self):
        self.assertEqual(self.run_check("Ears", None), ["repo:missing:own/thing"])
        self.assertEqual(self.run_check("Ears", repo("new/thing")), ["repo:moved:own/thing"])
        self.assertEqual(self.run_check("Ears", repo("Own/Thing", archived=True)), ["repo:archived:own/thing"])

    def test_staleness_rules_by_section(self):
        eight_months = repo("Own/Thing", last="2026-01-20T00:00:00Z")
        self.assertEqual(self.run_check("Jarvis Agents", eight_months), ["repo:stale:own/thing"])
        self.assertEqual(self.run_check("Mission Control", eight_months), ["repo:stale:own/thing"])
        self.assertEqual(self.run_check("Ears", eight_months), [])
        self.assertEqual(self.run_check("Ears", repo("Own/Thing", last="2025-09-01T00:00:00Z")),
                         ["repo:stale:own/thing"])
        self.assertEqual(self.run_check("Watch List", eight_months), [])  # reported as a drop candidate instead


class RetestTests(unittest.TestCase):
    def agent(self, **kw):
        base = {"name": "Agent", "url": "https://github.com/o/r", "repo": "o/r", "section": "S", "tested": "hands-on",
                "testedAt": "2026-09-27", "testedVersion": "0.9.2", "watchOut": ""}
        base.update(kw)
        return base

    def test_parse_version(self):
        self.assertEqual(s.parse_version("v2026.9.24"), (2026, 9, 24))
        self.assertEqual(s.parse_version("@usejarvis/brain 0.14.0"), (0, 14, 0))
        self.assertEqual(s.parse_version("rc.14-v0.21.5"), (0, 21, 5))
        self.assertIsNone(s.parse_version("d6ebaa6"))
        self.assertIsNone(s.parse_version("nightly"))

    def test_minor_bump_flags_patch_does_not(self):
        r = repo(releases=[("v0.10.1", "2026-09-28T00:00:00Z"), ("v0.9.2", "2026-09-24T00:00:00Z")])
        [f] = s.retest_findings(self.agent(), r, TODAY)
        self.assertEqual(f.key, "retest:release:Agent")
        self.assertIn("minor bump", f.problem)
        r = repo(releases=[("v0.9.7", "2026-09-28T00:00:00Z")])
        self.assertEqual(s.retest_findings(self.agent(), r, TODAY), [])

    def test_highest_version_wins_over_newest_created(self):
        r = repo(releases=[("v2026.8.33", "2026-09-29T00:00:00Z"), ("v2026.9.6", "2026-09-23T00:00:00Z")])
        self.assertEqual(s.retest_findings(self.agent(testedVersion="2026.9.6"), r, TODAY), [])

    def test_tag_pattern_filters_other_packages(self):
        r = repo(releases=[("installer-v1.0.0", "2026-09-28T00:00:00Z"), ("v0.14.0", "2026-09-22T00:00:00Z")])
        self.assertEqual(s.retest_findings(self.agent(testedVersion="0.14.0", tagPattern=r"^v\d"), r, TODAY), [])
        self.assertEqual(len(s.retest_findings(self.agent(testedVersion="0.14.0"), r, TODAY)), 1)

    def test_unknown_version_uses_release_current_at_test_date(self):
        r = repo(releases=[("v2.1.0", "2026-09-28T00:00:00Z"), ("v2.0.1", "2026-09-26T00:00:00Z")])
        [f] = s.retest_findings(self.agent(testedVersion=None, testedAt="2026-09-26", tested="code"), r, TODAY)
        self.assertIn("`v2.0.1`, the newest release when it was tested with no version recorded", f.problem)
        self.assertIn("Re-review", f.action)
        [f] = s.retest_findings(self.agent(testedVersion="16e37bd", testedAt="2026-09-26"), r, TODAY)
        self.assertIn("at commit `16e37bd`", f.problem)

    def test_prereleases_are_ignored(self):
        flagged = repo(releases=[("v0.10.0", "2026-09-28T00:00:00Z"), ("v0.9.2", "2026-09-24T00:00:00Z")])
        flagged["releases"]["nodes"][0]["isPrerelease"] = True
        self.assertEqual(s.retest_findings(self.agent(), flagged, TODAY), [])
        suffixed = repo(releases=[("v0.10.0-beta.1", "2026-09-28T00:00:00Z"), ("v0.9.2", "2026-09-24T00:00:00Z")])
        self.assertEqual(s.retest_findings(self.agent(), suffixed, TODAY), [])
        day = "2026-09-28T00:00:00Z"
        tags = repo(tags=[("v0.21.4+canary.20260928T0713Z", day), ("rc.14-v0.21.5", day),
                          ("cli-1.3.0-rc.1", day), ("v0.9.2", "2026-09-24T00:00:00Z")])
        self.assertEqual([c["tag"] for c in s.release_candidates(tags, None)], ["v0.9.2"])

    def test_tags_used_when_there_are_no_releases(self):
        r = repo(tags=[("v1.1.0", "2026-09-28T00:00:00Z"), ("v1.0.0", "2026-09-01T00:00:00Z")])
        self.assertEqual(len(s.retest_findings(self.agent(testedVersion="1.0.0"), r, TODAY)), 1)

    def test_first_release_after_test(self):
        r = repo(releases=[("v0.1.0", "2026-09-28T00:00:00Z")])
        [f] = s.retest_findings(self.agent(testedVersion="d6ebaa6"), r, TODAY)
        self.assertIn("First versioned release", f.problem)

    def test_quarterly_age(self):
        keys = [f.key for f in s.retest_findings(self.agent(testedAt="2026-06-01", repo=None), None, TODAY)]
        self.assertEqual(keys, ["retest:age:Agent"])
        self.assertEqual(s.retest_findings(self.agent(testedAt="2026-07-01", repo=None), None, TODAY), [])


class WatchListTests(unittest.TestCase):
    entry = s.Entry("W", "https://github.com/o/w", "Watch List", "Omarchy Contenders", 3, [])

    def test_promote_needs_two_regular_humans_and_three_months(self):
        regulars = [user("a")] * 4 + [user("b")] * 3 + [user("c")]
        [f] = s.watch_findings(self.entry, repo("o/w", authors=regulars), TODAY)
        self.assertEqual(f.key, "watch:promote:o/w")
        self.assertIn("2 people made 3 or more commits each", f.problem)
        self.assertIn("a 4, b 3, c 1", f.problem)
        young = repo("o/w", authors=regulars, created="2026-08-01T00:00:00Z")
        self.assertEqual(s.watch_findings(self.entry, young, TODAY), [])

    def test_drive_by_commits_do_not_count(self):
        drive_by = [user("a")] * 50 + [user("b")] * 2 + [user("c")]
        self.assertEqual(s.watch_findings(self.entry, repo("o/w", authors=drive_by), TODAY), [])

    def test_bots_do_not_count(self):
        bot = {"email": "x", "name": "dependabot[bot]", "user": {"login": "dependabot[bot]"}}
        self.assertEqual(s.watch_findings(self.entry, repo("o/w", authors=[user("a")] * 3 + [bot] * 5), TODAY), [])

    def test_drop_after_six_months_quiet(self):
        [f] = s.watch_findings(self.entry, repo("o/w", last="2026-03-01T00:00:00Z"), TODAY)
        self.assertEqual(f.key, "watch:drop:o/w")

    def test_archived_or_missing_left_to_repo_health(self):
        self.assertEqual(s.watch_findings(self.entry, None, TODAY), [])
        self.assertEqual(s.watch_findings(self.entry, repo("o/w", archived=True), TODAY), [])


def finding(key, name="N", check="links"):
    return s.Finding(check, key, name, "Section", "https://x.dev", "Broken.", "Fix it.")


class FingerprintTests(unittest.TestCase):
    def test_fingerprint_is_order_independent(self):
        self.assertEqual(s.fingerprint({"a", "b"}), s.fingerprint({"b", "a"}))
        self.assertNotEqual(s.fingerprint({"a"}), s.fingerprint({"a", "b"}))

    def test_hidden_block_round_trip_with_double_dashes(self):
        keys = {"link:dead:https://a.dev/x--y-->z", "retest:age:A"}
        block = s.hidden_block(keys)
        self.assertEqual(block.count("--"), 2)  # only the comment's own delimiters
        self.assertEqual(s.parse_hidden_block(f"text\n\n{block}\n"), keys)

    def test_parse_hidden_block_missing(self):
        self.assertIsNone(s.parse_hidden_block("edited by hand"))
        self.assertIsNone(s.parse_hidden_block(None))

    def test_report_escapes_mentions_and_embeds_keys(self):
        report = s.Report(TODAY, [finding("k1", name="@usejarvis/brain")], ran=list(s.CHECKS))
        body = s.render_report(report)
        self.assertNotIn("@usejarvis", body)
        self.assertEqual(s.parse_hidden_block(body), {"k1"})
        self.assertIn("## Dead links (1)", body)
        self.assertIn("## Watch List review (0)", body)


class PublishDecisionTests(unittest.TestCase):
    def test_nothing_found_and_no_issue(self):
        self.assertEqual(s.plan_publish(None, "body", [], "csells"), [])

    def test_nothing_found_closes_open_issue(self):
        kinds = [a.kind for a in s.plan_publish({"number": 5, "body": "old"}, "body", [], "csells")]
        self.assertEqual(kinds, ["comment", "close"])

    def test_first_findings_create_assigned_issue(self):
        [a] = s.plan_publish(None, "body", [finding("k1")], "csells")
        self.assertEqual((a.kind, a.title, a.assignee), ("create", "Staleness report", "csells"))

    def test_same_findings_update_quietly(self):
        old = s.render_report(s.Report(TODAY - dt.timedelta(days=7), [finding("k1")], ran=list(s.CHECKS)))
        new = s.render_report(s.Report(TODAY, [finding("k1")], ran=list(s.CHECKS)))
        self.assertEqual([a.kind for a in s.plan_publish({"number": 5, "body": old}, new, [finding("k1")], "c")],
                         ["update"])
        self.assertEqual(s.plan_publish({"number": 5, "body": new}, new, [finding("k1")], "c"), [])

    def test_new_findings_mention_owner_with_only_the_new_items(self):
        old = s.render_report(s.Report(TODAY, [finding("k1", "Old")], ran=list(s.CHECKS)))
        findings = [finding("k1", "Old"), finding("k2", "New")]
        new = s.render_report(s.Report(TODAY, findings, ran=list(s.CHECKS)))
        update, comment = s.plan_publish({"number": 5, "body": old}, new, findings, "csells")
        self.assertEqual((update.kind, comment.kind), ("update", "comment"))
        self.assertTrue(comment.body.startswith("@csells 1 new item since the last report"))
        self.assertIn("**New**", comment.body)
        self.assertNotIn("**Old**", comment.body)

    def test_resolved_findings_do_not_mention(self):
        old = s.render_report(s.Report(TODAY, [finding("k1"), finding("k2")], ran=list(s.CHECKS)))
        new = s.render_report(s.Report(TODAY, [finding("k1")], ran=list(s.CHECKS)))
        self.assertEqual([a.kind for a in s.plan_publish({"number": 5, "body": old}, new, [finding("k1")], "c")],
                         ["update"])


class IgnoreTests(unittest.TestCase):
    def report(self):
        return s.Report(TODAY, [finding("link:dead:a"), finding("repo:stale:o/r", check="repos")], ran=list(s.CHECKS))

    def test_ignored_findings_leave_the_open_list(self):
        report = self.report()
        s.apply_ignores(report, [{"key": "link:dead:a", "reason": "Kept on purpose", "until": "2026-12-31"}])
        self.assertEqual([f.key for f in report.findings], ["repo:stale:o/r"])
        body = s.render_report(report)
        self.assertEqual(s.parse_hidden_block(body), {"repo:stale:o/r"})
        self.assertIn("<summary>Ignored (1", body)
        self.assertIn("**Ignored:** Kept on purpose (until 2026-12-31)", body)
        self.assertIn("1 item need", body)

    def test_expired_and_unused_ignores_become_notes(self):
        report = self.report()
        s.apply_ignores(report, [{"key": "link:dead:a", "reason": "r", "until": "2026-09-28"},
                                 {"key": "watch:drop:x/y", "reason": "r"}])
        self.assertEqual(len(report.findings), 2)
        notes = " ".join(report.notes["links"] + report.notes["watch"])
        self.assertIn("expired on 2026-09-28", notes)
        self.assertIn("watch:drop:x/y matched nothing", notes)

    def test_only_ignored_findings_close_the_issue(self):
        report = self.report()
        s.apply_ignores(report, [{"key": "link:dead:a", "reason": "r"}, {"key": "repo:stale:o/r", "reason": "r"}])
        kinds = [a.kind for a in s.plan_publish({"number": 1, "body": "x"}, s.render_report(report),
                                                report.findings, "c")]
        self.assertEqual(kinds, ["comment", "close"])

    def test_newly_ignored_finding_does_not_mention(self):
        old = s.render_report(self.report())
        report = self.report()
        report.findings.append(finding("link:dead:b"))
        s.apply_ignores(report, [{"key": "link:dead:b", "reason": "r"}])
        kinds = [a.kind for a in s.plan_publish({"number": 1, "body": old}, s.render_report(report),
                                                report.findings, "c")]
        self.assertEqual(kinds, ["update"])

    def test_ignore_file_needs_reasons(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d) / "staleness-ignore.json"
            tmp.write_text(json.dumps({"ignore": [{"key": "k"}]}))
            with self.assertRaises(s.ScriptError):
                s.load_ignores(tmp)
            tmp.write_text(json.dumps({"ignore": [{"key": "k", "reason": "r", "until": "soon"}]}))
            with self.assertRaises(s.ScriptError):
                s.load_ignores(tmp)
        self.assertEqual(s.load_ignores(s.ROOT / "data" / "staleness-ignore.json"),
                         json.loads((s.ROOT / "data" / "staleness-ignore.json").read_text())["ignore"])


class FakeGitHub:
    """Stands in for `gh api` with an in-memory issue tracker."""

    def __init__(self):
        self.issues, self.comments, self.labels, self.calls = {}, [], set(), []

    def __call__(self, args, stdin=None, ok_codes=(0,)):
        self.calls.append(args)
        path = args[1]
        method = args[args.index("--method") + 1] if "--method" in args else "GET"
        payload = json.loads(stdin) if stdin else {}
        if path.startswith("repos/o/r/issues?"):
            return 0, json.dumps([i for i in self.issues.values()
                                  if i["state"] == "open" and "staleness" in i["labels"]]), ""
        if path == "repos/o/r/labels/staleness":
            return (0, "{}", "") if "staleness" in self.labels else (1, "", "gh: Not Found (HTTP 404)")
        if path == "repos/o/r/labels" and method == "POST":
            self.labels.add(payload["name"])
            return 0, "{}", ""
        if path == "repos/o/r/issues" and method == "POST":
            n = len(self.issues) + 1
            self.issues[n] = {"number": n, "state": "open", "title": payload["title"], "body": payload["body"],
                              "labels": payload["labels"], "assignees": payload["assignees"]}
            return 0, json.dumps({"number": n}), ""
        if path.endswith("/comments") and method == "POST":
            self.comments.append((int(path.split("/")[4]), payload["body"]))
            return 0, "{}", ""
        if path.startswith("repos/o/r/issues/") and method == "PATCH":
            self.issues[int(path.split("/")[4])].update(payload)
            return 0, "{}", ""
        raise AssertionError(f"unexpected gh call {args}")


class FakeIssueLifecycleTests(unittest.TestCase):
    def week(self, fake, findings, day):
        report = s.Report(day, findings, ran=list(s.CHECKS))
        body = s.render_report(report)
        with mock.patch.object(s, "gh", fake), mock.patch("sys.stderr"):
            s.apply_actions("o/r", s.plan_publish(s.find_issue("o/r"), body, findings, "csells"))

    def test_weekly_lifecycle(self):
        fake = FakeGitHub()
        self.week(fake, [finding("k1", "One")], TODAY)
        self.assertEqual(list(fake.issues), [1])
        self.assertEqual(fake.issues[1]["assignees"], ["csells"])
        self.assertIn("staleness", fake.labels)
        self.assertEqual(fake.comments, [])

        self.week(fake, [finding("k1", "One")], TODAY + dt.timedelta(days=7))
        self.assertEqual(fake.comments, [])  # same findings: body refreshed, nobody pinged
        self.assertIn(str(TODAY + dt.timedelta(days=7)), fake.issues[1]["body"])

        self.week(fake, [finding("k1", "One"), finding("k2", "Two")], TODAY + dt.timedelta(days=14))
        self.assertEqual(len(fake.comments), 1)
        self.assertIn("@csells", fake.comments[0][1])
        self.assertIn("**Two**", fake.comments[0][1])
        self.assertNotIn("**One**", fake.comments[0][1])

        self.week(fake, [], TODAY + dt.timedelta(days=21))
        self.assertEqual(fake.issues[1]["state"], "closed")
        self.assertIn("All clear", fake.comments[-1][1])

        self.week(fake, [finding("k3", "Three")], TODAY + dt.timedelta(days=28))
        self.assertEqual(list(fake.issues), [1, 2])  # a fresh issue once the old one is closed


if __name__ == "__main__":
    unittest.main()

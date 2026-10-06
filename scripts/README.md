# Scripts

## staleness.py

Checks the list for rot, following the Re-Verification rules in [methodology.md](../methodology.md#re-verification), and prints a Markdown report. It needs Python 3.12 or later and the [GitHub CLI](https://cli.github.com/), signed in (`gh auth login`). There are no other dependencies.

```sh
python3 scripts/staleness.py                    # dry run: print the report, change nothing
python3 scripts/staleness.py --only retest,watch  # run some of the checks (links, repos, retest, watch)
python3 scripts/staleness.py --publish          # also update the tracking issue (what CI does)
python3 -m unittest discover -s scripts         # offline tests
```

A full run takes about a minute. The exit status is non-zero only when the script itself fails, never because it found something.

### Checks

- **Dead links.** Every http(s) URL in README.md, blueprint.md, history.md, testing.md and methodology.md, fetched with HEAD and then GET, a browser user agent and a 20-second timeout. It flags 404, 410, domains that no longer resolve, other refusals such as 403, and redirects to a different domain. Sites in [data/link-allowlist.json](../data/link-allowlist.json) that block bots are skipped. Timeouts and server errors are listed as notes and tried again the next week. GitHub repository links are checked through the API instead, which also catches renames.
- **Repository health.** Every GitHub repository linked from README.md is checked for being missing, archived, moved (with the new URL) or stale. Stale means no commit on the default branch in 6 months for Jarvis Agents and Mission Control, or in 12 months for everything else. Watch List entries use the 6-month rule too, but they are reported under Watch List review.
- **Re-test queue.** Agents in [data/scorecard.json](../data/scorecard.json) whose last test is more than 90 days old, or whose newest stable release is a major or minor bump over the version tested. Pre-releases are ignored. It also flags any difference between that file and the readme's scorecard table.
- **Watch List review.** A Watch List entry is a *promote candidate* when at least two people (not bots) have each made three or more commits in the last 90 days, and the repository is at least three months old. The report lists commit counts per author. An entry is a *drop candidate* when it has had no commit in six months.

### The Tracking Issue

`.github/workflows/staleness.yml` runs the script with `--publish` every Monday at 15:00 UTC, and on demand from the Actions tab (untick "publish" for a dry run that only writes the job summary). It uses the workflow's own `GITHUB_TOKEN` with `issues: write`. No other secrets are needed.

With `--publish`, the script keeps a single open issue labelled `staleness`:

- If there are findings and no open issue, it creates "Staleness report", assigned to the owner, and creates the label if it's missing.
- If an issue is open, it replaces the body with the new report. It posts a comment that @mentions the owner only when there are findings that weren't in the previous report, and the comment lists just those.
- If there are no findings, it closes the issue with a short comment.

The report ends with a hidden HTML comment holding a fingerprint and the list of finding keys. That comment is how the next run tells new findings from old ones, so leave it alone when editing the issue. `--owner` (or `STALENESS_OWNER`) changes who is assigned and mentioned (default `csells`). `--repo` changes where the issue lives (default `$GITHUB_REPOSITORY`).

To mute a finding you've decided to keep, add its key to [data/staleness-ignore.json](../data/README.md#staleness-ignorejson) with a reason and, optionally, an end date. Ignored findings move to a collapsed section and don't keep the issue open.

`.github/workflows/staleness-tests.yml` runs the offline unit tests (no network) on pushes and pull requests that touch `scripts/` or `data/`.

### Clearing a Finding

Fix the list in a pull request. The next run drops fixed items, and the issue closes when nothing is left. For a link that works in a browser but fails the checker, add it to [data/link-allowlist.json](../data/link-allowlist.json). After re-testing an agent, update its `testedAt` and `testedVersion` in [data/scorecard.json](../data/scorecard.json).

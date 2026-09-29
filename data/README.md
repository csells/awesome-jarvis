# Data Files

Machine-readable data behind the list. The weekly [staleness check](../scripts/README.md) reads all three files.

## scorecard.json

One record per agent in the [scorecard](../readme.md#scorecard), with when and at which version it was last tested. Keep it in step with the scorecard table: the staleness check flags any agent whose scores, platform, "Tested" level or "Watch out" text differ between the two.

| Field | Meaning |
|---|---|
| `name` | Agent name exactly as in the scorecard's first column |
| `platform` | The scorecard's Platform column |
| `repo` | GitHub `owner/name`, or `null` for commercial products |
| `url` | The entry's link: the repository, or the vendor page for commercial products |
| `section` | Where the entry lives in the readme, such as `Jarvis Agents › macOS` |
| `scores` | `voice`, `handsFree`, `visual` and `oversight`, each `full` (●), `partial` (◐) or `none` (○) |
| `tested` | `hands-on`, `partial`, `code` or `docs`, matching the Tested column |
| `testedAt` | Date of the last test or review, `YYYY-MM-DD` |
| `testedVersion` | Release tag, version or commit tested, or `null` if not recorded |
| `tagPattern` | Optional regular expression that picks the relevant releases in a repository that tags several things (for example `^cli-` for Happy) |
| `watchOut` | The scorecard's "Watch out" text |

When you re-test an agent, update `testedAt` and `testedVersion` in the same pull request as the scorecard and [testing.md](../testing.md).

An agent joins the re-test queue when its `testedAt` is more than 90 days old, or when its newest stable GitHub release is a major or minor bump over `testedVersion`. Pre-releases don't count: releases GitHub marks as pre-releases, and tags with a pre-release suffix such as `-beta`, `-rc`, `-alpha` or `+canary`. If `testedVersion` is a commit or `null`, the check compares against the newest stable release that existed on `testedAt`.

## link-allowlist.json

Sites that refuse automated checkers, and links that redirect to another domain on purpose. For a matching link, the checker reports a bot-blocking status (`blockedStatuses`, normally 403, 429 and 999), a timeout, a server error or a redirect to another domain as "skipped" rather than as a finding. A 404, 410 or a domain that no longer resolves is still flagged.

- `hosts`: a host and every subdomain of it, such as `fandom.com`.
- `urls`: a URL prefix, such as `https://livekit.io/join-slack`.

Give every entry a `reason`. Add a host only after opening the link in a browser and confirming it works.

## staleness-ignore.json

Findings to leave alone, such as a Watch List entry you've decided not to promote yet. Each entry in `ignore` has:

| Field | Meaning |
|---|---|
| `key` | The finding's key, as listed in the hidden fingerprint block at the end of the report, such as `watch:promote:virtengine/bosun` |
| `reason` | Required. Why it's ignored; shown in the report |
| `until` | Optional date, `YYYY-MM-DD`. After it, the ignore stops applying and the report says so in its notes |

```json
{ "key": "watch:promote:virtengine/bosun", "reason": "Second maintainer is new; look again in January", "until": "2027-01-15" }
```

Ignored findings are listed in a collapsed "Ignored" section of the report. They don't count as open items, don't keep the issue open and don't trigger a mention. An entry that no longer matches any finding is reported as a note so it can be cleaned up.

# Weekly attestation ledger

GitHub's audit-log API is Enterprise-only (it returns 404 on this plan), and log retention
is limited. So this directory keeps a **weekly state snapshot**, hashed and anchored in
Bitcoin with OpenTimestamps.

## What a snapshot contains

| Field | Source |
|---|---|
| `org` | seats, 2FA requirement, plan, default permissions |
| `members` | current owner/member logins |
| `repo` | visibility, default branch, feature flags |
| `rulesets` | every ruleset: target, enforcement, rule types, ref conditions |
| `branches` | name, head commit SHA, protected flag |
| `tags` | name and the commit each tag points at |
| `releases` | tag, draft/prerelease, creation time |
| `issues` | number, state, labels, opened/closed timestamps |
| `events` | last 100 public org events |
| `sources` | explicit note that the audit-log API is unavailable on this plan |

## Why snapshots instead of an event log

A change to a seat, a ruleset, a tag pointer or a release shows up as a **diff between two
anchored snapshots**. Because both sides of the diff are timestamped in Bitcoin, the
timeline cannot be rewritten after the fact — not by GitHub, not by this repository, not by
whoever operates it. It also works on any plan.

## Files

| File | Content |
|---|---|
| `attest-YYYY-Www.json` | Canonical snapshot, keys sorted, one file per ISO week |
| `attest-YYYY-Www.json.ots` | OpenTimestamps receipt for that exact byte sequence |
| `manifest.jsonl` | Append-only index: week, file, sha256, anchor status, seat/rule/tag counts |

## Verify

```bash
sha256sum ledger/attest-2026-W43.json
grep 2026-W43 ledger/manifest.jsonl
ots verify ledger/attest-2026-W43.json.ots
```

`ots verify` reports `Pending confirmation` until the digest is mined into a Bitcoin block
(usually a few hours). Re-run later, or `ots upgrade` the receipt and commit the upgrade.

## Limits (stated, not hidden)

- Weekly granularity. A change made and reverted inside one week is invisible in the ledger
  (it remains visible in GitHub for the plan's retention window).
- The snapshot records state, not intent. It proves *what* the system looked like, not *why*.
- Redaction: no IP addresses, user agents or tokens are captured — the snapshot uses public
  and administrator-visible metadata only.
- If the job stops, the missing week is itself evidence. Gaps are not swept under the rug.

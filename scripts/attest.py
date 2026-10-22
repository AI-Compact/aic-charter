#!/usr/bin/env python3
"""Weekly state attestation for AI Compact (AIC).

Why not simply export the audit log? GitHub's audit-log API is Enterprise-only
(the endpoint returns 404 on the free plan). So instead we take a full weekly
snapshot of everything that matters — seats, rulesets, tags, branches, releases,
issues, public events — hash it, and anchor that hash in Bitcoin via OpenTimestamps.

Effect: any later change to seats, protection rules, tags or charter anchors shows up
as a diff between two Bitcoin-anchored snapshots. Tamper-evident, plan-independent.

Usage:  GH_TOKEN=... python3 scripts/attest.py [--push]
Env:    GH_TOKEN (admin:org + repo), AIC_ORG, AIC_REPO
"""

import argparse, base64, datetime as dt, hashlib, json, os, subprocess, sys
import urllib.request, urllib.error

API = "https://api.github.com"
ORG = os.environ.get("AIC_ORG", "AI-Compact")
REPO = os.environ.get("AIC_REPO", "AI-Compact/aic-charter")
TOKEN = os.environ.get("GH_TOKEN", "").strip()

ORG_KEYS = ["login", "name", "two_factor_requirement_enabled", "members_count",
            "default_repository_permission", "members_can_create_repositories",
            "members_can_create_public_repositories"]

EMAIL_RE = None  # set below


def scrub(obj):
    """Drop anything that looks like a personal identifier (email, phone)."""
    import re
    email = re.compile(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", re.I)
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if "email" in k.lower():
                continue
            out[k] = scrub(v)
        return out
    if isinstance(obj, list):
        return [scrub(x) for x in obj]
    if isinstance(obj, str):
        return email.sub("[redacted]", obj)
    return obj


def gh(path):
    req = urllib.request.Request(API + path)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--dir", default="ledger")
    args = ap.parse_args()
    if not TOKEN:
        # No credential on this machine: skip cleanly instead of failing every week.
        print("SKIP: no token present (~/.dsh/aic-audit.token). Attestation not taken.")
        sys.exit(0)

    snap = {"kind": "aic-weekly-attestation", "issuer": "aic",
            "charter_version": "compact:v1.2",
            "taken_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}

    st, org = gh(f"/orgs/{ORG}")
    snap["org"] = {k: org.get(k) for k in ORG_KEYS if k in org}
    snap["org"]["plan"] = (org.get("plan") or {}).get("name")

    st, mem = gh(f"/orgs/{ORG}/members?per_page=100")
    snap["members"] = sorted(m.get("login") for m in mem) if isinstance(mem, list) else []

    st, repo = gh(f"/repos/{REPO}")
    snap["repo"] = {"full_name": repo.get("full_name"), "visibility": repo.get("visibility"),
                    "default_branch": repo.get("default_branch"),
                    "has_issues": repo.get("has_issues"), "has_wiki": repo.get("has_wiki"),
                    "archived": repo.get("archived")}

    st, rs = gh(f"/repos/{REPO}/rulesets")
    snap["rulesets"] = []
    for r in (rs if isinstance(rs, list) else []):
        st2, d = gh(f"/repos/{REPO}/rulesets/{r['id']}")
        snap["rulesets"].append({"id": r["id"], "name": r.get("name"), "target": r.get("target"),
                                 "enforcement": d.get("enforcement"),
                                 "rules": sorted(x.get("type") for x in d.get("rules", [])),
                                 "include": (d.get("conditions", {}).get("ref_name", {}) or {}).get("include")})
    snap["rulesets"].sort(key=lambda x: x["name"] or "")

    st, br = gh(f"/repos/{REPO}/branches?per_page=100")
    snap["branches"] = sorted(({"name": b["name"], "sha": b["commit"]["sha"], "protected": b.get("protected")}
                               for b in (br if isinstance(br, list) else [])), key=lambda x: x["name"])

    st, tags = gh(f"/repos/{REPO}/tags?per_page=100")
    snap["tags"] = sorted(({"name": t["name"], "sha": t["commit"]["sha"]} for t in (tags if isinstance(tags, list) else [])),
                          key=lambda x: x["name"])

    st, rel = gh(f"/repos/{REPO}/releases?per_page=100")
    snap["releases"] = sorted(({"tag": r.get("tag_name"), "draft": r.get("draft"), "prerelease": r.get("prerelease"),
                                "created_at": r.get("created_at")} for r in (rel if isinstance(rel, list) else [])),
                              key=lambda x: x.get("tag") or "")

    st, iss = gh(f"/repos/{REPO}/issues?state=all&per_page=100")
    snap["issues"] = sorted(({"number": i["number"], "state": i["state"],
                              "labels": sorted(l["name"] for l in i.get("labels", [])),
                              "created_at": i.get("created_at"), "closed_at": i.get("closed_at")}
                             for i in (iss if isinstance(iss, list) else [])), key=lambda x: x["number"])

    st, ev = gh(f"/orgs/{ORG}/events?per_page=100")
    snap["events"] = [{"type": e.get("type"), "actor": (e.get("actor") or {}).get("login"),
                       "repo": (e.get("repo") or {}).get("name"), "created_at": e.get("created_at")}
                      for e in (ev if isinstance(ev, list) else [])]

    snap = scrub(snap)

    # honesty about what could not be captured
    snap["sources"] = {"audit_log_api": "unavailable on this plan (HTTP 404); Enterprise-only",
                       "method": "weekly state snapshot + OpenTimestamps"}

    os.makedirs(args.dir, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)
    y, w, _ = now.isocalendar()
    week = f"{y}-W{w:02d}"
    path = os.path.join(args.dir, f"attest-{week}.json")
    blob = json.dumps(snap, ensure_ascii=False, sort_keys=True, indent=1)
    open(path, "w", encoding="utf-8").write(blob + "\n")
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()

    receipt = path + ".ots"
    if os.path.exists(receipt):
        os.remove(receipt)          # a stale receipt would refer to older bytes
    anchored = False
    try:
        subprocess.run(["ots", "stamp", path], check=True, capture_output=True, timeout=180)
        anchored = os.path.exists(receipt)
    except Exception as ex:
        print("WARN ots:", ex, file=sys.stderr)

    man = os.path.join(args.dir, "manifest.jsonl")
    rows = [json.loads(l) for l in open(man, encoding="utf-8")] if os.path.exists(man) else []
    rows = [r for r in rows if r["week"] != week]
    rows.append({"week": week, "file": path, "sha256": sha, "anchored": anchored,
                 "seats": len(snap["members"]), "rulesets": len(snap["rulesets"]),
                 "tags": len(snap["tags"]), "issues": len(snap["issues"]),
                 "created_at": snap["taken_at"]})
    rows.sort(key=lambda r: r["week"])
    open(man, "w", encoding="utf-8").write("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n")

    print(f"week={week} sha256={sha} anchored={anchored} seats={len(snap['members'])} "
          f"rulesets={len(snap['rulesets'])} tags={len(snap['tags'])}")
    if not args.push:
        print("dry run")
        return
    for p in (path, receipt, man):
        if not os.path.exists(p):
            continue
        st, cur = gh(f"/repos/{REPO}/contents/{p}")
        body = {"message": f"ledger: weekly attestation {week}\n\nissuer=aic\ncharter_version=compact:v1.2",
                "content": base64.b64encode(open(p, "rb").read()).decode()}
        if st == 200 and isinstance(cur, dict) and cur.get("sha"):
            body["sha"] = cur["sha"]
        req = urllib.request.Request(f"{API}/repos/{REPO}/contents/{p}", data=json.dumps(body).encode(), method="PUT")
        req.add_header("Authorization", "Bearer " + TOKEN)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                print("push", p, r.status)
        except urllib.error.HTTPError as e:
            print("push FAILED", p, e.code, e.read().decode()[:150], file=sys.stderr)


if __name__ == "__main__":
    main()

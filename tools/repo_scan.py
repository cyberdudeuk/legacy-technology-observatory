"""Quarterly scan of public government repositories by primary language.

Counts public repositories whose primary language matches each entry in
LANGUAGES across the organisations in data/repo-scan.json, plus code-search
hits for legacy terms. Writes data/repo-scan.json and a Markdown report that
compares with the previous run.

Uses only the standard library. Needs GITHUB_TOKEN (the workflow's own
read-only token is enough). Search allows about 30 requests a minute, so the
script waits between calls.

Run:  GITHUB_TOKEN=... python tools/repo_scan.py --report scan-report.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "repo-scan.json"
API = "https://api.github.com"
LANGUAGES = ["JavaScript", "Scala", "Python", "Ruby", "HCL", "Shell", "Java", "C#", "TypeScript",
             "Kotlin", "Go", "PHP", "Perl", "R", "Fortran", "PLSQL", "COBOL"]
DISPLAY = {"PLSQL": "PL/SQL"}
TERMS = ["COBOL", "mainframe"]
PAUSE = 2.5


def _get(path: str, params: dict) -> dict:
    url = f"{API}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "User-Agent": "legacy-code-observatory-scan",
    })
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 (fixed https host)
        return json.load(r)


def count_repos(lang: str, orgs: list[str]) -> int:
    q = f'language:"{lang}" ' + " ".join(f"org:{o}" for o in orgs)
    return int(_get("/search/repositories", {"q": q, "per_page": 1})["total_count"])


def count_code(term: str, orgs: list[str]) -> int:
    q = f'"{term}" ' + " OR ".join(f"org:{o}" for o in orgs)
    return int(_get("/search/code", {"q": q, "per_page": 1})["total_count"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default="scan-report.md")
    args = ap.parse_args()
    if not os.environ.get("GITHUB_TOKEN"):
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 2
    prev = json.loads(OUT.read_text(encoding="utf-8"))
    orgs = prev["orgs"]
    langs = []
    for lang in LANGUAGES:
        langs.append({"name": DISPLAY.get(lang, lang), "count": count_repos(lang, orgs)})
        time.sleep(PAUSE)
    mentions = {}
    for term in TERMS:
        try:
            mentions[term] = count_code(term, orgs)
        except Exception as e:  # code search can be refused; record and carry on
            mentions[term] = prev.get("mentions", {}).get(term)
            print(f"code search for {term} failed: {e}", file=sys.stderr)
        time.sleep(PAUSE)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new = {"date": now, "method": prev["method"], "orgs": orgs, "languages": langs, "mentions": mentions}
    OUT.write_text(json.dumps(new, indent=1) + "\n", encoding="utf-8")

    before = {x["name"]: x["count"] for x in prev["languages"]}
    lines = [f"# Quarterly repository scan, {now[:10]}", "",
             f"Compared with the previous run on {prev['date'][:10]}.", "",
             "| Language | Before | Now | Change |", "|---|---:|---:|---:|"]
    for x in sorted(langs, key=lambda y: -y["count"]):
        b = before.get(x["name"], 0)
        lines.append(f"| {x['name']} | {b} | {x['count']} | {x['count'] - b:+d} |")
    lines += ["", "Code mentions: " + ", ".join(f"{k} {v}" for k, v in mentions.items()), "",
              "Review the changes, update any text on the site that quotes these numbers, then merge."]
    Path(args.report).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())

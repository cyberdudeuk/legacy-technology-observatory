"""Static checks for the Legacy Code Observatory.

Each check returns a list of problems (empty means pass). The tests in
tests/test_checks.py run every check against the real site and against a
known-bad sample, so a check that cannot fail is caught.

Run:  python tools/checks.py
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site" / "index.html"
DATA = ROOT / "data" / "observatory.json"

EMAIL = re.compile(r"[\w.+-]{1,64}@[\w-]{1,63}\.[\w.]{2,}")  # bounded to keep scans linear (defect D10)
RETIRED = re.compile(r"Office of the Chief Data Officer|Data Management Team", re.I)
MAX_BYTES = 400_000
ALLOWED_SCRIPT_HOSTS = ("https://cdnjs.cloudflare.com/",)


class _Text(HTMLParser):
    """Collects visible text outside <script> and <style>, and script sources."""

    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.text: list[str] = []
        self.script_srcs: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
            src = dict(attrs).get("src")
            if tag == "script" and src:
                self.script_srcs.append(src)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


def _walk_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _walk_strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _walk_strings(v)


def _records_with_sources(data):
    for key, val in data.items():
        if isinstance(val, list):
            for rec in val:
                if isinstance(rec, dict) and isinstance(rec.get("s"), list):
                    yield key, rec


def check_no_emails(html: str, data: dict) -> list[str]:
    """No email address in visible HTML or in any data value (defect rule: contact by form only)."""
    p = _Text()
    p.feed(html)
    found = EMAIL.findall(" ".join(p.text)) + [m for s in _walk_strings(data) for m in EMAIL.findall(s)]
    return [f"email address found: {e}" for e in found]


def check_retired_names(html: str, data: dict) -> list[str]:
    p = _Text()
    p.feed(html)
    hits = RETIRED.findall(" ".join(p.text)) + [m for s in _walk_strings(data) for m in RETIRED.findall(s)]
    return [f"retired name found: {h}" for h in hits]


def check_sources_https(html: str, data: dict) -> list[str]:
    bad = []
    for sid, src in data.get("sources", {}).items():
        url = src.get("url", "")
        if not (url.startswith("https://") or url.startswith("#")):
            bad.append(f"{sid} is not https: {url}")
    return bad


def check_citations_known(html: str, data: dict) -> list[str]:
    known = set(data.get("sources", {}))
    bad = []
    for key, rec in _records_with_sources(data):
        for sid in rec["s"]:
            if sid not in known:
                bad.append(f"{key}: unknown source {sid}")
    return bad


def check_registers_cited(html: str, data: dict) -> list[str]:
    """Every system and devolved/local record cites at least one source."""
    bad = []
    for key in ("systems", "devolved_and_local"):
        for rec in data.get(key, []):
            if not rec.get("s"):
                bad.append(f"{key}: {rec.get('n', '?')} has no source")
    return bad


def check_unsourced_labelled(html: str, data: dict) -> list[str]:
    bad = []
    for rec in data.get("languages", []):
        if not rec.get("s") and rec.get("ev") not in ("unconfirmed", "analysis"):
            bad.append(f"language {rec.get('n')} has no source and is not labelled")
    return bad


def check_requirements_traced(html: str, data: dict) -> list[str]:
    needs = {n[0] for n in data.get("user_needs", [])}
    bad = []
    for r in data.get("requirements", []):
        rid, _, rneeds, _, checks, _, status = r
        if not rneeds or any(n not in needs for n in rneeds):
            bad.append(f"{rid} does not trace to a known user need")
        if not checks and status != "Planned":
            bad.append(f"{rid} has no verifying check")
    return bad


def check_size(html: str, data: dict) -> list[str]:
    n = len(html.encode("utf-8"))
    return [f"page is {n} bytes, over {MAX_BYTES}"] if n > MAX_BYTES else []


def check_pinned_scripts(html: str, data: dict) -> list[str]:
    p = _Text()
    p.feed(html)
    bad = []
    for src in p.script_srcs:
        if not src.startswith(ALLOWED_SCRIPT_HOSTS):
            bad.append(f"script from an unexpected host: {src}")
        if re.search(r"@latest|/latest/", src) or not re.search(r"/\d+\.\d+\.\d+/", src):
            bad.append(f"script not pinned to an exact version: {src}")
    return bad


def check_no_eval(html: str, data: dict) -> list[str]:
    return ["page uses eval or new Function"] if re.search(r"\beval\(|new Function\(", html) else []


def check_json_ld(html: str, data: dict) -> list[str]:
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if not m:
        return ["no JSON-LD description"]
    try:
        json.loads(m.group(1))
    except ValueError as e:
        return [f"JSON-LD does not parse: {e}"]
    return []


CHECKS = [
    check_no_emails, check_retired_names, check_sources_https, check_citations_known,
    check_registers_cited, check_unsourced_labelled, check_requirements_traced,
    check_size, check_pinned_scripts, check_no_eval, check_json_ld,
]


def run(html: str, data: dict) -> dict[str, list[str]]:
    return {c.__name__: c(html, data) for c in CHECKS}


def main() -> int:
    html = SITE.read_text(encoding="utf-8")
    data = json.loads(DATA.read_text(encoding="utf-8"))
    results = run(html, data)
    failed = 0
    for name, problems in results.items():
        status = "PASS" if not problems else "FAIL"
        print(f"{status}  {name}")
        for p in problems:
            print(f"      - {p}")
        failed += bool(problems)
    print(f"\n{len(results) - failed} of {len(results)} checks pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

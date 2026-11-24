"""Monthly maintenance: source links and evidence freshness.

- Requests every source URL in data/observatory.json and lists any that fail.
- Flags the evidence as due for review when it is older than REVIEW_DAYS.
Writes a Markdown report and exits 1 when something needs attention, so the
workflow can open or update one tracking issue.

Run:  python tools/maintenance.py --out maintenance-report.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "observatory.json"
REVIEW_DAYS = 100
# Sites that refuse automated requests; a failure here is reported as "check by hand", not broken.
SOFT = (403, 405, 406, 429, 999)


def check_url(url: str) -> tuple[str, str]:
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0 (link check; legacy-technology-observatory)"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:  # noqa: S310 (https only, from our own data)
            return "ok", str(r.status)
    except urllib.error.HTTPError as e:
        return ("manual" if e.code in SOFT else "broken"), str(e.code)
    except Exception as e:  # timeouts, DNS, TLS
        return "broken", type(e).__name__


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="maintenance-report.md")
    ap.add_argument("--no-network", action="store_true", help="skip link requests (for tests)")
    args = ap.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    today = dt.date.today()
    evidence = dt.date.fromisoformat(data["evidence_date"])
    age = (today - evidence).days
    broken, manual = [], []
    if not args.no_network:
        for sid, src in data["sources"].items():
            url = src["url"]
            if not url.startswith("https://"):
                continue
            status, detail = check_url(url)
            if status == "broken":
                broken.append(f"- {sid} [{src['title']}]({url}): {detail}")
            elif status == "manual":
                manual.append(f"- {sid} [{src['title']}]({url}): refused automated check ({detail})")
    stale = age > REVIEW_DAYS
    lines = [f"# Monthly maintenance report, {today.isoformat()}", ""]
    lines.append(f"Evidence date {evidence.isoformat()}, {age} days ago. " + ("**Review is due.**" if stale else "Review not yet due."))
    lines += ["", f"## Broken links ({len(broken)})", *(broken or ["None."]),
              "", f"## Check by hand ({len(manual)})", *(manual or ["None."])]
    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 1 if (broken or stale) else 0


if __name__ == "__main__":
    sys.exit(main())

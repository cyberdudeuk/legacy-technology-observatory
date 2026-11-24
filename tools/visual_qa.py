"""Automated visual inspection, run on every pull request and release.

Serves site/ over HTTP, then opens every section at desktop (1366px) and
phone (400px) widths in light and dark themes, with the contents drawer open
and closed. It fails when:
- the page throws a script error,
- anything makes the page scroll sideways,
- the in-page self-checks do not all pass, or a negative test does not fail.
Full-page screenshots are saved to qa-shots/ for a person to glance at.

Run:  pip install playwright==1.48.0 && python -m playwright install chromium
      python tools/visual_qa.py
"""
from __future__ import annotations

import functools
import http.server
import re
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "qa-shots"
VIEWS = ["overview", "guide", "languages", "layers", "systems", "skills", "analytics", "migration", "learning",
         "inclusion", "repos", "knowledge", "documents", "about"]
SIZES = [(1366, 900, "desktop"), (400, 860, "phone")]


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):  # keep CI logs readable
        pass


def serve() -> tuple[http.server.ThreadingHTTPServer, str]:
    handler = functools.partial(_QuietHandler, directory=str(ROOT / "site"))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}/index.html"


def main() -> int:
    SHOTS.mkdir(exist_ok=True)
    srv, url = serve()
    problems: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for scheme in ("light", "dark"):
            for w, h, tag in SIZES:
                page = browser.new_page(viewport={"width": w, "height": h}, color_scheme=scheme)
                page.on("pageerror", lambda e, t=f"{scheme} {tag}": problems.append(f"{t}: script error: {e}"))
                page.goto(url)
                page.wait_for_timeout(800)
                summary = page.inner_text("#checksSummary")
                m = re.match(r"(\d+) of (\d+) checks pass\. (\d+) of (\d+) negative", summary)
                if not m or m.group(1) != m.group(2) or m.group(3) != m.group(4):
                    problems.append(f"{scheme} {tag}: self-checks: {summary}")
                for drawer in ("as loaded", "toggled"):
                    if drawer == "toggled":
                        page.click("#drawerToggle")
                        page.wait_for_timeout(200)
                    for v in VIEWS:
                        page.evaluate(f"location.hash='#{v}'")
                        page.wait_for_timeout(150)
                        if page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"):
                            problems.append(f"{scheme} {tag} {v} (drawer {drawer}): page scrolls sideways")
                        if drawer == "as loaded":
                            page.screenshot(path=str(SHOTS / f"{scheme}-{tag}-{v}.png"), full_page=True)
                page.close()
        browser.close()
    srv.shutdown()
    if problems:
        print("Visual inspection found problems:")
        print("\n".join(f"- {x}" for x in problems))
        return 1
    print(f"Visual inspection passed: {len(VIEWS)} sections x 2 widths x 2 themes x drawer open and closed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Refresh data/observatory.json and data/xref.json from the page's own records, so the open data never
disagrees with the site. Loads site/index.html in a headless browser and reads the records it holds.
Run: python3 tools/export_data.py"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://cyberdudeuk.github.io/legacy-technology-observatory/"
CAT = "https://cyberdudeuk.github.io/github-repos-asset-catalogue/"
# JSON key -> name of the record in the page
NAMES = {"sources": "SRC", "tiles": "TILES", "findings": "FINDINGS", "languages": "LANGS", "systems": "SYS",
         "devolved_and_local": "LOCAL", "suppliers": "SUPPLIERS", "wider": "WIDER", "routes": "ROUTES", "steps": "STEPS",
         "decommissioning": "DECOM", "user_needs": "NEEDS", "requirements": "REQS", "defects": "DEFECTS",
         "glossary": "GLOSSARY", "beyond_code": "LAYERS", "costs": "COSTS",
         "representation": "REP", "pay_gaps": "PAY", "organisations_removing_barriers": "ORGS_INC",
         "case_studies": "CASES", "scenarios": "SCENARIOS", "themes": "THEMES2", "personas": "PERSONAS"}


def main():
    out_path = ROOT / "data" / "observatory.json"
    data = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"])
        pg = b.new_page()
        pg.goto((ROOT / "site" / "index.html").as_uri(), wait_until="load")
        js = "({" + ",".join(f'"{k}":(typeof {v}!=="undefined"?{v}:null)' for k, v in NAMES.items()) + \
             ',"edition":ALL.edition,"orgs":ORGS,"slugs":ORG_SLUG})'
        got = pg.evaluate(js)
        b.close()
    for k in NAMES:
        if got.get(k) is not None:
            data[k] = got[k]
    # keep the published shapes stable for reusers (repo_counts comes from tools/repo_scan.py, not the page)
    data["sources"] = {k: {"title": v[0], "url": v[1]} for k, v in got["sources"].items()}
    data["glossary"] = [{"term": g[0], "definition": g[1], "alternatives": g[2]} for g in got["glossary"]]
    data["edition"] = got["edition"]
    data["evidence_date"] = "2026-11-24"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    xref = {
        "portal": "Legacy Technology Observatory", "id": "lto", "version": got["edition"].split("-")[1],
        "as_of": data["evidence_date"], "url": SITE, "status": "Evidence base, prototype",
        "licence": "Code MIT; content and data CC BY 4.0",
        "links": "Every address also works with a hyphen for hosts that pass only a plain #name: #language-cobol, #layer-pstn.",
        "keys": {
            "languages": [{"id": l["id"], "name": l["n"], "url": f"{SITE}#language={l['id']}"} for l in got["languages"]],
            "layers": [{"id": l["id"], "name": l["n"], "layer": l["layer"], "url": f"{SITE}#layer={l['id']}"} for l in got["beyond_code"]],
            "organisations": [{"id": got["slugs"][o], "github": o, "url": f"{CAT}#org-{got['slugs'][o]}"} for o in got["orgs"]],
            "views": [{"id": v, "url": f"{SITE}#{v}"} for v in ["overview", "languages", "layers", "systems", "skills", "analytics", "migration", "learning", "repos", "knowledge"]],
        },
        "related": [{"id": "cat", "name": "GitHub Repos Asset Catalogue", "url": CAT, "manifest": CAT + "data/xref.json"}],
    }
    (ROOT / "data" / "xref.json").write_text(json.dumps(xref, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"exported {len(data)} record sets; xref with {sum(len(v) for v in xref['keys'].values())} keys")


if __name__ == "__main__":
    main()

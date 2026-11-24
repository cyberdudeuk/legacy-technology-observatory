# Legacy Technology Observatory

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24500735.svg)](https://doi.org/10.5281/zenodo.24500735)

*Formerly the Legacy Code Observatory (renamed in 3.0 when it widened beyond code).*

The old technology behind UK public services, from programming languages and mainframes to phone lines, emergency radio, devices and encryption: where it runs, what it costs, who can maintain it, and how the public sector is moving off it.

One of three linked sites, each with one job: the [GitHub Repos Asset Catalogue](https://cyberdudeuk.github.io/github-repos-asset-catalogue/) shows code that exists (what you could reuse); this observatory shows what is old and risky (what you need to replace); a public sector tech hub with an app store, in development, will show what public bodies make and run (what you can adopt).

**Read it:** https://cyberdudeuk.github.io/legacy-technology-observatory/

Every figure links to a public source. Judgements are labelled *Analysis*, modelled figures *Estimate*, and weak or single-source claims *Unconfirmed*.

## What's inside

| Section | What it covers |
|---|---|
| Overview | Headline numbers, findings, what legacy costs by type of cost, legacy share by sector, risk matrix, and role-based starting points |
| Guide | Guided tour, readiness planner, tutorials, personas, journeys, user stories, scenarios, use cases, case studies, worked examples, user guide |
| Languages | 19 languages and platforms, from FORTRAN (1957) to TypeScript (2012): origin, purpose, talent pool, debt link, outlook |
| Beyond code | The whole legacy stack: networks (landlines, 2G/3G, PSN, Airwave), devices, medical and operational technology, practices and encryption, with the dates that matter |
| Systems and services | Named legacy systems across central government, devolved administrations, local government, the NHS and suppliers |
| Analytics | From evidence to decisions (investment, workforce, commercial, security, roadmaps, missions, inclusion), an adjustable priority tool with a copyable decision brief, roadmap horizons, and heatmaps of who works in technology (gender, ethnicity, disability, age), age profile, pay gaps, what is known per language, risk and key dates, plus organisations working to remove barriers |
| Skills and talent | Talent pool evidence, the link to technical debt, an age-inclusive approach, and skills needed by migration route |
| Migration | The 6 Rs, a step-by-step process, AI code translation evidence, decommissioning dates and outlook |
| Learning | What exists, gaps and options for training and keeping skills |
| Inclusion | Equality impacts, inclusive routes into skills, language guide and accessibility statement |
| Repo scan | Public government repositories by language, refreshed quarterly, with links into the GitHub Repos Asset Catalogue |
| Knowledge | Glossary, knowledge graph, data dictionary, taxonomy, related themes, open data |
| Documents | Theory of change, research, service blueprint, PRD, functional and technical requirements, architecture, HLD, LLD, ontology, traceability explorer |
| About | Method, the case against this work, self-checks, defect register, running costs, sources, contact |

## Repository layout

```
site/index.html            the whole site: one self-contained page
data/observatory.json      every record on the site, for reuse
data/repo-scan.json        latest repository scan (the site reads it when hosted here)
data/xref.json             shared keys for other portals (languages, layers, organisations)
tools/checks.py            static checks (each proved to fail on a bad sample)
tools/visual_qa.py         automated visual inspection of every section
tools/repo_scan.py         quarterly repository scan
tools/maintenance.py       monthly link and freshness check
tools/export_data.py       refreshes data/observatory.json and data/xref.json from the page
tests/                     unit tests, including negative tests for every check
docs/                      verification approach and defect register
```

## Automation

| Workflow | When | What it does |
|---|---|---|
| CI | Every pull request and push | Static checks, negative tests, then visual inspection at desktop and phone widths in light and dark themes with the drawer open and closed; screenshots attached |
| Publish site | Push to `main` | Runs the same checks and inspection, then publishes to GitHub Pages; a failed check blocks publishing |
| Quarterly repository scan | 1 Feb, May, Aug, Nov | Recounts repositories and opens a pull request with a comparison |
| Monthly maintenance | 3rd of each month | Checks every source link and whether the evidence is due for review; opens, updates or closes one issue |

All of these run on free GitHub-hosted runners for public repositories. Every third-party action is pinned to a commit.

## Keeping it running

About 3 to 5 hours a month for one person (estimate): review the quarterly scan pull request, act on the maintenance issue if it opens, read new audit reports, and answer issues.

One-off setting after the first push: **Settings > Pages > Build and deployment > Source: GitHub Actions**.

## Contact

Use the [contact form](https://github.com/cyberdudeuk/legacy-technology-observatory/issues/new?template=0-contact.yml). Corrections, new evidence and accessibility problems each have their own form. We never publish email addresses.

## Licence

Code is [MIT](LICENSE). Content and data are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Quoted sources keep their own licences.

An independent research aid. It is not an official statistic and does not represent the policy of any department.

## How to cite

Cite the archived release on Zenodo: Silva, E. *Legacy Technology Observatory*. Zenodo. [doi:10.5281/zenodo.24500735](https://doi.org/10.5281/zenodo.24500735). That DOI always points to the latest release; each release also has its own DOI. GitHub's **Cite this repository** button uses `CITATION.cff`.

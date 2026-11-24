# Legacy Code Observatory

Which programming languages and platforms run UK public services, who can still maintain them, how they drive technical debt, and how the public sector is moving off them.

**Read it:** https://cyberdudeuk.github.io/legacy-code-observatory/

Every figure links to a public source. Judgements are labelled *Analysis*, modelled figures *Estimate*, and weak or single-source claims *Unconfirmed*.

## What's inside

| Section | What it covers |
|---|---|
| Overview | Headline numbers, findings, legacy share by sector, risk matrix, and role-based starting points |
| Guide | Guided tour, readiness planner, tutorials, personas, journeys, user stories, scenarios, use cases, case studies, worked examples, user guide |
| Languages | 19 languages and platforms, from FORTRAN (1957) to TypeScript (2012): origin, purpose, talent pool, debt link, outlook |
| Systems and services | Named legacy systems across central government, devolved administrations, local government, the NHS and suppliers |
| Skills and talent | Talent pool evidence, the link to technical debt, an age-inclusive approach, and skills needed by migration route |
| Migration | The 6 Rs, a step-by-step process, AI code translation evidence, decommissioning dates and outlook |
| Learning | What exists, gaps and options for training and keeping skills |
| Inclusion | Equality impacts, inclusive routes into skills, language guide and accessibility statement |
| Repo scan | Public government repositories by language, refreshed quarterly |
| Knowledge | Glossary, knowledge graph, data dictionary, taxonomy, related themes, open data |
| Documents | Theory of change, research, service blueprint, PRD, functional and technical requirements, architecture, HLD, LLD, ontology, traceability explorer |
| About | Method, the case against this work, self-checks, defect register, running costs, sources, contact |

## Repository layout

```
site/index.html            the whole site: one self-contained page
data/observatory.json      every record on the site, for reuse
data/repo-scan.json        latest repository scan (the site reads it when hosted here)
tools/checks.py            static checks (each proved to fail on a bad sample)
tools/visual_qa.py         automated visual inspection of every section
tools/repo_scan.py         quarterly repository scan
tools/maintenance.py       monthly link and freshness check
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

Use the [contact form](https://github.com/cyberdudeuk/legacy-code-observatory/issues/new?template=0-contact.yml). Corrections, new evidence and accessibility problems each have their own form. We never publish email addresses.

## Licence

Code is [MIT](LICENSE). Content and data are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Quoted sources keep their own licences.

An independent research aid. It is not an official statistic and does not represent the policy of any department.

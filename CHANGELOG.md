# Changelog

## 3.1.0 — 24 November 2026
- New **Analytics** section: volumes at a glance and six heatmaps, each also an accessible table with a number in every cell.
- **Who works in technology**: representation of women, ethnic minority groups, Black women, disabled people and people aged 50 and over in UK IT jobs (BCS) and the civil service Digital and Data profession (Civil Service Statistics 2025), with a representation ratio.
- **Age profile and pay by age**: digital and data staff against the whole civil service; median age band 40 to 49 for both.
- **Pay gaps** by gender, ethnicity, disability and age, with their limits stated (civil service gaps are not adjusted for grade).
- **What is known for each language**: workforce demographics per programming language are shown as a visible data gap; no public source has them.
- **Organisations working to remove barriers**, filterable by barrier, including Coding Black Females, UKBlackTech, Code First Girls and Code Your Future.
- Defect D13 fixed: per-language system counts used a substring match ("platform" counted as PL/SQL). Check C19 now proves whole-word matching. New check C20 for organisation links.

## 3.0.0 — 24 November 2026
- Renamed the Legacy Code Observatory to the **Legacy Technology Observatory**: the scope now covers the whole legacy stack, not only code.
- New **Beyond code** section: the six-layer legacy stack, a register of 12 technologies (analogue landlines, 2G and 3G, PSN, Airwave, unsupported operating systems, medical technology, operational technology, NHS fax and pagers, pre-quantum encryption, mainframes, data centres) with the skills to replace each, and a table of the dates that matter.
- New **What legacy costs** section on the overview: 14 published figures across seven types of cost (savings missed, running premium, share of spend, keeping it alive, replacing it, incidents, skills). Figures are not added together because they overlap.
- Four new headline numbers, an eighth finding, 11 new glossary terms and new knowledge graph links.
- **Find and reuse code**: links from the repository scan into the GitHub Repos Asset Catalogue for every scanned organisation and for legacy code, reuse and code practice.
- `data/xref.json` publishes shared keys (languages, layers, organisations); `#language-cobol` and `#layer-pstn` open the matching record.
- Checks C17 and C18 with negative tests; the repository register check now covers beyond-code and cost records; visual inspection covers 13 sections.
- The public sector tech hub and app store will be a separate site; this one links to it once it is published.

## 2.2.0 — 24 November 2026
- Moved the Page contents switch into the drawer itself, with a slim rail that keeps it visible when the list is hidden.
- Compact phone header: search on its own row; Display and Ask as labelled icon buttons.
- Tapping outside or pressing Escape closes the contents list on phones.
- GitHub repository: issue forms for contact, corrections, new evidence and accessibility; CI with static checks, negative tests and automated visual inspection; publishing to GitHub Pages; quarterly repository scan; monthly link and freshness check.
- Contact form falls back to the GitHub issue form wherever the page cannot store messages.
- The repo scan chart reads the latest `data/repo-scan.json` when hosted here.
- Defects D10 to D12 recorded with their checks.

## 2.1.0 — 24 November 2026
- Guide: guided tour, readiness planner, tutorials, personas, journeys, user stories, scenarios, use cases, case studies, worked examples, user guide.
- Related themes, automatic glossary tooltips.
- Fixed sideways scrolling on phones (D8) and a check that could not fail (D9).

## 2.0.0 — 24 November 2026
- Coverage of Northern Ireland, Scotland, Wales, local government and the NHS.
- Start here by role, plain-English summaries, display settings, focus management, Inclusion section, accessibility statement.
- Document set with traceability explorer; 15 in-page self-checks with negative tests; defect register.

## 1.0.0 — 24 November 2026
- First release: languages, systems, skills, migration, learning, repo scan, knowledge layer, method and sources.

# How the observatory checks itself

Every release passes three layers of checks. Each check is proved to fail on a known-bad sample, so a check that cannot fail is caught.

## 1. In-page self-checks (20)

Run in the reader's browser every time the page loads, and shown on the About page with their negative tests.

| ID | Check |
|---|---|
| C1 | Every system and wider-sector record cites a known source |
| C2 | Every citation points to a listed source |
| C3 | Every source link is https or an in-page anchor |
| C4 | Every unsourced language record is labelled Unconfirmed or Analysis |
| C5 | No email addresses appear in the content |
| C6 | Retired organisation names do not appear |
| C7 | Every table row has as many cells as its header |
| C8 | Every button, link and form field has an accessible name |
| C9 | Text colours meet 4.5:1 contrast in light and dark themes |
| C10 | Every chart and diagram has a text title |
| C11 | Every page opens with a plain-English summary |
| C12 | Knowledge graph node types use distinct colours |
| C13 | Every requirement traces to a user need and to a check, unless planned |
| C14 | Headings do not skip levels |
| C15 | Every table keeps a minimum width so it scrolls instead of squeezing on phones |
| C16 | Nothing makes the page scroll sideways at the current width |
| C17 | Every record beyond code and every cost figure cites a known source and says what it measures |
| C18 | Every link to the GitHub Repos Asset Catalogue uses a key the catalogue publishes |
| C19 | Every heatmap has a caption and a number in every cell, every demographic and pay figure cites a known source, and language-to-system matching uses whole words |
| C20 | Every organisation listed has a secure link, a barrier and a description |

## 2. Repository checks (`tools/checks.py`, 11)

No email addresses, no retired names, https sources, known citations, cited registers (systems, devolved and local, beyond code, costs), labelled unsourced records, traced requirements, page size, pinned scripts from cdnjs only, no `eval`, valid JSON-LD. `tests/test_checks.py` runs each against the real site and a bad sample.

## 3. Visual inspection (`tools/visual_qa.py`)

Every section (14) at 1366px and 400px, in light and dark themes, with the contents drawer as loaded and toggled. Fails on any script error, any sideways scrolling, or any in-page self-check or negative test that does not behave. Screenshots are attached to each CI run.

A failure in any layer blocks publishing.

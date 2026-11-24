# Defect register

Every defect found, its root cause, the fix, and the check that stops it coming back. The same register is shown on the site's About page.

| ID | Defect | Root cause | Fix | Check that prevents a repeat |
|---|---|---|---|---|
| D1 | Risk matrix showed all ratings in one stray row | The cell builder returned bare labels without table cells | Wrapped each rating in a table cell | C7: every table row has as many cells as its header |
| D2 | Tables squeezed into unreadable columns on phones | Tables were set to 100% width with no minimum | Set a minimum table width inside a scrolling container | C15: every table keeps a minimum width of 640px |
| D3 | Knowledge graph used near-identical colours for languages and migration routes | Two amber tokens were assigned to different node types | Gave routes their own violet token | C12: every node type in the graph has a distinct colour |
| D4 | The content checks would have scanned their own test sample | Checks read the whole page, including scripts | Limited checks to the page's visible content | C5 and C6 negative tests confirm the sample is caught only when supplied |
| D5 | Secondary grey text fell below 4.5:1 contrast on the light theme | The light token was too pale on the grey background | Darkened the token; also darkened the light accent | C9: text tokens meet 4.5:1 in both themes |
| D6 | Grids of four cards left one card alone on a row | Auto-fit grids made three columns at desktop width | Used fixed two-column grids for sets of four | Covered by the visual inspection at every release |
| D7 | Card headings jumped two levels below their section heading | Card templates always used level 4 headings, even under level 2 section headings | Card headings now sit one level below their section heading | C14: headings do not skip levels |
| D8 | Pages scrolled sideways on phones | Screen-reader-only labels inside tables were positioned against the whole page, escaping their scrolling container | Made table, chart and tab containers the positioning context | C16: nothing makes the page scroll sideways at the current width |
| D9 | The table-width check could not fail | Its negative sample inherited the page-wide minimum width | Gave the sample an explicit zero minimum width | C15 negative test now fails as expected |
| D10 | A repository test hung for minutes | A 400,000-character padding in the shared bad sample made the email pattern scan quadratically | Moved the size test to its own sample and bounded the email pattern | Repository unit tests run in under a second; the size check keeps its own negative test |
| D11 | The contents switch sat in the masthead, away from the list it controls | It was placed with the search and tools | Moved the switch into the top of the drawer, with a slim rail that keeps it visible when the list is hidden | Visual inspection with the drawer open and closed, at desktop and phone widths |
| D12 | On phones the header took three rows and the open contents list could not be dismissed by tapping outside it | Header tools wrapped as one block; the overlay had no outside-tap handler | Search takes its own full-width row with Display and Ask beside the name; tapping outside or pressing Escape closes the list | Visual inspection at 400px with the list open and closed |

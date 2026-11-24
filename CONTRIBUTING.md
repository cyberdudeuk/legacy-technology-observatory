# Contributing

Thank you for helping keep the evidence accurate.

## Without code

Use an [issue form](https://github.com/cyberdudeuk/legacy-technology-observatory/issues/new/choose): report an error, suggest a system or source, or report an accessibility problem. Please include a public link for any fact, so it can be checked and cited.

## With code

1. Fork, branch and change `site/index.html` (data lives in the script near the top of the page).
2. If you change data, run the site and copy the new records into `data/observatory.json`, or describe the change in your pull request and the maintainer will do it.
3. Run the checks locally:
   ```
   python tools/checks.py
   python -m unittest discover -s tests
   pip install playwright==1.48.0 && python -m playwright install chromium
   python tools/visual_qa.py
   ```
4. Open a pull request. CI runs the same checks and the visual inspection.

## Rules every change follows

- Every figure cites a public source; judgements are labelled Analysis, modelled figures Estimate, weak claims Unconfirmed.
- No email addresses anywhere. Contact is by issue form only.
- Every defect fixed gets a check that would have caught it, with a negative test, and an entry in `docs/defect-register.md`.
- Plain English, following the language guide on the Inclusion page.
- WCAG 2.2 AA: keyboard use, contrast, text alternatives for every chart.

By contributing you agree your contribution is licensed as described in the [LICENSE](LICENSE), and to follow the [code of conduct](CODE_OF_CONDUCT.md).

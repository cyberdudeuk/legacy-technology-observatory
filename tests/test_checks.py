"""Every check must pass on the real site and fail on a known-bad sample."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import checks  # noqa: E402

BAD_HTML = """<html><head><script src="https://example.com/lib@latest.js"></script></head>
<body><p>Write to someone@example.gov.uk at the Office of the Chief Data Officer</p>
<script>eval("1")</script></body></html>"""

BAD_DATA = {
    "sources": {"S1": {"title": "x", "url": "http://insecure.example"}},
    "systems": [{"n": "No source", "s": []}],
    "devolved_and_local": [{"n": "Unknown source", "s": ["S999"]}],
    "languages": [{"n": "Unlabelled", "s": [], "ev": "sourced"}],
    "user_needs": [["N1", "x", "y", "z"]],
    "requirements": [["R1", "x", ["N9"], "f", [], [], "Done"]],
    "note": "contact: person@example.org",
}


class RealSitePasses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = checks.SITE.read_text(encoding="utf-8")
        cls.data = json.loads(checks.DATA.read_text(encoding="utf-8"))

    def test_every_check_passes(self):
        for name, problems in checks.run(self.html, self.data).items():
            with self.subTest(check=name):
                self.assertEqual(problems, [], f"{name}: {problems}")


class BadSampleFails(unittest.TestCase):
    def test_every_check_fails_on_bad_sample(self):
        results = checks.run(BAD_HTML, BAD_DATA)
        for name, problems in results.items():
            if name in ("check_json_ld", "check_size"):
                continue  # covered separately below
            with self.subTest(check=name):
                self.assertTrue(problems, f"{name} did not fail on the bad sample")

    def test_size_fails_when_too_big(self):
        # Kept separate: padding the shared sample made the email pattern scan quadratic (defect D10)
        self.assertTrue(checks.check_size("x" * (checks.MAX_BYTES + 1), {}))

    def test_json_ld_fails_when_missing_or_broken(self):
        self.assertTrue(checks.check_json_ld("<p>none</p>", {}))
        self.assertTrue(checks.check_json_ld('<script type="application/ld+json">{bad</script>', {}))


if __name__ == "__main__":
    unittest.main()

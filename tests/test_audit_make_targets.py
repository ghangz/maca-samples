import tempfile
import unittest
from pathlib import Path

from tools.audit_make_targets import audit


class AuditMakeTargetsTest(unittest.TestCase):
    def test_supports_spaces_before_colon_and_ignores_assignment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sample = root / "sample"
            sample.mkdir()
            (sample / "Makefile").write_text(
                "VAR:=value\n"
                "all :\n"
                "\t@true\n"
                "run:\n"
                "\t@true\n"
                "clean:\n"
                "\t@true\n",
                encoding="utf-8",
            )

            report = audit(root)

        self.assertEqual(report["failed_count"], 0)
        self.assertEqual(report["results"][0]["targets"], ["all", "clean", "run"])


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path

from tools.summarize_validation_logs import summarize


class SummarizeValidationLogsTest(unittest.TestCase):
    def test_marks_invalid_json_as_failed_record(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            (log_dir / "ok.json").write_text('{"sample":"vectorAdd","success":true}', encoding="utf-8")
            (log_dir / "bad.json").write_text("{not-json", encoding="utf-8")

            report = summarize(log_dir)

        self.assertEqual(report["log_count"], 2)
        self.assertEqual(report["passed"], 1)
        self.assertEqual(report["failed"], 1)
        failed = next(item for item in report["logs"] if item["path"] == "bad.json")
        self.assertIn("error", failed)


if __name__ == "__main__":
    unittest.main()

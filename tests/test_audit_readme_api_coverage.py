import tempfile
import unittest
from pathlib import Path

from tools.audit_readme_api_coverage import audit


class AuditReadmeApiCoverageTest(unittest.TestCase):
    def test_matches_documented_apis_exactly(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sample = root / "sample"
            sample.mkdir()
            (sample / "Makefile").write_text("all:\n", encoding="utf-8")
            (sample / "kernel.cpp").write_text("mcMalloc();\n", encoding="utf-8")
            (sample / "README.md").write_text("This sample uses mcMallocAsync.\n", encoding="utf-8")

            report = audit(root)

        self.assertEqual(report["sample_count"], 1)
        self.assertEqual(report["results"][0]["used_apis"], ["mcMalloc"])
        self.assertEqual(report["results"][0]["missing_from_readme"], ["mcMalloc"])

    def test_scans_cuda_and_header_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sample = root / "sample"
            sample.mkdir()
            (sample / "Makefile").write_text("all:\n", encoding="utf-8")
            (sample / "kernel.cu").write_text("mcMemcpy();\n", encoding="utf-8")
            (sample / "kernel.hpp").write_text("mcStreamCreate();\n", encoding="utf-8")
            (sample / "README.md").write_text("mcMemcpy mcStreamCreate\n", encoding="utf-8")

            report = audit(root)

        self.assertEqual(report["results"][0]["missing_from_readme"], [])


if __name__ == "__main__":
    unittest.main()

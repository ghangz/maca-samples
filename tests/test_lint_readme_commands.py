import tempfile
import unittest
from pathlib import Path

from tools.lint_readme_commands import extract_commands, lint


class LintReadmeCommandsTest(unittest.TestCase):
    def test_extract_commands_requires_shell_fence_and_joins_line_continuations(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            readme = Path(tmpdir) / "README.md"
            readme.write_text(
                "```cmake\n"
                "make run\n"
                "```\n"
                "```bash\n"
                "$ make \\\n"
                "  run\n"
                "```\n",
                encoding="utf-8",
            )

            commands = extract_commands(readme)

        self.assertEqual(commands, ["make run"])

    def test_lint_skips_hidden_and_build_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sample = root / "sample"
            sample.mkdir()
            (sample / "Makefile").write_text("all:\n", encoding="utf-8")
            (sample / "README.md").write_text("```bash\n$ make\n$ make run\n```\n", encoding="utf-8")
            build_dir = root / "build" / "generated"
            build_dir.mkdir(parents=True)
            (build_dir / "Makefile").write_text("all:\n", encoding="utf-8")

            results = lint(root)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["path"], "sample")


if __name__ == "__main__":
    unittest.main()

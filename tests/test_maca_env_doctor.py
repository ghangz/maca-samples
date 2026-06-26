import os
import tempfile
import unittest

from tools.maca_env_doctor import inspect_maca_home


class MacaEnvDoctorTests(unittest.TestCase):
    def test_inspect_maca_home_requires_env(self):
        result = inspect_maca_home("")
        self.assertFalse(result.ok)

    def test_inspect_maca_home_checks_expected_dirs(self):
        with tempfile.TemporaryDirectory() as directory:
            os.makedirs(os.path.join(directory, "bin"))
            os.makedirs(os.path.join(directory, "include"))
            result = inspect_maca_home(directory)
            self.assertFalse(result.ok)
            self.assertIn("lib/lib64", result.detail)

    def test_inspect_maca_home_passes_when_layout_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            for child in ("bin", "include", "lib"):
                os.makedirs(os.path.join(directory, child))
            result = inspect_maca_home(directory)
            self.assertTrue(result.ok)

    def test_inspect_maca_home_accepts_lib64_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            for child in ("bin", "include", "lib64"):
                os.makedirs(os.path.join(directory, child))
            result = inspect_maca_home(directory)
            self.assertTrue(result.ok)


if __name__ == "__main__":
    unittest.main()

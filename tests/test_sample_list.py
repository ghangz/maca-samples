import os
import tempfile
import unittest

from tools.sample_list import collect_samples, detect_build_system


class SampleListTests(unittest.TestCase):
    def test_detect_build_system(self):
        self.assertEqual(detect_build_system(["CMakeLists.txt"]), "cmake")
        self.assertEqual(detect_build_system(["Makefile"]), "make")
        self.assertEqual(detect_build_system(["README.md"]), "unknown")

    def test_collect_samples_finds_sample_dirs(self):
        with tempfile.TemporaryDirectory() as directory:
            sample_dir = os.path.join(directory, "0_Introduction", "vectorAdd")
            os.makedirs(sample_dir)
            with open(os.path.join(sample_dir, "Makefile"), "w", encoding="utf-8") as handle:
                handle.write("all:\n")
            with open(os.path.join(sample_dir, "README.md"), "w", encoding="utf-8") as handle:
                handle.write("# sample\n")

            samples = collect_samples(directory)

        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0]["category"], "0_Introduction")
        self.assertEqual(samples[0]["build_system"], "make")


if __name__ == "__main__":
    unittest.main()

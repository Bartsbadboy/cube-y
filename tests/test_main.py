import io
import tempfile
import unittest
from pathlib import Path

from main import FOUND, IMPOSSIBLE, REFUSED, main


class Main(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.file = Path(self.dir.name) / "solution.txt"
        self.out = io.StringIO()

    def tearDown(self):
        self.dir.cleanup()

    def test_rectangle_is_found_judged_and_saved(self):
        code = main(["--box", "10x5x1", "--out", str(self.file)], self.out)
        self.assertEqual(code, FOUND)
        self.assertIn("Le juge valide.", self.out.getvalue())
        self.assertTrue(self.file.read_text(encoding="utf-8").startswith("Couche 1"))

    def test_square_is_impossible_and_nothing_is_saved(self):
        code = main(["--box", "5x5x1", "--out", str(self.file)], self.out)
        self.assertEqual(code, IMPOSSIBLE)
        self.assertFalse(self.file.exists())

    def test_progress_lines(self):
        main(["--box", "10x5x1", "--out", str(self.file), "--every", "50"], self.out)
        self.assertGreaterEqual(self.out.getvalue().count("posées"), 3)

    def test_a_saved_solution_is_judged_again(self):
        main(["--box", "10x5x1", "--out", str(self.file)], io.StringIO())
        code = main(["--box", "10x5x1", "--check", str(self.file)], self.out)
        self.assertEqual(code, FOUND)

    def test_a_tampered_solution_is_refused(self):
        main(["--box", "10x5x1", "--out", str(self.file)], io.StringIO())
        text = self.file.read_text(encoding="utf-8").replace("01 02", "02 02", 1)
        self.file.write_text(text, encoding="utf-8")
        code = main(["--box", "10x5x1", "--check", str(self.file)], self.out)
        self.assertEqual(code, REFUSED)
        self.assertIn("Le juge refuse", self.out.getvalue())


if __name__ == "__main__":
    unittest.main()

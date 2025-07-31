import unittest
from pathlib import Path
from nelox.parser import Parser
from nelox.scanner import Scanner

class TestGenerated(unittest.TestCase):
    def test_all_cases(self):
        base = Path(__file__).resolve().parent.parent
        folder = base / "dataset_generator" / "dataset"
        for test_file in folder.glob("*.txt"):
            with self.subTest(testcase=test_file.name):
                with test_file.open(encoding="utf-8") as f:
                    src = f.read()
                parser = Parser(Scanner(src))
                try:
                    parser.parse()
                except Exception as e:
                    self.fail(f"Parser failed on {test_file.name}: {e}")

if __name__ == "__main__":
    unittest.main()

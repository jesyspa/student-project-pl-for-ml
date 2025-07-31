import unittest
from pathlib import Path
from nelox.scanner import Scanner
from nelox.parser import Parser
from nelox.interpreter import Interpreter

class TestGenerated(unittest.TestCase):
    def test_all_cases(self):
        base = Path(__file__).resolve().parent.parent
        folder = base / "dataset_generator" / "dataset"
        for test_file in folder.glob("*.txt"):
            with self.subTest(testcase=test_file.name):
                with test_file.open(encoding="utf-8") as f:
                    src = f.read()

                scanner = Scanner(src)
                parser = Parser(scanner)
                expressions = parser.parse()

                try:
                    interpreter = Interpreter()
                    interpreter.interpret(expressions)
                except Exception as e:
                    self.fail(f"Failed to interpret {test_file.name}: {e}")

if __name__ == "__main__":
    unittest.main()

import unittest, os
from nelox.parser import Parser
from nelox.scanner import Scanner

class TestHandwrittenExamples(unittest.TestCase):
    def test_all_cases(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder = os.path.join(base, "dataset")
        for test in os.listdir(folder):
            if test.endswith(".txt"):
                path = os.path.join(folder, test)
            with self.subTest(testcase=test):
                with open(path, "r", encoding="utf-8") as f:
                    src = f.read()
                parser = Parser(Scanner(src))
                parser.parse()  # as no interpreter is present

if __name__ == "__main__":
    unittest.main()

import unittest, os
from nelox.parser import Parser
from nelox.scanner import Scanner

class TestHandWritten(unittest.TestCase):
    base = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "dataset", "handwritten"
    )

    def running(self, filename):
        path = os.path.join(self.base, filename)
        with open(path, "r") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        parser.parse()

    def test_all_cases(self):
        for i in range(1, 13):
            with self.subTest(testcase=f"testcase{i}"):
                self.running(f"testcase{i}.txt")


if __name__ == "__main__":
    unittest.main()

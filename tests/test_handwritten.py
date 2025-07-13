import unittest, os
from nelox.parser import Parser
from nelox.scanner import Scanner

class TestHandWritten(unittest.TestCase):
    def test_case1(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase1.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case2(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase2.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case3(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase3.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case4(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase4.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case5(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase5.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case6(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase6.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case7(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase7.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case8(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase8.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case9(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase9.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case10(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase10.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case11(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase11.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)

    def test_case12(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "dataset", "handwritten", "testcase12.txt")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        parser = Parser(Scanner(src))
        self.assertIsInstance(parser.parse(), list)


if __name__ == "__main__":
    unittest.main()

import unittest
import io
import sys
import os
from nelox.scanner import Scanner
from nelox.parser import Parser
from nelox.interpreter import Interpreter


class InterpreterTest(unittest.TestCase):
    def run_code(self, source):
        scanner = Scanner(source)
        parser = Parser(scanner)
        expressions = parser.parse()
        interpreter = Interpreter()
        return interpreter.interpret(expressions)

    def run_case(self, case_name):
        base_path = os.path.join(os.path.dirname(__file__), "cases", case_name)

        with open(base_path + ".code") as f:
            code = f.read()
        with open(base_path + ".input", "r") as f:
            input_data = f.read()
        with open(base_path + ".output", "r") as f:
            expected_output = f.read().strip()

        original_stdin = sys.stdin
        original_stdout = sys.stdout
        sys.stdin = io.StringIO(input_data)
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.run_code(code)
            result = captured_output.getvalue().strip()
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

        self.assertEqual(result, expected_output)

    def test_problem1(self): self.run_case("problem1")
    def test_problem2(self): self.run_case("problem2")
    def test_problem3(self): self.run_case("problem3")
    def test_problem4(self): self.run_case("problem4")
    def test_problem5(self): self.run_case("problem5")
    def test_problem6(self): self.run_case("problem6")
    def test_problem7(self): self.run_case("problem7")
    def test_problem8(self): self.run_case("problem8")
    def test_problem9(self): self.run_case("problem9")
    def test_problem10(self): self.run_case("problem10")
    def test_problem0(self): self.run_case("problem0")


if __name__ == "__main__":
    unittest.main()

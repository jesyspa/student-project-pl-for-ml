import unittest
from nelox.scanner import Scanner
from nelox.parser import Parser
from nelox.interpreter import Interpreter
from dataset_generator.fuzzer import Fuzzer

class TestGenerated(unittest.TestCase):
    def setUp(self):
        self.fuzzer = Fuzzer()

    def test_pretty_parse_roundtrip(self):
        for _ in range(self.fuzzer.num_samples):
            program_str = self.fuzzer.generate_program()
            scanner = Scanner(program_str)
            parser = Parser(scanner)
            try:
                parser.parse()
            except Exception:
                self.fail(f"Parser failed: {program_str}")

    def test_generated_programs_execute(self):
        for _ in range(50):
            program_str = self.fuzzer.generate_program()
            scanner = Scanner(program_str)
            parser = Parser(scanner)
            expressions = parser.parse()
            try:
                Interpreter().interpret(expressions)
            except Exception:
                self.fail(f"Interpreter failed: {program_str}")

if __name__ == "__main__":
    unittest.main()

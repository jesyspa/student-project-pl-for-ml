import unittest

from nelox.pretty_printer import pretty_program
from nelox.scanner import Scanner
from nelox.parser import Parser
from nelox.interpreter import Interpreter
from dataset_generator.Fuzzer import Fuzzer

class TestGenerated(unittest.TestCase):
    def setUp(self):
        self.fuzzer = Fuzzer()

    def test_pretty_parse_roundtrip(self):
        for _ in range(5):
            program = self.fuzzer.generate_program()
            program_str = pretty_program(program)
            scanner = Scanner(program_str)
            parser = Parser(scanner)
            try:
                parser.parse()
            except Exception:
                self.fail(f"Parser failed: {program_str}")

    def test_generated_programs_execute(self):
        for _ in range(5):
            self.fuzzer.env.reset()
            program = self.fuzzer.generate_program()
            try:
                Interpreter().interpret(program)
            except Exception:
                program_str = pretty_program(program)
                self.fail(f"Interpreter failed:\n{program_str}")

if __name__ == "__main__":
    unittest.main()

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
        for _ in range(500):
            program = self.fuzzer.generate_program()
            program_str = pretty_program(program)
            with self.subTest(program=program_str):
                scanner = Scanner(program_str)
                parser = Parser(scanner)
                parser.parse()

    def test_generated_programs_execute(self):
        for _ in range(500):
            self.fuzzer.env.reset()
            program = self.fuzzer.generate_program()
            program_str = pretty_program(program)
            with self.subTest(program=program_str):
                Interpreter().interpret(program)

if __name__ == "__main__":
    unittest.main()

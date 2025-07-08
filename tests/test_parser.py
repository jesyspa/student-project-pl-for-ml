import unittest
from nelox.parser import Parser
from nelox.scanner import Scanner


class ParserTest(unittest.TestCase):

    def test_simple_addition(self):
        source = "(+ 1 2)"
        scanner = Scanner(source)
        parser = Parser(scanner)
        exprs = parser.parse()

        self.assertEqual(len(exprs), 1)
        expr = exprs[0]

        self.assertIsInstance(expr, list)
        self.assertEqual(expr[0], '+')
        self.assertEqual(expr[1], 1)
        self.assertEqual(expr[2], 2)

    def test_define_variable(self):
        source = "(define x 42)"
        scanner = Scanner(source)
        parser = Parser(scanner)
        exprs = parser.parse()

        self.assertEqual(len(exprs), 1)
        expr = exprs[0]

        self.assertIsInstance(expr, list)
        self.assertEqual(expr[0], 'define')
        self.assertEqual(expr[1], 'x')
        self.assertEqual(expr[2], 42)

    def test_nested_lists(self):
        source = "(+ 1 (* 2 3))"
        scanner = Scanner(source)
        parser = Parser(scanner)
        exprs = parser.parse()

        self.assertEqual(len(exprs), 1)
        expr = exprs[0]

        self.assertIsInstance(expr, list)
        self.assertEqual(expr[0], '+')
        self.assertEqual(expr[1], 1)
        self.assertIsInstance(expr[2], list)
        self.assertEqual(expr[2][0], '*')
        self.assertEqual(expr[2][1], 2)
        self.assertEqual(expr[2][2], 3)

    def test_multiple_lists(self):
        source = "(+ 1 2) (define x 42)"
        scanner = Scanner(source)
        parser = Parser(scanner)
        exprs = parser.parse()

        self.assertEqual(len(exprs), 2)

        first = exprs[0]
        self.assertIsInstance(first, list)
        self.assertEqual(first[0], '+')
        self.assertEqual(first[1], 1)
        self.assertEqual(first[2], 2)

        second = exprs[1]
        self.assertIsInstance(second, list)
        self.assertEqual(second[0], 'define')
        self.assertEqual(second[1], 'x')
        self.assertEqual(second[2], 42)


if __name__ == '__main__':
    unittest.main()

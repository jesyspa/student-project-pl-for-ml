import unittest
from nelox.parser import Parser
from nelox.scanner import Scanner
from nelox.token_type import TokenType
from nelox.Expr import Variable, Literal, ListExpr


class ParserTest(unittest.TestCase):

    def test_simple_addition(self):
        source = "(+ 1 2)"
        scanner = Scanner(source)
        parser = Parser(scanner)
        exprs = parser.parse()

        self.assertEqual(len(exprs), 1)
        expr = exprs[0]

        self.assertIsInstance(expr, ListExpr)
        self.assertIsInstance(expr.elements[0], Variable)
        self.assertEqual(expr.elements[0].name.lexeme, '+')
        self.assertIsInstance(expr.elements[1], Literal)
        self.assertEqual(expr.elements[1].value, 1)
        self.assertIsInstance(expr.elements[2], Literal)
        self.assertEqual(expr.elements[2].value, 2)

    def test_define_variable(self):
        source = "(define x 42)"
        scanner = Scanner(source)
        parser = Parser(scanner)
        exprs = parser.parse()

        self.assertEqual(len(exprs), 1)
        expr = exprs[0]

        self.assertIsInstance(expr, ListExpr)
        self.assertIsInstance(expr.elements[0], Variable)
        self.assertEqual(expr.elements[0].name.lexeme, 'define')
        self.assertIsInstance(expr.elements[1], Variable)
        self.assertEqual(expr.elements[1].name.lexeme, 'x')
        self.assertIsInstance(expr.elements[2], Literal)
        self.assertEqual(expr.elements[2].value, 42)

    def test_nested_lists(self):
        source = "(+ 1 (* 2 3))"
        scanner = Scanner(source)
        parser = Parser(scanner)
        exprs = parser.parse()

        self.assertEqual(len(exprs), 1)
        expr = exprs[0]

        self.assertIsInstance(expr, ListExpr)
        self.assertIsInstance(expr.elements[0], Variable)
        self.assertEqual(expr.elements[0].name.lexeme, '+')
        self.assertIsInstance(expr.elements[1], Literal)
        self.assertEqual(expr.elements[1].value, 1)

        inner = expr.elements[2]
        self.assertIsInstance(inner, ListExpr)
        self.assertIsInstance(inner.elements[0], Variable)
        self.assertEqual(inner.elements[0].name.lexeme, '*')
        self.assertIsInstance(inner.elements[1], Literal)
        self.assertEqual(inner.elements[1].value, 2)
        self.assertIsInstance(inner.elements[2], Literal)
        self.assertEqual(inner.elements[2].value, 3)

    def test_multiple_lists(self):
        source = "(+ 1 2) (define x 42)"
        scanner = Scanner(source)
        parser = Parser(scanner)
        exprs = parser.parse()

        self.assertEqual(len(exprs), 2)

        first = exprs[0]
        self.assertIsInstance(first.elements[0], Variable)
        self.assertEqual(first.elements[0].name.lexeme, '+')
        self.assertEqual(first.elements[1].value, 1)
        self.assertEqual(first.elements[2].value, 2)

        second = exprs[1]
        self.assertIsInstance(second.elements[0], Variable)
        self.assertEqual(second.elements[0].name.lexeme, 'define')
        self.assertIsInstance(second.elements[1], Variable)
        self.assertEqual(second.elements[1].name.lexeme, 'x')
        self.assertIsInstance(second.elements[2], Literal)
        self.assertEqual(second.elements[2].value, 42)

    def test_string_literal(self):
        source = '"hello world"'
        scanner = Scanner(source)
        parser = Parser(scanner)
        result = parser.parse()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Literal)
        self.assertEqual(result[0].value, "hello world")

    def test_peek_after_scan(self):
        scanner = Scanner("(foo 123)")
        scanner.scan_tokens()

        token = scanner.peek()
        self.assertEqual(token.type, TokenType.LEFT_PAREN)

        token_again = scanner.peek()
        self.assertEqual(token_again.type, TokenType.LEFT_PAREN)

    def test_advance_progresses_through_tokens(self):
        scanner = Scanner("(foo 123)")
        scanner.scan_tokens()

        types = []
        while not scanner.is_at_end():
            token = scanner.advance()
            types.append(token.type)

        self.assertEqual(
            types,
            [
                TokenType.LEFT_PAREN,
                TokenType.IDENTIFIER,
                TokenType.NUMBER,
                TokenType.RIGHT_PAREN
            ]
        )


if __name__ == '__main__':
    unittest.main()

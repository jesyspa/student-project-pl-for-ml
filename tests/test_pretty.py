import unittest
from nelox.pretty_printer import pretty
from nelox.Expr import Literal, Variable, List
from nelox.token_type import TokenType
from nelox.nelox_token import Token

def make_token(type_, lexeme):
    return Token(type_, lexeme, None, 0)

class PrettyPrinterTest(unittest.TestCase):
    def test_literal(self):
        self.assertEqual(pretty(Literal(42)), "42")

    def test_variable(self):
        token = make_token(TokenType.IDENTIFIER, "x")
        self.assertEqual(pretty(Variable(token)), "x")

    def test_list(self):
        token_plus = make_token(TokenType.IDENTIFIER, "+")
        token_x = make_token(TokenType.IDENTIFIER, "x")
        expr = List([
            Variable(token_plus),
            Variable(token_x),
            Literal(5)
        ])
        self.assertEqual(pretty(expr), "(+ x 5)")

if __name__ == "__main__":
    unittest.main()

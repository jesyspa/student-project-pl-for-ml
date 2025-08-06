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

    def test_nested_expression(self):
        plus = Variable(make_token(TokenType.IDENTIFIER, "+"))
        mult = Variable(make_token(TokenType.IDENTIFIER, "*"))
        x = Variable(make_token(TokenType.IDENTIFIER, "x"))

        inner = List([mult, x, Literal(3)])
        outer = List([plus, Literal(1), inner])

        self.assertEqual(pretty(outer), "(+ 1 (* x 3))")

    def test_function_expression(self):
        func_token = make_token(TokenType.IDENTIFIER, "func")
        name_token = make_token(TokenType.IDENTIFIER, "f")
        arg_token = make_token(TokenType.IDENTIFIER, "x")
        print_token = make_token(TokenType.IDENTIFIER, "print")

        body1 = List([
            Variable(print_token),
            Variable(arg_token)
        ])
        body2 = List([
            Variable(print_token),
            Literal(99)
        ])
        func_expr = List([
            Variable(func_token),
            Variable(name_token),
            List([Variable(arg_token)]),
            body1,
            body2
        ])
        exp = (
            "(func f (x)\n"
            "   (print x)\n"
            "   (print 99))"
        )
        self.assertEqual(pretty(func_expr), exp)


if __name__ == "__main__":
    unittest.main()

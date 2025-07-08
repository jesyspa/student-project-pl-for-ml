import unittest
from nelox.Expr import Literal, Variable, Binary, Unary, Assign, If, Call
from nelox.ast_printer import AstPrinter
from nelox.token_type import TokenType
from nelox.nelox_token import Token


class DummyOperator:
    def __init__(self, lexeme):
        self.lexeme = lexeme


class AstPrinterTest(unittest.TestCase):

    def setUp(self):
        self.printer = AstPrinter()

    def test_literal(self):
        lit = Literal(42)
        self.assertEqual(self.printer.visit_literal_expr(lit), "42")

    def test_variable(self):
        var = Variable(Token(TokenType.IDENTIFIER, "x", None, 1))
        self.assertEqual(self.printer.visit_variable_expr(var), "x")

    def test_binary(self):
        expr = Binary(
            left=Literal(1),
            operator=DummyOperator("+"),
            right=Literal(2)
        )
        expected = "( + 1 2 )"
        self.assertEqual(self.printer.visit_binary_expr(expr), expected)

    def test_unary(self):
        expr = Unary(
            operator=DummyOperator("-"),
            right=Literal(3)
        )
        expected = "( - 3 )"
        self.assertEqual(self.printer.visit_unary_expr(expr), expected)

    def test_assign(self):
        assign = Assign(
            name=Variable(Token(TokenType.IDENTIFIER, "a", None, 1)),
            value=Literal(10)
        )
        expected = "( = a 10 )"
        self.assertEqual(self.printer.visit_assign_expr(assign), expected)

    def test_if(self):
        if_stmt = If(
            condition=Variable(Token(TokenType.IDENTIFIER, "cond", None, 1)),
            then_branch=Literal("then_branch"),
            else_branch=Literal("else_branch")
        )
        expected = "( if-else cond then_branch else_branch )"
        self.assertEqual(self.printer.visit_if_stmt(if_stmt), expected)

    def test_call(self):
        call = Call(
            callee=Variable(Token(TokenType.IDENTIFIER, "func", None, 1)),
            paren=None,
            arguments=[Literal(1), Literal(2)]
        )
        expected = "( call func 1 2 )"
        self.assertEqual(self.printer.visit_call_expr(call), expected)


if __name__ == "__main__":
    unittest.main()

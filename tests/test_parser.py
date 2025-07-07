import unittest
from nelox.token_type import TokenType
from nelox.nelox_token import Token
from nelox.parser import Parser
from nelox.Expr import Binary, Literal, Variable, Assign


class ParserTest(unittest.TestCase):

    def test_simple_addition(self):
        tokens = [
            Token(TokenType.LEFT_PAREN, '(', None, 1),
            Token(TokenType.IDENTIFIER, '+', None, 1),
            Token(TokenType.NUMBER, '1', 1, 1),
            Token(TokenType.NUMBER, '2', 2, 1),
            Token(TokenType.RIGHT_PAREN, ')', None, 1),
            Token(TokenType.EOF, '', None, 1)
        ]
        parser = Parser(tokens)
        exprs = parser.parse()

        self.assertEqual(len(exprs), 1)
        self.assertIsInstance(exprs[0], Binary)
        self.assertIsInstance(exprs[0].left, Literal)
        self.assertEqual(exprs[0].left.value, 1)
        self.assertEqual(exprs[0].operator.lexeme, '+')
        self.assertIsInstance(exprs[0].right, Literal)
        self.assertEqual(exprs[0].right.value, 2)

    def test_define_variable(self):
        tokens = [
            Token(TokenType.LEFT_PAREN, '(', None, 1),
            Token(TokenType.IDENTIFIER, 'define', None, 1),
            Token(TokenType.IDENTIFIER, 'x', None, 1),
            Token(TokenType.NUMBER, '42', 42, 1),
            Token(TokenType.RIGHT_PAREN, ')', None, 1),
            Token(TokenType.EOF, '', None, 1)
        ]
        parser = Parser(tokens)
        exprs = parser.parse()

        self.assertEqual(len(exprs), 1)
        self.assertIsInstance(exprs[0], Assign)
        self.assertIsInstance(exprs[0].name, Variable)
        self.assertEqual(exprs[0].name.name.lexeme, 'x')
        self.assertIsInstance(exprs[0].value, Literal)
        self.assertEqual(exprs[0].value.value, 42)


if __name__ == '__main__':
    unittest.main()

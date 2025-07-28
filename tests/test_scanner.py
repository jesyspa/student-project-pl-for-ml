import unittest
from nelox.scanner import Scanner, scan_all_tokens
from nelox.token_type import TokenType


class TestScanner(unittest.TestCase):
    def test_single_parentheses(self):
        scanner = Scanner("()")
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0].type, TokenType.LEFT_PAREN)
        self.assertEqual(tokens[1].type, TokenType.RIGHT_PAREN)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_number_token(self):
        scanner = Scanner("123")
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].literal, 123.0)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_unterminated_string(self):
        source = '"hello world'
        scanner = Scanner(source)
        with self.assertRaises(SyntaxError):
            scanner.scan_tokens()

    def test_simple_expression(self):
        scanner = Scanner("(add 2 3)")
        types = [t.type for t in scanner.scan_tokens()]

        expected = [
            TokenType.LEFT_PAREN,
            TokenType.IDENTIFIER,
            TokenType.NUMBER,
            TokenType.NUMBER,
            TokenType.RIGHT_PAREN,
            TokenType.EOF
        ]
        self.assertEqual(types, expected)

    def test_next_token_number(self):
        scanner = Scanner("42")
        token = scanner.next_token()

        self.assertEqual(token.type, TokenType.NUMBER)
        self.assertEqual(token.literal, 42)
        self.assertEqual(token.lexeme, "42")

    def test_next_token_identifier(self):
        scanner = Scanner("hello")
        token = scanner.next_token()

        self.assertEqual(token.type, TokenType.IDENTIFIER)
        self.assertEqual(token.lexeme, "hello")

    def test_next_token_left_paren(self):
        scanner = Scanner("(")
        token = scanner.next_token()

        self.assertEqual(token.type, TokenType.LEFT_PAREN)
        self.assertEqual(token.lexeme, "(")

    def test_next_token_string(self):
        scanner = Scanner('"world"')
        token = scanner.next_token()

        self.assertEqual(token.type, TokenType.STRING)
        self.assertEqual(token.literal, "world")
        self.assertEqual(token.lexeme, '"world"')

    def test_multiple_next_token_calls(self):
        scanner = Scanner("(foo 123)")
        tokens = scanner.scan_tokens()

        expected_types = [
            TokenType.LEFT_PAREN,
            TokenType.IDENTIFIER,
            TokenType.NUMBER,
            TokenType.RIGHT_PAREN,
            TokenType.EOF
        ]

        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)

    def test_line_numbers(self):

        source = '(print\n 42\n "hello")'
        tokens = scan_all_tokens(source)

        assert tokens[0].type == TokenType.LEFT_PAREN
        assert tokens[0].line == 1

        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].line == 1

        assert tokens[2].type == TokenType.NUMBER
        assert tokens[2].line == 2

        assert tokens[3].type == TokenType.STRING
        assert tokens[3].line == 3

        assert tokens[4].type == TokenType.RIGHT_PAREN
        assert tokens[4].line == 3

        assert tokens[5].type == TokenType.EOF

    def test_sign(self):
        source = '(!= 2 3)'
        tokens = scan_all_tokens(source)

        expected_types = [
            TokenType.LEFT_PAREN,
            TokenType.IDENTIFIER,
            TokenType.NUMBER,
            TokenType.NUMBER,
            TokenType.RIGHT_PAREN,
            TokenType.EOF
        ]

        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)


if __name__ == '__main__':
    unittest.main()

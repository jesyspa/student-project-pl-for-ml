from typing import List

from .nelox_token import Token
from .token_type import TokenType


def is_alpha_numeric(c):
    return is_alpha(c) or is_digit(c)


def is_alpha(c):
    return c.isalpha() or c == '_'


def is_digit(c):
    return '0' <= c <= '9'


class Scanner:

    def __init__(self, source: str):
        self.source: str = source
        self.tokens: List[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            token = self.next_token()
            if token:
                self.tokens.append(token)

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        if c == '\n':
            self.line += 1
        return c

    def make_token(self, type: TokenType, literal=None) -> Token:
        text = self.source[self.start:self.current]
        return Token(type, text, literal, self.line)

    def next_token(self) -> Token | None:
        while True:
            if self.is_at_end():
                return self.make_token(TokenType.EOF)

            self.start = self.current
            c = self.advance()

            if c == '(':
                return self.make_token(TokenType.LEFT_PAREN)
            elif c == ')':
                return self.make_token(TokenType.RIGHT_PAREN)
            elif c.isdigit():
                return self.number()
            elif is_alpha(c):
                return self.identifier()
            elif c == '"':
                return self.string()
            elif c in (' ', '\r', '\t'):
                continue
            elif c == '\n':
                continue
            else:
                raise SyntaxError(f"[line {self.line}] Unexpected character: '{c}'")

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def string(self) -> Token:
        while self.peek() != '"' and not self.is_at_end():
            self.advance()

        if self.is_at_end():
            raise SyntaxError(f"[line {self.line}] Unterminated string.")

        self.advance()
        value = self.source[self.start + 1: self.current - 1]
        return self.make_token(TokenType.STRING, value)

    def number(self) -> Token:
        while self.peek().isdigit():
            self.advance()

        text = self.source[self.start:self.current]
        return self.make_token(TokenType.NUMBER, int(text))

    def identifier(self) -> Token:
        while not self.is_at_end() and not self.is_whitespace_or_delimiter(self.peek()):
            self.advance()

        return self.make_token(TokenType.IDENTIFIER)

    def is_whitespace_or_delimiter(self, char):
        return char.isspace() or char in '()"'


def scan_all_tokens(source: str) -> List[Token]:
    return Scanner(source).scan_tokens()

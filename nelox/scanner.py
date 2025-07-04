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
            self.start = self.current
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
        return c

    def add_token(self, type: TokenType, literal=None) -> Token:
        text = self.source[self.start:self.current]
        return Token(type, text, literal, self.line)

    def next_token(self) -> Token | None:
        c = self.advance()

        if c == '(':
            return self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            return self.add_token(TokenType.RIGHT_PAREN)
        elif c.isdigit():
            return self.number()
        elif is_alpha(c):
            return self.identifier()
        elif c == '"':
            return self.string()
        elif c in (' ', '\r', '\t'):
            return None
        elif c == '\n':
            self.line += 1
            return None
        else:
            raise SyntaxError(f"[line {self.line}] Unexpected character: '{c}'")

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def string(self) -> Token:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            raise SyntaxError(f"[line {self.line}] Unterminated string.")

        self.advance()
        value = self.source[self.start + 1: self.current - 1]
        return self.add_token(TokenType.STRING, value)

    def number(self) -> Token:
        while self.peek().isdigit():
            self.advance()

        text = self.source[self.start:self.current]
        return self.add_token(TokenType.NUMBER, int(text))

    def identifier(self) -> Token:
        while is_alpha_numeric(self.peek()):
            self.advance()

        return self.add_token(TokenType.IDENTIFIER)


def scan_all_tokens(source: str) -> List[Token]:
    return Scanner(source).scan_tokens()

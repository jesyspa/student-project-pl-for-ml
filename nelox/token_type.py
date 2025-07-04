from enum import Enum, auto


class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    EOF = auto()

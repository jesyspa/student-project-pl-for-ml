from enum import Enum, auto


class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    SET = auto()
    AND = auto()
    FALSE = auto()
    FUNC = auto()
    FOR = auto()
    IF = auto()
    LIST = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    TRUE = auto()
    WHILE = auto()

    EOF = auto()

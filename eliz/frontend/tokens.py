from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    MODULE = auto()
    IMPORT = auto()
    PUBLIC = auto()
    CLASS = auto()
    FN = auto()
    LET = auto()
    NEW = auto()
    THIS = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    NOT = auto()
    AND = auto()
    OR = auto()

    # Punctuation
    DOT = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    # Specials
    EOF = auto()

@dataclass(frozen=True)
class Token:
    type: TokenType
    value: object
    line: int
    column: int

def __repr__(self) -> str:
    return (
        f"Token({self.type.name}, {self.value!r}, )"
        f"line={self.line}, column={self.column})"
    )
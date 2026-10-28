from eliz.frontend.tokens import Token, TokenType

KEYWORDS = {
    "module": TokenType.MODULE,
    "import": TokenType.IMPORT,
    "public": TokenType.PUBLIC,
    "class": TokenType.CLASS,
    "fn": TokenType.FN,
    "let": TokenType.LET,
    "new": TokenType.NEW,
    "this": TokenType.THIS,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
}

class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        while not self._is_at_end():
            char = self._peek()

            if char.isspace():
                self._advance()
                continue

            if char == "#" and self._peek_next() == "#":
                self._skip_comment()
                continue

            if char.isalpha() or char == "_":
                tokens.append(self._read_identifier())
                continue

            if char.isdigit():
                tokens.append(self._read_number())
                continue

            if char == '"':
                tokens.append(self._read_string())
                continue

            tokens.append(self._read_symbol())

        tokens.append(
            Token(TokenType.EOF, None, self.line, self.column)
        )
        return tokens

    def _read_identifier(self) -> Token:
        line, column = self.line, self.column
        start = self.position

        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        value = self.source[start:self.position]
        token_type = KEYWORDS.get(value, TokenType.IDENTIFIER)

        return Token(token_type, value, line, column)

    def _read_number(self) -> Token:
        line, column = self.line, self.column
        start = self.position

        while self._peek().isdigit():
            self._advance()

        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()

            while self._peek().isdigit():
                self._advance()

        value = self.source[start:self.position]

        return Token(TokenType.NUMBER, float(value) if "." in value else int(value), line, column)

    def _read_string(self) -> Token:
        line, column = self.line, self.column
        self._advance()
        characters: list[str] = []

        while not self._is_at_end() and self._peek() != '"':
            char = self._advance()

            if char == "\\" and not self._is_at_end():
                escaped = self._advance()
                escapes = {
                    "n": "\n",
                    "t": "\t",
                    '"': '"',
                    "\\": "\\",
                }
                characters.append(escapes.get(escaped, escaped))
            else:
                characters.append(char)

        if self._is_at_end():
            raise SyntaxError(
                f"Unterminated string at line {line}, column {column}"
            )

        self._advance()

        return Token(TokenType.STRING, "".join(characters), line, column)

    def _read_symbol(self) -> Token:
        line, column = self.line, self.column
        char = self._advance()

        pairs = {
            "==": TokenType.EQUAL,
            "!=": TokenType.NOT_EQUAL,
            "<=": TokenType.LESS_EQUAL,
            ">=": TokenType.GREATER_EQUAL,
            "&&": TokenType.AND,
            "||": TokenType.OR,
        }

        pair = char + self._peek()
        if pair in pairs:
            self._advance()
            return Token(pairs[pair], pair, line, column)

        symbols = {
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.MULTIPLY,
            "/": TokenType.DIVIDE,
            "%": TokenType.MODULO,
            "=": TokenType.ASSIGN,
            "<": TokenType.LESS,
            ">": TokenType.GREATER,
            "!": TokenType.NOT,
            ".": TokenType.DOT,
            ",": TokenType.COMMA,
            ":": TokenType.COLON,
            ";": TokenType.SEMICOLON,
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            "{": TokenType.LEFT_BRACE,
            "}": TokenType.RIGHT_BRACE,
        }

        if char not in symbols:
            raise SyntaxError(
                f"Unexpected character {char!r} at line {line}, column {column}"
            )

        return Token(symbols[char], char, line, column)
    
    def _skip_comment(self) -> None:
        while not self._is_at_end() and self._peek() != "\n":
            self._advance()

    def _peek(self) -> str:
        if self.position >= len(self.source):
            return "\0"
        return self.source[self.position]

    def _peek_next(self) -> str:
        next_position = self.position + 1
        if next_position >= len(self.source):
            return "\0"
        return self.source[next_position]

    def _advance(self) -> str:
        char = self.source[self.position]
        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def _is_at_end(self) -> bool:
        return self.position >= len(self.source)
# python -m unittest tests.test_lexer -v

import unittest

from eliz.frontend.lexer import Lexer
from eliz.frontend.tokens import TokenType


class TestLexer(unittest.TestCase):
    def tokenize(self, source: str):
        return Lexer(source).tokenize()

    def test_variable_declaration(self):
        tokens = self.tokenize("let age = 15;")

        self.assertEqual(
            [token.type for token in tokens],
            [
                TokenType.LET,
                TokenType.IDENTIFIER,
                TokenType.ASSIGN,
                TokenType.NUMBER,
                TokenType.SEMICOLON,
                TokenType.EOF,
            ],
        )

    def test_string_literal(self):
        tokens = self.tokenize('"Hello, Eliz!"')

        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "Hello, Eliz!")

    def test_number_literals(self):
        tokens = self.tokenize("42 3.14")

        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].value, 3.14)

    def test_operators(self):
        tokens = self.tokenize("== != <= >= + - * /")

        self.assertEqual(
            [token.type for token in tokens[:-1]],
            [
                TokenType.EQUAL,
                TokenType.NOT_EQUAL,
                TokenType.LESS_EQUAL,
                TokenType.GREATER_EQUAL,
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.MULTIPLY,
                TokenType.DIVIDE,
            ],
        )

    def test_keywords(self):
        tokens = self.tokenize("if else while true false null")

        self.assertEqual(
            [token.type for token in tokens[:-1]],
            [
                TokenType.IF,
                TokenType.ELSE,
                TokenType.WHILE,
                TokenType.TRUE,
                TokenType.FALSE,
                TokenType.NULL,
            ],
        )

    def test_comments(self):
        tokens = self.tokenize("let age = 15; ## comment\nprint(age);")

        self.assertEqual(
            [token.type for token in tokens],
            [
                TokenType.LET,
                TokenType.IDENTIFIER,
                TokenType.ASSIGN,
                TokenType.NUMBER,
                TokenType.SEMICOLON,
                TokenType.IDENTIFIER,
                TokenType.LEFT_PAREN,
                TokenType.IDENTIFIER,
                TokenType.RIGHT_PAREN,
                TokenType.SEMICOLON,
                TokenType.EOF,
            ],
        )

    def test_unterminated_string(self):
        with self.assertRaises(SyntaxError):
            self.tokenize('"Hello, Eliz!')

    def test_unexpected_character(self):
        with self.assertRaises(SyntaxError):
            self.tokenize("@")

    def test_end_of_file(self):
        tokens = self.tokenize("")

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)


if __name__ == "__main__":
    unittest.main()
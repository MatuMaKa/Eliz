from eliz.frontend.tokens import Token, TokenType
from eliz.frontend import ast_nodes as ast

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.position = 0

    def parse(self) -> ast.Program:
        statements = []

        while not self._is_at_end():
            statements.append(self._parse_statement())

        return ast.Program(statements)

    def _parse_statement(self) -> ast.Statement:
        if self._match(TokenType.LET):
            return self._parse_variable_declaration()

        if self._match(TokenType.IF):
            return self._parse_if_statement()

        if self._match(TokenType.WHILE):
            return self._parse_while_statement()

        if self._match(TokenType.FOR):
            return self._parse_for_statement()

        expression = self._parse_expression()

        if self._match(TokenType.ASSIGN):
            if not isinstance(expression, ast.Variable):
                token = self._previous()
                raise SyntaxError(
                    f"Invalid assignment target at line {token.line}, "
                    f"column {token.column}."
                )
            value = self._parse_expression()
            self._match(TokenType.SEMICOLON)

            return ast.Assignment(
                name=expression.name,
                value=value
            )

        self._match(TokenType.SEMICOLON)
        return ast.ExpressionStatement(expression)

    def _parse_for_statement(self) -> ast.ForStatement:
        self._consume(
            TokenType.LEFT_PAREN,
            "Expected '(' after for."
            )

        initializer = None
        if self._match(TokenType.LET):
            initializer = self._parse_variable_declaration()
        elif not self._check(TokenType.SEMICOLON):
            initializer = self._parse_for_clause()
        else:
            self._advance()

        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._parse_expression()

        self._consume(TokenType.SEMICOLON, "Expected ';' after condition.")

        increment = None
        if not self._check(TokenType.RIGHT_PAREN):
            increment = self._parse_for_clause()

        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after for clauses.")
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before for body.")
        body = self._parse_block()

        return ast.ForStatement(initializer, condition, increment, body)

    def _parse_while_statement(self) -> ast.WhileStatement:
        condition = self._parse_expression()

        self._consume(
            TokenType.LEFT_BRACE,
            "Expected '{' after while condition."
        )

        body = self._parse_block()
        return ast.WhileStatement(condition, body)

    def _parse_if_statement(self) -> ast.IfStatement:
        condition = self._parse_expression()
        self._consume(
            TokenType.LEFT_BRACE,
            "Expected '{' after if condition."
        )

        then_branch = self._parse_block()

        elif_branch = None
        else_branch = None
        if self._match(TokenType.ELIF):
            elif_branch = self._parse_if_statement()

        elif self._match(TokenType.ELSE):
            self._consume(
                TokenType.LEFT_BRACE,
                "Expected '{' after else."
            )
            else_branch = self._parse_block()

        return ast.IfStatement(condition, then_branch, else_branch, elif_branch)

    def _parse_for_clause(self) -> ast.Statement:
        expression = self._parse_expression()

        if self._match(TokenType.ASSIGN):
            if not isinstance(expression, ast.Variable):
                raise SyntaxError(
                    "Invalid assignment target in for loop."
                )
            value = self._parse_expression()
            return ast.Assignment(expression.name, value)

        return ast.ExpressionStatement(expression)

    def _parse_block(self) -> list[ast.Statement]:
        statements = []

        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            statements.append(self._parse_statement())

        self._consume(
            TokenType.RIGHT_BRACE,
            "Expected '}' after block."
        )
        return statements

    def _parse_variable_declaration(self) -> ast.VariableDeclaration:
        name = self._consume(
            TokenType.IDENTIFIER,
            "Expected variable name after 'let'."
        ).value

        type_name = None
        if self._match(TokenType.COLON):
            type_name = self._consume(
                TokenType.IDENTIFIER,
                "Expected type name after ':'."
            ).value

        self._consume(
            TokenType.ASSIGN,
            "Expected '=' after variable name."
        )

        value = self._parse_expression()
        self._match(TokenType.SEMICOLON)

        return ast.VariableDeclaration(
            name=name,
            value=value,
            type_name=type_name
        )

    def _parse_expression(self) -> ast.Expression:
        return self._parse_or()

    def _parse_or(self) -> ast.Expression:
        expression = self._parse_and()

        while self._match(TokenType.OR):
            operator = self._previous().value
            right = self._parse_and()
            expression = ast.BinaryExpression(expression, operator, right)

        return expression

    def _parse_and(self) -> ast.Expression:
        expression = self._parse_equality()

        while self._match(TokenType.AND):
            operator = self._previous().value
            right = self._parse_equality()
            expression = ast.BinaryExpression(expression, operator, right)

        return expression

    def _parse_equality(self) -> ast.Expression:
        expression = self._parse_comparison()
        while self._match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self._previous().value
            right = self._parse_comparison()
            expression = ast.BinaryExpression(expression, operator, right)
        return expression

    def _parse_comparison(self) -> ast.Expression:
        expression = self._parse_term()

        while self._match(
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL
        ):
            operator = self._previous().value
            right = self._parse_term()
            expression = ast.BinaryExpression(expression, operator, right)
        return expression

    def _parse_term(self) -> ast.Expression:
        expression = self._parse_factor()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().value
            right = self._parse_factor()
            expression = ast.BinaryExpression(expression, operator, right)

        return expression

    def _parse_factor(self) -> ast.Expression:
        expression = self._parse_unary()

        while self._match(
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.MODULO,
        ):
            operator = self._previous().value
            right = self._parse_unary()
            expression = ast.BinaryExpression(expression, operator, right)

        return expression

    def _parse_unary(self) -> ast.Expression:
        if self._match(TokenType.NOT, TokenType.MINUS):
            operator = self._previous().value
            right = self._parse_unary()
            return ast.UnaryExpression(operator, right)

        return self._parse_call()

    def _parse_call(self) -> ast.Expression:
        expression = self._parse_primary()

        while True:
            if self._match(TokenType.LEFT_PAREN):
                arguments = []

                if not self._check(TokenType.RIGHT_PAREN):
                    while True:
                        arguments.append(self._parse_expression())
                        if not self._match(TokenType.COMMA):
                            break

                self._consume(
                    TokenType.RIGHT_PAREN,
                    "Expected ')' after arguments.",
                )

                expression = ast.CallExpression(expression, arguments)
            else:
                break

        return expression

    def _parse_primary(self) -> ast.Expression:
        if self._match(TokenType.FALSE):
            return ast.Literal(False)

        if self._match(TokenType.TRUE):
            return ast.Literal(True)

        if self._match(TokenType.NULL):
            return ast.Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return ast.Literal(self._previous().value)

        if self._match(TokenType.IDENTIFIER):
            return ast.Variable(self._previous().value)

        if self._match(TokenType.LEFT_PAREN):
            expression = self._parse_expression()
            self._consume(
                TokenType.RIGHT_PAREN,
                "Expected ')' after expression.",
            )
            return expression

        token = self._peek()
        raise SyntaxError(
            f"Expected an expression at line {token.line}, "
            f"column {token.column}."
        )

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()

        token = self._peek()
        raise SyntaxError(
            f"{message} Line {token.line}, column {token.column}."
        )

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return token_type == TokenType.EOF
        return self._peek().type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.position += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.position]

    def _previous(self) -> Token:
        return self.tokens[self.position - 1]
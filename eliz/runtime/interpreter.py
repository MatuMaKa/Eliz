from typing import Any

from eliz.frontend import ast_nodes as ast
from eliz.runtime.environment import Environment
from eliz.errors.exceptions import ElizRuntimeError

class Interpreter:
    def __init__(self) -> None:
        self.environment = Environment()
        self.globals = self.environment
        self._define_builtins()

    def interpret(self, program: ast.Program) -> None:
        try:
            for statement in program.statements:
                self._execute(statement)
        except ElizRuntimeError:
            raise
        except Exception as error:
            raise ElizRuntimeError(str(error)) from error

    def _define_builtins(self) -> None:
        self.environment.define("print",
                                self._builtin_print)

    @staticmethod
    def _builtin_print(*arguments: Any) -> None:
        print(*arguments)

    def _execute(self, statement: ast.Statement) -> None:
        if isinstance(statement, ast.VariableDeclaration):
            value = self._evaluate(statement.value)

            if statement.type_name is not None:
                from eliz.runtime.types import get_type_name

                actual_type = get_type_name(value)

                if actual_type != statement.type_name:
                    raise ElizRuntimeError(
                        f"Expected type '{statement.type_name}', "
                        f"got '{actual_type}'"
                    )

            self.environment.define(statement.name, value)
            return

        if isinstance(statement, ast.Assignment):
            value = self._evaluate(statement.value)
            self.environment.assign(statement.name, value)
            return

        if isinstance(statement, ast.ExpressionStatement):
            self._evaluate(statement.expression)
            return

        if isinstance(statement, ast.IfStatement):
            condition = self._evaluate(statement.condition)

            if self._is_truthy(condition):
                for child in statement.then_branch:
                    self._execute(child)
            elif statement.else_branch is not None:
                for child in statement.else_branch:
                    self._execute(child)
            return

        if isinstance(statement, ast.WhileStatement):
            while self._is_truthy(self._evaluate(statement.condition)):
                for child in statement.body:
                    self._execute(child)
            return

        raise ElizRuntimeError(
            f"Unsupported statement: {type(statement).__name__}"
        )

    def _evaluate(self, expression: ast.Expression) -> Any:
        if isinstance(expression, ast.Literal):
            return expression.value

        if isinstance(expression, ast.Variable):
            return self.environment.get(expression.name)

        if isinstance(expression, ast.UnaryExpression):
            right = self._evalutate(expression.operand)

            if expression.operator == "-":
                return -right

            if expression.operator in ("!", "not"):
                return not self._is_truthy(right)

            raise ElizRuntimeError(
                f"Unknown unary operator '{expression.operator}'."
            )

        if isinstance(expression, ast.BinaryExpression):
            return self._evaluate_binary(expression)

        if isinstance(expression, ast.CallExpression):
            callee = self._evaluate(expression.callee)
            args = [
                self._evaluate(argument)
                for argument in expression.arguments
            ]

            if not callable(callee):
                raise ElizRuntimeError(
                    "Only functions can be called."
                )

            return callee(*args)

        raise ElizRuntimeError(
            f"Unsupported expression: {type(expression).__name__}"
        )

    def _evaluate_binary(self, expression: ast.BinaryExpression) -> Any:
        left = self._evaluate(expression.left)
        right = self._evaluate(expression.right)
        operator = expression.operator

        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right
        if operator == "/":
            return left / right
        if operator == "%":
            return left % right
        if operator == "==":
            return left == right
        if operator == "!=":
            return left != right
        if operator == "<":
            return left < right
        if operator == "<=":
            return left <= right
        if operator == ">":
            return left > right
        if operator == ">=":
            return left >= right
        if operator in ("and", "&&"):
            return self.is_truthy(left) and self._is_truthy(right)
        if operator in ("or", "||"):
            return self.is_truthy(left) or self._is_truthy(right)

        raise ElizRuntimeError(
            f"Unknown binary operator '{operator}'"
        )
    
@staticmethod
def _is_truthy(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return bool(value)
from dataclasses import dataclass
from typing import Any

class ASTNode:
    """Base class for all AST nodes."""

class Statement(ASTNode):
    """Base class for all statement nodes."""

class Expression(ASTNode):
    """Base class for all expression nodes."""

@dataclass
class Program(ASTNode):
    statements: list[Statement]

@dataclass
class ModuleDeclaration(Statement):
    name: str

@dataclass
class ImportDeclaration(Statement):
    module_name: str

@dataclass
class ClassDeclaration(Statement):
    name: str
    methods: list[Statement]
    is_public: bool = False

@dataclass
class FunctionDeclaration(Statement):
    name: str
    parameters: list[str]
    body: list[Statement]
    is_public: bool = False

@dataclass
class VariableDeclaration(Statement):
    name: str
    value: Expression
    type_name: str | None = None

@dataclass
class Assignment(Statement):
    name: str
    value: Expression

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_branch: list[Statement]
    else_branch: list[Statement] | None = None
    elif_branch: IfStatement | None = None

@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: list[Statement]

@dataclass
class ForStatement(Statement):
    initializer: Statement | None
    condition: Expression | None
    increment: Statement | None
    body: list[Statement]

@dataclass
class ReturnStatement(Statement):
    value: Expression | None = None

@dataclass
class ExpressionStatement(Statement):
    expression: Expression

@dataclass
class Literal(Expression):
    value: Any

@dataclass
class Variable(Expression):
    name: str

@dataclass
class ThisExpression(Expression):
    pass

@dataclass
class NewExpression(Expression):
    class_name: str
    arguments: list[Expression]

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class UnaryExpression(Expression):
    operator: str
    operand: Expression

@dataclass
class CallExpression(Expression):
    callee: Expression
    arguments: list[Expression]

@dataclass
class GetExpression(Expression):
    object: Expression
    property: str

@dataclass
class SetExpression(Expression):
    object: Expression
    name: str
    value: Expression

@dataclass
class BlockStatement(Statement):
    statements: list[Statement]
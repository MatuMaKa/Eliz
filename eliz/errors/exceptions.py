class ElizError(Exception):
    """Base class for all Eliz errors."""

class ElizSyntaxError(ElizError):
    """Raised when Eliz source code has invalid syntax."""

    def __init__(self, message: str, line: int | None = None, column: int | None = None) -> None:
        self.message = message
        self.line = line
        self.column = column

        if line is not None and column is not None:
            message = f"{message} (line {line}, column {column})"
        elif line is not None:
            message = f"{message} (line {line})"
        super().__init__(message)

class ElizRuntimeError(ElizError):
    """Raised when an error occurs while executing code."""

    def __init__(self, message: str, line: int | None = None, column: int | None = None) -> None:
        self.message = message
        self.line = line
        self.column = column

        if line is not None and column is not None:
            message = f"{message} (line {line}, column {column})"
        elif line is not None:
            message = f"{message} (line {line})"
        super().__init__(message)

class ElizNameError(ElizRuntimeError):
    """Raised when a variable or identifier is undefined."""

class ElizTypeError(ElizRuntimeError):
    """Raised when an operation received an invalid type."""

class ElizImportError(ElizError):
    """Raised when an imported module cannot be found or loaded."""

class ElizArgumentError(ElizRuntimeError):
    """Raised when a function receives invalid arguments."""
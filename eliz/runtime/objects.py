from typing import Any, Callable

class ReturnSignal(Exception):
    def __init__(self, value: Any) -> None:
        self.value = value

class ElizFunction:
    def __init__(self, name: str, parameters: list[str], body: list[Any], closure: Any, interpreter: Any, is_initializer: bool = False) -> None:
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure
        self.interpreter = interpreter
        self.is_initializer = is_initializer

    def bind(self, instance: "ElizInstance") -> "ElizFunction":
        from eliz.runtime.environment import Environment

        env = Environment(self.closure)
        env.define("this", instance)

        return ElizFunction(
            name=self.name,
            parameters=self.parameters,
            body=self.body,
            closure=env,
            interpreter=self.interpreter,
            is_initializer=self.is_initializer
        )

    def __call__(self, *args: Any) -> Any:
        from eliz.runtime.environment import Environment
        from eliz.errors.exceptions import ElizArgumentError

        if len(args) != len(self.parameters):
            raise ElizArgumentError(
                f"Function '{self.name}' expects {len(self.parameters)} "
                f"arguments, but received {len(args)}."
            )

        previous_env = self.interpreter.environment
        env = Environment(previous_env)

        for param, arg in zip(self.parameters, args):
            env.define(param.name, arg)

        self.interpreter.environment = env

        try:
            for statement in self.body:
                self.interpreter._execute(statement)
        except ReturnSignal as signal:
            if self.is_initializer:
                return self.closure.get("this")
            return signal.value
        finally:
            self.interpreter.environment = previous_env

        if self.is_initializer:
            return self.closure.get("this")

        return None

    def __repr__(self) -> str:
        return f"<fn {self.name}>"

class ElizClass:
    def __init__(self, name: str, methods: dict[str, ElizFunction]) -> None:
        self.name = name
        self.methods = methods

    def find_method(self, name: str) -> ElizFunction | None:
        return self.methods.get(name)

    def __call__(self, *args: Any) -> "ElizInstance":
        instance = ElizInstance(self)
        initializer = self.find_method("init")

        if initializer is not None:
            initializer.bind(instance)(*args)

        return instance

    def __repr__(self) -> str:
        return f"<class {self.name}>"

class ElizInstance:
    def __init__(self, eliz_class: ElizClass) -> None:
        self.eliz_class = eliz_class
        self.fields: dict[str, Any] = {}

    def get(self, name: str) -> Any:
        if name in self.fields:
            return self.fields[name]

        method = self.eliz_class.find_method(name)

        if method is not None:
            return method.bind(self)

        raise AttributeError(
            f"Object of class '{self.eliz_class.name}' "
            f"has no attribute '{name}'."
        )

    def set(self, name: str, value: Any) -> None:
        self.fields[name] = value

    def __repr__(self) -> str:
        return f"<instance of {self.eliz_class.name}>"
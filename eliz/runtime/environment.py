class Environment:
    def __init__(self, parent: "Environment | None" = None) -> None:
        self.values: dict[str, object] = {}
        self.parent = parent

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def get(self, name: str) -> object:
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise NameError(f"Undefined variable '{name}'.")

    def assign(self, name: str, value: object) -> None:
        if name in self.values:
            self.values[name] = value
            return

        if self.parent is not None:
            self.parent.assign(name, value)
            return

        raise NameError(f"Undefined variable '{name}'.")
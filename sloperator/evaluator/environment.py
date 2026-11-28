from dataclasses import dataclass

from sloperator.errors import SlopRuntimeError
from sloperator.evaluator.values import Value


@dataclass
class Binding:
    value: Value
    mutable: bool
    kind: str = "binding"


class Environment:
    def __init__(self, parent: "Environment | None" = None) -> None:
        self.bindings: dict[str, Binding] = {}
        self.parent = parent

    def declare(
        self,
        name: str,
        value: Value,
        mutable: bool,
        line: int,
        kind: str = "binding",
    ) -> None:
        if name in self.bindings:
            raise SlopRuntimeError(line, f"'{name}' is already declared in this scope")
        self.bindings[name] = Binding(value, mutable, kind)

    def get(self, name: str, line: int) -> Value:
        return self.lookup(name, line).value

    def get_for_assignment(self, name: str, line: int) -> Value:
        binding = self.lookup(name, line)
        self.require_mutable(name, binding, line)
        return binding.value

    def assign(self, name: str, value: Value, line: int) -> None:
        binding = self.lookup(name, line)
        self.require_mutable(name, binding, line)
        binding.value = value

    def require_mutable(self, name: str, binding: Binding, line: int) -> None:
        if not binding.mutable:
            if binding.kind == "loadbearing":
                raise SlopRuntimeError(line, f"cannot assign to loadbearing '{name}'")
            raise SlopRuntimeError(line, f"cannot assign to immutable binding '{name}'")

    def lookup(self, name: str, line: int) -> Binding:
        env: Environment | None = self
        while env is not None:
            if name in env.bindings:
                return env.bindings[name]
            env = env.parent
        raise SlopRuntimeError(line, f"undefined variable '{name}'")

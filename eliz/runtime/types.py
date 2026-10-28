from typing import Any

BUILTIN_TYPES: dict[str, type | tuple[type, ...] | None] = {
    "String": str,
    "Int": int,
    "Float": float,
    "Bool": bool,
    "Null": type(None),
}

def get_type_name(value: Any) -> str:
    if value is None:
        return "Null"
    if isinstance(value, str):
        return "String"
    if isinstance(value, int):
        return "Int"
    if isinstance(value, float):
        return "Float"
    if isinstance(value, bool):
        return "Bool"

    return type(value).__name__

def is_type(value: Any, type_name: str) -> bool:
    expected_type = BUILTIN_TYPES.get(type_name)

    if expected_type is None:
        return type_name == "Null" and value is None

    return isinstance(value, expected_type)
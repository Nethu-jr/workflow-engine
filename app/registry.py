from typing import Any, Callable, Dict

ToolFunc = Callable[[Dict[str, Any]], Dict[str, Any]]
_TOOL_REGISTRY: Dict[str, ToolFunc] = {}

def register_tool(name: str):
    def decorator(func: ToolFunc):
        _TOOL_REGISTRY[name] = func
        return func
    return decorator

def get_tool(name: str) -> ToolFunc:
    return _TOOL_REGISTRY[name]

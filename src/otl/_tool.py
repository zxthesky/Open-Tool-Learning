from __future__ import annotations

from typing import Dict, List

class BasicToolCallingModule:
    def __init__(self) -> None:
        self.tool_pool: BasicToolPool


class BasicTool:
    tool_name: str
    tool_description: str

    def __init__(self) -> None:
        self.tool_name
        self.tool_description

    def __call__(self):
        pass

    def __eq__(self, other):
        # if isinstance(other, class_name):
        #     return self.name == other.name
        # return False
        raise NotImplementedError

    def __hash__(self):
        # return hash((self.name, self.description))
        raise NotImplementedError


class BasicLocalTool(BasicTool):
    pass


class BasicRemoteTool(BasicTool):
    pass


class BasicToolPool:
    pool: List[BasicTool]

    def __init__(self) -> None:
        self.pool: Dict[str, List[BasicTool]]

    def add_tool(self) -> None:
        pass

    def remove_tool(self) -> None:
        pass

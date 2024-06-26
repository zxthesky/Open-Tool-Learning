from __future__ import annotations

from typing import List

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

class LocalTool(BasicTool):
    pass

class RemoteTool(BasicTool):
    pass

class BasicToolPool:
    pool: List[BasicTool]

    def __init__(self) -> None:
        self.pool: List[BasicTool]

    def add_tool(self) -> None:
        pass

    def remove_tool(self) -> None:
        pass

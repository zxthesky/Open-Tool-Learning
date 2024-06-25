from __future__ import annotations

from typing import List

class Tool:
    tool_name: str
    tool_description: str

    def __init__(self) -> None:
        self.tool_name
        self.tool_description


    def __call__(self):
        pass

class LocalTool(Tool):
    pass

class RemoteTool(Tool):
    pass

class ToolPool:
    pool: List[Tool]

    def __init__(self) -> None:
        self.pool: List[Tool]
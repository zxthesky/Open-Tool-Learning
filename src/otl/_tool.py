from __future__ import annotations

from typing import Any, Dict, List

from ._vectorstore import BasicVectorStore

class BasicToolCallingModule:
    def __init__(self) -> None:
        self.set_list: List[str]
        self.tools_set: Dict[str, BasicToolPool]


class BasicTool:
    tool_name: str
    tool_description: str
    callable: bool

    def __init__(self) -> None:
        self.tool_name
        self.tool_description

        self.callable

    def __call__(self):
        pass

    def __eq__(self, other) -> bool:
        # if isinstance(other, class_name):
        #     return self.name == other.name
        # return False
        raise NotImplementedError

    def __hash__(self) -> Any:
        # return hash((self.name, self.description))
        raise NotImplementedError


class BasicLocalTool(BasicTool):
    pass


class BasicRemoteTool(BasicTool):
    pass


class BasicToolPool:
    id_list: List[str]
    tools: Dict[str, List[BasicTool]]
    vectors: BasicVectorStore

    def __init__(self) -> None:
        self.id_list: List[str]
        self.tools: Dict[str, List[BasicTool]]
        self.vectors: BasicVectorStore

    def add_tool(self) -> None:
        raise NotImplementedError

    def remove_tool(self) -> None:
        raise NotImplementedError

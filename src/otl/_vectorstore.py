from typing import Any, Dict

class BasicVectorStore:
    def __init__(self) -> None:
        self.vector_type: str
        self.storage: Dict[str, Any]

    def add(self) -> None:
        raise NotImplementedError
    
    def remove(self) -> None:
        raise NotImplementedError
    
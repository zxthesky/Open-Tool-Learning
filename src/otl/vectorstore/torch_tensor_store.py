from typing import Dict

from .._vectorstore import BasicVectorStore
from .._embedding import BasicEmbedder


class TensorStore(BasicVectorStore):
    def __init__(self) -> None:
        self.vector_type = "torch"
        import torch
        self.storage: Dict[str,torch.Tensor]

    def add(self, embedder: BasicEmbedder, key_id: str, input_text: str) -> None:
        self.storage[key_id] = embedder(input_text) #TODO 待测试

    def remove(self, key_id: str) -> None:
        del self.storage[key_id]
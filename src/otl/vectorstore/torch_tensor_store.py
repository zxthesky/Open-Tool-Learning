from typing import Dict

from .._vectorstore import BasicVectorStore

class TensorStore(BasicVectorStore):
    def __init__(self) -> None:
        import torch
        self.storage: Dict[str,torch.Tensor]

    
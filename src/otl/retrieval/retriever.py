from typing import Any, List, Literal

from .._retrieval import BasicRetriever, BasicEmbedder


class Retriever(BasicRetriever):
    def __init__(self, embedder: BasicEmbedder) -> None:
        self.embedder: BasicEmbedder = embedder
        self.top_k: int = 1
        self.similarity: Literal["cosine"] = "cosine"

    def encode(self, inputs: str | List[str]) -> Any:
        return self.embedder(inputs)
    
    def retrieval(query_vector, document_vectors) -> int:
        pass
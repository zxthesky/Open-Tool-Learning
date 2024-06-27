from typing import Any, List, Literal

from .._retrieval import BasicRetriever
from .._vectorstore import BasicVectorStore

class Retriever(BasicRetriever):
    def __init__(self) -> None:
        self.top_k: int = 1
        self.similarity: Literal["cosine"] = "cosine"
    
    def retrieval(query_vector, vector_store: BasicVectorStore) -> Any:
        pass




from .._retrieval import BasicRetriever, BasicEmbedder



class Retriever(BasicRetriever):
    def __init__(self, embedder: BasicEmbedder) -> None:
        self.embedder = embedder


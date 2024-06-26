
from transformers import AutoModel, AutoTokenizer

from .._retrieval import BasicLocalEmbedder

class LocalEmbedder(BasicLocalEmbedder):
    def __init__(self, checkpoint_path) -> None:
        
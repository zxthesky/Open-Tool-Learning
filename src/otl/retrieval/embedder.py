from typing import Any, List

from .._retrieval import BasicLocalEmbedder

class LocalEmbedder(BasicLocalEmbedder):
    def __init__(self, checkpoint_path) -> None:
        from transformers import AutoModel, AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
        self.model = AutoModel.from_pretrained(checkpoint_path, trust_remote_code=True)

    def __call__(self, inputs: str | List[str]) -> Any:
        batch_dict = self.tokenizer(inputs, padding=True, truncation=True, return_tensors='pt')
        outputs = self.model(**batch_dict)
        embeddings = outputs.last_hidden_state[:, 0]
        return embeddings #TODO 自定义embedding格式
from typing import List

from .._agent import ChatAgent
from .._model import FoundationLanguageModel

class Agent(ChatAgent):
    def __init__(self,
        name: str = "",
        description: str = "") -> None:
        self.name: str = name
        self.description: str = description
        self.system_message: str = "You are a helpful assistant."

        self.llm: FoundationLanguageModel = None

        self.chat_history: List[dict] = [{"role": "system", "content": self.system_message}]
        self.chat_template = None

        self.tool_calling = None

        self.tool_retrieval = None

    def clear_history(self) -> None:
        self.chat_history = [{"role": "system", "content": self.system_message}]

    def load_llm(self, model_name, model_checkpoint) -> None:
        from ..model.llm import AutoModel
        self.llm = AutoModel(model_name, checkpoint_path=model_checkpoint)

    
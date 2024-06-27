
from .._tool import BasicToolCallingModule
from .._retrieval import BasicRetriever

class ToolCallingModule(BasicToolCallingModule):
    def __init__(self, retriever: BasicRetriever) -> None:
        self.set_list = []
        self.tools_set = dict()
        self.retriever = retriever

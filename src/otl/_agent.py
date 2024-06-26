from __future__ import annotations


class BasicAgent:
    '''A basic class for agent.

    Agent Information:
        self.name
        self.description

    Foundation Model:
        self.llm
    '''
    def __init__(self) -> None:

        self.name: str
        self.description: str

        self.llm

    def load_llm(self) -> None:
        pass


class ChatAgent(BasicAgent):
    '''A chat agent with tool learning and retrieval modules.

    Agent Information:
        self.name
        self.description
        self.system_message

    Foundation Model:
        self.llm

    Chat Relevant Information:
        self.chat_history
        self.chat_template

    Function/Tool Calling Module:
        self.tool_calling

    Retrieval Module:
        self.retrieval
    '''
    def __init__(self) -> None:

        self.name: str
        self.description: str
        self.system_message: str = "You are a helpful assistant."

        self.llm

        self.chat_history = [{"role": "system", "content": self.system_message}]
        self.chat_template

        self.tool_calling

        self.tool_retrieval

    def clear_history(self) -> None:
        self.chat_history = [{"role": "system", "content": self.system_message}]
from __future__ import annotations


class Agent:
    '''A base class for Agent.

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
    def __init__(self):

        self.name
        self.description
        self.system_message = "You are a helpful assistant."

        self.llm

        self.chat_history = [{"role": "system", "content": self.system_message}]
        self.chat_template

        self.tool_calling

        self.tool_retrieval

    def clear_history(self):
        self.chat_history = [{"role": "system", "content": self.system_message}]

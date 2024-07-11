from typing import List
import openai

class Chatgpt:

    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key
        self.model_name = "gpt-3.5-turbo"

    def answer(self, data):
        pass





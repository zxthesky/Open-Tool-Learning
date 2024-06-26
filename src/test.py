import sys
sys.dont_write_bytecode = True

import otl
from otl.agents import Agent
from otl.model.llm import LLaMA


if __name__ == "__main__":
    agent = Agent()

    checkpoint_path = "..."
    model = LLaMA(checkpoint_path)

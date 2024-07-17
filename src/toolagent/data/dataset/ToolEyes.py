import json
import re
from ...utils import read_JSON,write_JSON



class ToolEyes:
    """ dataset ToolEyes

    该类是ToolEyes数据集的处理

    Attributes:
        filename (str): the path of the file

    Example:
        >>> ToolEyes = ToolEyes("...")

    """
    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def load_data(self):
        self.data.extend(process_data(self.filename))

def process_system(input):
    candidate_tools_str = re.search("\[[\s\S]*\]", input).group(0)
    raw_instruction = input.split("Specifically, you have access of the following tools:\n")[0]
    raw_instruction += "Specifically, you have access of the following tools:\n" + "[candidate_tools]" + "\n\nLet's Begin!"
    candidate_tools = json.loads(candidate_tools_str)
    return raw_instruction, candidate_tools


def get_conersation_and_candidate_tools(conversations):
    final_conversation = []
    candidate_tools = []
    for conversation in conversations:
        temp_conversation = {}
        if conversation["from"] == "system":
            temp_conversation["role"] = "system"
            instruction, candidate_tools = process_system(conversation["value"])
            temp_conversation["content"] = instruction
        else:
            temp_conversation["role"] = conversation["from"]
            temp_conversation["content"] = conversation["value"]
        final_conversation.append(temp_conversation)
    return final_conversation, candidate_tools

def process_data(filename):
    all_data = read_JSON(filename)
    final_data_lst = []
    for data in all_data:
        final_data_need = {}
        final_data_need["id"] = data["id"]
        conversations, candidate_tools = get_conersation_and_candidate_tools(data["conversations"])
        final_data_need["conversations"] = conversations
        final_data_need["candidate_tools"] = candidate_tools
        query = ""
        for i in conversations:
            if i["role"] == "user":
                query = i["content"]
                break
        final_data_need["query"] = query
        final_data_lst.append(final_data_need)

    return final_data_lst


if __name__ == '__main__':
    filename = ""
    process_data(filename)







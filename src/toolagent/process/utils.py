import re
from ..utils import read_JSON,write_JSON
import json
import os
import ast
def extract_tool_name_and_parameters_API_Bank(input: str)->dict:
    """(API_Bank)get tool name and parameters from response

    从 api_bank 中提取处工具名称和参数的操作

    Args:
        input (str):response

    Returns:
        dict: tool name and parameters construct the dict
    """
    tool_name = ""
    for i in range(13, len(input)):
        if input[i] != "(":
            tool_name += input[i]
        else:
            break

    parameters = re.search("\(.*\)", input).group(0)
    parameter_dict = {}
    if parameters[0] == "(":
        parameters = parameters[1:]
    if parameters[-1] == ")":
        parameters = parameters[:-1]
    all_parameter_names = []
    if parameters != "":
        first_parameter_name = ""
        for i in parameters:
            if i != "=":
                first_parameter_name += i
            else:
                all_parameter_names.append(first_parameter_name)
                break

        other_parameter_names = re.findall(', [^=]*=', parameters)
        for parameter in other_parameter_names:
            parameter_name_temp = parameter[2:-1]
            all_parameter_names.append(parameter_name_temp)

        parameter_entity = re.split(', [^=]*=', parameters)
        if len(all_parameter_names) != 0:
            parameter_entity[0] = parameter_entity[0].split("=")[1]
            assert len(parameter_entity) == len(all_parameter_names)

            for i in range(len(parameter_entity)):
                parameter_dict[all_parameter_names[i]] = parameter_entity[i]

        for j in parameter_dict:
            if parameter_dict[j][0] == "'":
                parameter_dict[j] = parameter_dict[j][1:]
            if parameter_dict[j][-1] == "'":
                parameter_dict[j] = parameter_dict[j][:-1]


    function_call = {}
    function_call["name"] = tool_name
    function_call["parameters"] = parameter_dict

    return function_call

def process_input_API_Bank(input: str, candidate_tool: bool)->tuple:
    """(API_Bank) deal the raw API_Bank data

    处理api_bank的数据， 原始数据混在一起，需要将其分开

    Args:
        input (str): raw data
        candidate_tool (bool): whether contain candidate tools

    Returns:
        tuple: conversation(final multi-conversation and candidate_tools(str))

    """
    conversation = []
    candidate_tool_str = ""
    user_ai_split = input.split("\nUser: ")
    if candidate_tool == True:
        candidate_tool_str = user_ai_split[0]
        user_ai_split = user_ai_split[1:]

    for use_ai in user_ai_split:
        ai_splits = use_ai.split("\nAI: ")
        user = ai_splits[0]
        ais = ai_splits[1:]
        if "\nAPI-Request: " in user:
            raw_split_data = user.split("\nAPI-Request: ")
            user = raw_split_data[0]
            conversation.append({"role":"user", "content": user})
            for i in raw_split_data[1:]:
                request, function_result = i.split("->")
                now_response = {}
                now_response["role"] = "assistant"
                now_response["content"] = "API-Request: " + request
                now_response["function_call"] = [extract_tool_name_and_parameters_API_Bank(request)]
                now_response["function_result"] = [function_result]
                conversation.append(now_response)
        else:
            if user != "":
                if user.startswith("User: "):
                    user = user[6:]
                conversation.append({"role": "user", "content": user})

        for ai in ais:
            if "\nAPI-Request: " in ai:
                raw_split_data = ai.split("\nAPI-Request: ")
                ai = raw_split_data[0]
                conversation.append({"role": "assistant", "content": ai})
                for i in raw_split_data[1:]:
                    request, function_result = i.split("->")
                    now_response = {}
                    now_response["role"] = "assistant"
                    now_response["content"] = "API-Request: " + request
                    now_response["function_call"] = [extract_tool_name_and_parameters_API_Bank(request)]
                    now_response["function_result"] = [function_result]
                    conversation.append(now_response)
            else:
                if ai != "":
                    conversation.append({"role": "assistant", "content": ai})

    return (conversation, candidate_tool_str)
def get_query_API_Bank(input: str)->str:
    """(API_Bank)get raw query from input

    从输入中抽取处原始的问题

    Args:
        input(str): input

    Returns:
        str: user's query

    """
    query_raw = input.split("\nUser: ")[1]
    query_raw = query_raw.split("\nAI: ")[0]
    if "\nAPI-Request: " in query_raw:
        query_raw = query_raw.split("\nAPI-Request: ")[0]
    return query_raw

def process_level12_test(filepath_response: str)->list:
    """process api_bank level1 and level2 test data

    处理api_bank的level1和level2级别的test数据集， 将其转为通用格式

    Args:
        filepath_response (str): response to filepath which contain "response"

    Returns:
        list: final data which we need [{}, {}......] every {} contain many labels corresponding to the general dataset

    """
    return_response_data = read_JSON(filepath_response)

    file_to_data = {}
    for i in return_response_data:
        if i["file"] in file_to_data:
            file_to_data[i["file"]].append(i)
        else:
            file_to_data[i["file"]] = [i]
    final_data_lst = []
    for file in file_to_data:
        final_data_need = {}
        final_data_need["id"] = file
        final_data = file_to_data[file][-1]
        instruction_raw = final_data["instruction"]
        instruction, candidate_tool_str = instruction_raw.split("\n\nAPI descriptions:\n")
        instruction += "\n\nAPI descriptions:\n[candidate_tools]"
        candidate_tool_str = candidate_tool_str.replace("\n", ",")
        candidate_tool_str = "[" + candidate_tool_str + "]"
        tools = json.loads(candidate_tool_str)


        raw_conversation, _= process_input_API_Bank(final_data["input"], candidate_tool=False)
        raw_conversation.append({"role": "assistant", "content": final_data["expected_output"]})
        raw_conversation.insert(0,{"role": "system", "content": instruction})
        final_data_need["conversations"] = raw_conversation
        final_data_need["candidate_tools"] = tools
        query = ""
        for i in raw_conversation:
            if i["role"] == "user":
                query = i["content"]
                break
        final_data_need["query"] = query
        final_data_lst.append(final_data_need)


    return final_data_lst

def process_level3_test(filepath_response: str)-> list:
    """process api_bank level3 test data

        处理api_bank的level3级别的test数据集， 将其转为通用格式

        Args:
            filepath_response (str): response to filepath which contain "response"

        Returns:
            list: final data which we need [{}, {}......] every {} contain many labels corresponding to the general dataset

        """

    return_response_data = read_JSON(filepath_response)

    file_to_data = {}
    for i in return_response_data:
        if i["sample_id"] in file_to_data:
            file_to_data[i["sample_id"]].append(i)
        else:
            file_to_data[i["sample_id"]] = [i]
    final_data_lst = []
    for sample_id in file_to_data:
        final_data_need = {}
        final_data_need["id"] = sample_id
        final_data = file_to_data[sample_id][-1]

        instruction_raw = final_data["instruction"].split("\n\nAPI descriptions:\n")[0]
        instruction_raw += "\n\nAPI descriptions:\n[candidate_tools]"
        raw_conversation, candidate_tool_str = process_input_API_Bank(final_data["input"], candidate_tool=True)
        candidate_tool_str = candidate_tool_str.replace("\n", ",")
        candidate_tool_str = "[" + candidate_tool_str + "]"
        tools = json.loads(candidate_tool_str)
        raw_conversation.insert(0, {"role": "system", "content": instruction_raw})
        raw_conversation.append({"role": "assistant", "content": final_data["output"]})
        final_data_need["conversations"] = raw_conversation
        final_data_need["candidate_tools"] = tools
        query = ""
        for i in raw_conversation:
            if i["role"] == "user":
                query = i["content"]
                break
        final_data_need["query"] = query
        final_data_lst.append(final_data_need)

    return final_data_lst
def process_train_data_API_Bank(filepath: str) -> list:
    """process api_bank train data

    处理api_bank的train数据集， 将其转为通用格式

    Args:
        filepath(str): response to filepath which contain "response"

    Returns:
        list: final data which we need [{}, {}......] every {} contain many labels corresponding to the general dataset

    """
    all_data = read_JSON(filepath)
    query_to_data = {}
    for data in all_data:
        query = get_query_API_Bank(data["input"])
        if query not in query_to_data:
            query_to_data[query] = [data]
        else:
            query_to_data[query].append(data)
    final_data_lst = []
    for query in query_to_data:
        final_data_need = {}
        final_data = query_to_data[query][-1]

        final_data_need["id"] = query
        instruction_raw = final_data["instruction"].split("\n\nAPI descriptions:\n")[0]
        instruction_raw += "\n\nAPI descriptions:\n[candidate_tools]"
        raw_conversation, candidate_tool_str = process_input_API_Bank(final_data["input"], candidate_tool=True)
        candidate_tool_str = "[" + candidate_tool_str + "]"
        candidate_tool_str = candidate_tool_str.replace("\n", ",")
        tools = json.loads(candidate_tool_str)
        raw_conversation.insert(0, {"role": "system", "content": instruction_raw})
        raw_conversation.append({"role": "assistant", "content": final_data["output"][4:]})
        final_data_need["conversations"] = raw_conversation
        final_data_need["candidate_tools"] = tools
        query = ""
        for i in raw_conversation:
            if i["role"] == "user":
                query = i["content"]
                break
        final_data_need["query"] = query
        final_data_lst.append(final_data_need)

    return final_data_lst

def process_system_ToolEyes(input: str)->tuple:
    """ get dataset system

    获得此数据对应的system

    Args:
        input (str): raw_system

    Returns:
        tuple: (final_conversation - list, candidate_tools -- list)

    """
    candidate_tools_str = re.search("\[[\s\S]*\]", input).group(0)
    raw_instruction = input.split("Specifically, you have access of the following tools:\n")[0]
    raw_instruction += "Specifically, you have access of the following tools:\n" + "[candidate_tools]" + "\n\nLet's Begin!"
    candidate_tools = json.loads(candidate_tools_str)
    return (raw_instruction, candidate_tools)

def get_conersation_and_candidate_tools_ToolEyes(conversations: list)->tuple:
    """ get final conversation and candidate tools

    获得最后的多轮对话和候选工具

    Args:
        conversations (list): raw conversation we should deal with

    Returns:
        tuple: (final_conversation, candidate_tools)

    """
    final_conversation = []
    candidate_tools = []
    for conversation in conversations:
        temp_conversation = {}
        if conversation["from"] == "system":
            temp_conversation["role"] = "system"
            instruction, candidate_tools = process_system_ToolEyes(conversation["value"])
            temp_conversation["content"] = instruction
        else:
            temp_conversation["role"] = conversation["from"]
            temp_conversation["content"] = conversation["value"]
        final_conversation.append(temp_conversation)
    return (final_conversation, candidate_tools)


def process_data_ToolEyes(file_path: str)->list:
    """get final data

    将原始数据处理成最终数据

    Args:
        file_path (str):data path

    Returns:
        list: final_data_lst

    """
    all_data = read_JSON(file_path)
    final_data_lst = []
    for data in all_data:
        final_data_need = {}
        final_data_need["id"] = data["id"]
        conversations, candidate_tools = get_conersation_and_candidate_tools_ToolEyes(data["conversations"])
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


def load_data_ToolTalk(folder_path: str, system_prompt: str, all_apis: dict)->list:
    """load data from ToolTalk dataset

    读取原始的Tool_Talk数据

    Args:
        folder_path (str): the folder path of the data
        system_prompt (str): the raw system prompt
        all_apis (dict): all apis

    Returns:
        list: final data list we need

    """
    final_data = []
    raw_data = []
    all_data_file_name = os.listdir(folder_path)
    for filename in all_data_file_name:
        now_data_filename = os.path.join(folder_path, filename)
        now_data = read_JSON(now_data_filename)
        raw_data.append([now_data, filename])

    for data, filename in raw_data:
        temp_data = {}
        temp_data["id"] = filename
        raw_conversations = data["conversation"]
        candidate_api_names = data["apis_used"]
        all_candidate_apis = []
        for candidate_api_name in candidate_api_names:
            all_candidate_apis.append(all_apis[candidate_api_name])
        temp_data["candidate_tools"] = all_candidate_apis
        user_information = data["metadata"]
        if user_information.get("username", -1) == -1:
            username_now = data["user"]["username"]
        else:
            username_now = user_information["username"]
        system_prompt = system_prompt.replace("{location}", user_information["location"])
        system_prompt = system_prompt.replace("{timestamp}", user_information["timestamp"])
        system_prompt = system_prompt.replace("{username}", username_now)

        final_conv = [{"role": "system", "content": system_prompt}]
        for i in raw_conversations:
            temp_conv = {}
            temp_conv["role"] = i["role"]
            temp_conv["content"] = i["text"]
            if i.get("apis", -1) != -1:
                temp_conv["function_call"] = []
                temp_conv["function_result"] = []
                for used_apis in i["apis"]:
                    temp_function_call = {}
                    temp_function_call["name"] = used_apis["request"]["api_name"]
                    temp_function_call["parameters"] = used_apis["request"]["parameters"]
                    if used_apis["response"] != None:
                        temp_function_call["function_result"] = used_apis["response"]
                    else:
                        temp_function_call["function_result"] = used_apis["exception"]
                    temp_conv["function_call"].append(temp_function_call)
            final_conv.append(temp_conv)

        temp_data["conversations"] = final_conv
        query = ""
        for i in final_conv:
            if i["role"] == "user":
                query = i["content"]
                break
        temp_data["query"] = query
        final_data.append(temp_data)
    return final_data

def get_all_tool_and_information_ToolTalk(file_path: str)-> list:
    """ get one tool information

    获得单个python工具的信息

    Args:
        file_path (str): the

    Returns:
        list: tool's information

    """
    apis = []
    with open(file_path, "r") as source_code:
        tree = ast.parse(source_code.read())
    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            attributes = []
            for sub_node in ast.iter_child_nodes(node):
                if isinstance(sub_node, ast.Assign):  # 找到类中的赋值语句
                    for target in sub_node.targets:
                        if isinstance(target, ast.Name):  # 类属性赋值
                            try:
                                value = ast.literal_eval(sub_node.value)
                                attributes.append((target.id, value))
                            except ValueError:  # 如果值不是常量，无法解析
                                attributes.append((target.id, None))

            classes.append((class_name, attributes))

    for api_name, all_parameters in classes:
        now_api = {}
        now_api["name"] = api_name
        for parameter_name, content in all_parameters[:3]:
            if parameter_name == "description":
                now_api["description"] = content
            elif parameter_name == "parameters":
                now_api["parameters"] = content
            elif parameter_name == "output":
                now_api["output"] = content
        if now_api.get("description", -1) != -1 and now_api.get("parameters", -1) != -1 and now_api.get("output",
                                                                                                        -1) != -1:
            apis.append(now_api)

    return apis


def get_tool_information_final_ToolTalk(tool_folder_path: str)->dict:
    """ get all tools information

    获得所有工具的信息，用字典保存

    Args:
         tool_folder_path (str): the folder of all tools

    Returns:
        dict: all tools information

    """
    all_apis = {}
    all_py_file_name = os.listdir(tool_folder_path)
    all_py_file_name.remove("api.py")
    all_py_file_name.remove('exceptions.py')
    all_py_file_name.remove('__init__.py')
    all_py_file_name.remove('utils.py')
    for file_name in all_py_file_name:
        now_data_file = os.path.join(tool_folder_path, file_name)
        return_apis = get_all_tool_and_information_ToolTalk(now_data_file)
        for api in return_apis:
            all_apis[api["name"]] = api
    return all_apis


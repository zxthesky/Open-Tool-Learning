import re
import json


def process_model_response_standard(response: str)->list:
    """process model output to get tools

    从模型的输出中获得调用的tool

    Args:
        response (str): model output

    Returns:
        list: tools information contain name and parameters

    """
    used_tools = re.search("\[[\s\S]*\]", response)
    if used_tools != None:
        used_tool = re.search("\[[\s\S]*\]", response).group(0)
    else:
        return []
    try:
        tools = json.loads(used_tools)
    except:
        print("the format of model's response is wrong")
        tools = []

    return tools


def process_api_bank_response(response: str)->list:
    """ process api bank model response

    处理 api bank 数据集模版下的response

    Args:
        response (str): model output

    Returns:
        list: tools information

    """
    final_tools= []
    try:
        used_tool = re.search("API-Request: \[[\s\S]*\]", response).group(0)
        tool_name = ""
        for i in range(13, len(used_tool)):
            if used_tool[i] != "(":
                tool_name += used_tool[i]
            else:
                break

        parameters = re.search("\([\s\S]*\)", used_tool).group(0)
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
        final_tools.append(function_call)
    except:
        return []

    return final_tools





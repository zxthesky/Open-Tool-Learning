from src.toolagent.model.llm.LLaMA import LLaMA
from src.toolagent.data.one_data import one_data
from src.toolagent.utils import write_JSON
from src.toolagent.process.process_response import process_model_response_standard, process_api_bank_response
from src.toolagent.chat.chat_management import ChatManagementModule
from src.toolagent.process.process_dataset import get_dataset
from src.toolagent.config import Config

import argparse


def get_model(args):
    """get model

    获得模型

    Args:
        args: args

    Return:
        model

    """
    model_name = args.backbone_model
    model_path = args.model_path
    if model_name == "llama3":
        model = LLaMA(checkpoint_path=model_path)
    else:
        model = LLaMA(checkpoint_path=model_path)
    return model



def get_tool_result(response: str)->tuple:
    """ get tool result

    传入模型的输出，将工具提取出来并且获得这个工具调用的结果

    Args:
        response (str): model output

    Returns:
        tuple: tuple (tools, tools' result) the type of them is list

    """
    if args.dataset_name == "API_Bank":
        tools = process_api_bank_response(response)

    else:
        tools = process_model_response_standard(response)

    if tools != None or tools != {}:
        tool_results = []
        if type(tools) == type([]):
            for tool in tools:
                tool_name = tool["name"]
                tool_parameters = tool["parameters"]
                tool_result = "待填充"
                tool_results.append(tool_result)
        else:

            tool_name = tools["name"]
            tool_parameters = tools["parameters"]
            tool_result = "待填充"
            tool_results.append(tool_result)
            tools = [tools]
        return (tools, tool_results)

    return (0, 0)

def inference(model, data: one_data, max_step: int, template:str)->list:
    """one query's inference path

    一条数据的推理过程

    Args:
        model: inference model
        data (one_data): A piece of data
        max_step (int): the max step of model inference
        template (str): the template of the data

    Returns:
        list: the inference result which we use list to contain it

    """
    system = data.system
    query = data.query
    now_chat = ChatManagementModule(system, template)
    now_chat.add_message({"role": "user", "content": query})
    for i in range(max_step):
        input_text = now_chat.get_model_input()
        response = model(input_text)
        temp_data = {}
        temp_data["role"] = "assistant"
        temp_data["content"] = response
        tools, tool_results = get_tool_result(response)
        if tools != 0 or tools != {}:
            temp_data["function_call"] = tools
            temp_data["function_result"] = tool_results
        now_chat.add_message({"role": "assistant", "content": response})

    return now_chat.chat_history

def main(args)->None:
    """the main function

    主要的运行函数

    Args:
        args: args

    Returns:
        None

    """
    config = Config(dataset_name=args.dataset_name,filename=args.data_path,folder_path=args.folder_name, tool_folder_path=args.tool_folder_path)
    model = get_model(args)
    template = model.tokenizer.chat_template
    test_dataset = get_dataset(config)
    output_data_lst = []
    all_data = test_dataset.data

    for data in all_data:
        output_data_dict = {}
        data = one_data(data)
        output_data_dict["id"] = data.id

        conv = inference(model, data, max_step=args.max_step, template=template)
        output_data_dict["conversations"] = conv
        output_data_dict["candidate_tools"] = data.candidate_tools
        output_data_dict["query"] = data.query

        output_data_lst.append(output_data_dict)
    write_JSON(args.output_answer_file, output_data_lst, indent=2)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--backbone_model", type=str, default="llama3", required=False, help='the model you choose')
    parser.add_argument("--model_path", type=str, required=True, help="the path of model parameter")
    parser.add_argument("--dataset_name", type=str, default="default", required=False, help='dataset name you choose, if you want to use api_bank, you can choose it')
    parser.add_argument("--data_path", type=str, default="", required=False, help="The specific path of the data")
    parser.add_argument("--folder_name", type=str, default="", required=False, help="the style of ToolTalk")
    parser.add_argument("--output_answer_file", type=str, required=True, help="output file path")
    parser.add_argument("--tool_folder_path", type=str, default="", required=False, help="the folder path of tool")
    parser.add_argument("--write_file_path", type=str, default="", required=False, help="the processed data path ,you can choose to write or not")
    parser.add_argument("--openai_key", type=str, default="", required=False, help="openai key to use chatgpt")
    parser.add_argument("--eval_mode", type=str, default="all", required=False, help="eval step by step or eval the whole process or both")
    parser.add_argument("--max_step", type=int, default=5, required=False, help="max step the model can infer")
    args = parser.parse_args()

    main(args)


















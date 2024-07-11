from src.otl.model.llm.LLaMA import LLaMA
from src.otl.model.llm.Chatgpt import Chatgpt
from src.otl.data.dataset.API_Bank import API_Bank
from src.otl.data.dataset.ToolEyes import ToolEyes
from src.otl.data.dataset.ToolTalk import ToolTalk
from src.otl.data.dataset.SoAy import SoAy
from src.otl.data.general_dataset import General_dataset
from src.otl.data.one_data import one_data
from src.otl.utils import write_JSON
from src.otl.process.process_response import process_model_response, process_api_bank_response

import argparse


def get_model(args):
    model_name = args.backbone_model
    model_path = args.model_path
    if model_name == "llama3":
        model = LLaMA(checkpoint_path=model_path)
    elif model_name == "gpt":
        model = Chatgpt(api_key=args.openai_key)
    else:
        model = LLaMA(checkpoint_path=model_path)
    return model


def get_data(args):
    if args.dataset_name == "API_Bank":
        test_dataset = API_Bank(mode="test", filename=args.data_path, write_filename=args.write_file_path)
    elif args.dataset_name == "ToolEyes":
        test_dataset = ToolEyes(filename=args.data_path, write_filename=args.write_file_path)
    elif args.dataset_name == "ToolTalk":
        test_dataset = ToolTalk(folder_path=args.folder_name, tool_folder_path=args.tool_folder_path, write_filename=args.write_file_path)
    elif args.dataset_name == "SoAy":
        prompt = ""
        test_dataset = SoAy(folder_path=args.folder_name, tool_folder_path=args.tool_folder_path, prompt=prompt)
    else:
        test_dataset = General_dataset(filename=args.data_path)
    return test_dataset

def get_tool_result(response): # the type of tool is list, it can contain many tools
    if args.dataset_name == "API_Bank":
        tools = process_api_bank_response(response)

    else:
        tools = process_model_response(response)

    if tools != None or tools != {}:
        tool_results = []
        for tool in tools:
            tool_results.append("待填充")
        return tools, tool_results

    return 0, 0

def inference(model, data, max_step):
    conv = []
    system = data.system
    query = data.query
    conv = [{"role": "system", "content": system}, {"role": "user", "content": query}]
    model.change_message([{"role": "system", "content": system}, {"role": "user", "content": query}])
    for i in range(max_step):
        response = model.parse()
        temp_data = {}
        temp_data["role"] = "assistant"
        temp_data["content"] = response
        tools, tool_results = get_tool_result(response)
        if tools != 0 or tools != {}:
            temp_data["function_call"] = tools
            temp_data["function_result"] = tool_results
        model.add_message(temp_data)
        conv.append({"role": "assistant", "content": response})

    return conv

def main(args):
    model = get_model(args)
    test_dataset = get_data(args)
    output_data_lst = []
    all_data = test_dataset.data

    for data in all_data:
        output_data_dict = {}
        data = one_data(data)
        output_data_dict["id"] = data.id

        conv = inference(model, data, max_step=args.max_step)
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


















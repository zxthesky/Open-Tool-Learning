from ..data.general_dataset import General_dataset
from .utils import process_level12_test,process_level3_test,process_train_data_API_Bank,process_data_ToolEyes,load_data_ToolTalk,get_tool_information_final_ToolTalk
from ..config import Config
def get_dataset(config: Config) -> General_dataset:
    """ get dataset according to your dataset name

    根据用户的需求处理对应的数据

    Args:
        config (dict):{"dataset_name": ..., "filepath":..., "tool_folder_path":...,  ............}

    Returns:
        General_dataset: the final dataset we need
    """

    if config.dataset_name == "API_Bank":
        dataset_path = config.filename
        if "test" in dataset_path and ("1" in dataset_path or "2" in dataset_path):
            all_data = process_level12_test(dataset_path)
            return General_dataset.load_data_from_process_data(all_data)
        elif "test" in dataset_path and ("3" in dataset_path):
            all_data = process_level3_test(dataset_path)
            return General_dataset.load_data_from_process_data(all_data)
        elif "train" in dataset_path:
            all_data = process_train_data_API_Bank(dataset_path)
            return General_dataset.load_data_from_process_data(all_data)
        else:
            print("------------  dataset_path is wrong  ------------")
    elif config.dataset_name == "ToolEyes":
        dataset_path = config.filename
        all_data = process_data_ToolEyes(dataset_path)
        dataset = General_dataset.load_data_from_process_data(all_data)
        return dataset
    elif config.dataset_name == "ToolTalk":
        dataset_folder_path = config.folder_path
        tool_folder_path = config.tool_folder_path
        system_prompt = "You are a helpful assistant. Here is some user data:" \
                        "\nlocation: {location}" \
                        "\ntimestamp: {timestamp}" \
                        "\nusername (if logged in): {username}"
        all_tools = get_tool_information_final_ToolTalk(tool_folder_path)
        all_data = load_data_ToolTalk(dataset_folder_path, system_prompt, all_tools)
        dataset = General_dataset.load_data_from_process_data(all_data)

        return  dataset
    elif config.dataset_name == "SoAy":
        pass
    elif config.dataset_name == "default":
        dataset_path = config.filename
        dataset = General_dataset.load_data_from_single_file(dataset_path)
        return dataset
    else:
        print("no such dataset")















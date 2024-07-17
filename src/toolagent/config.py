
class Config:
    """some file path

    该类提供了一些配置，如数据的路径，工具的路径等等

    Attributes:
        dataset_name (str): the dataset name
        filepath (str): if all data in a file, we pass the filepath
        folder_path (str): if one file corresponding to one data ,and all data contain in a folder, pass the folder path
        tool_folder_path (str): the folder path of the tool

    """
    def __init__(self,dataset_name: str="", filename: str="", folder_path: str="", tool_folder_path: str=""):
        self.dataset_name = dataset_name
        self.filename = filename
        self.folder_path = folder_path
        self.tool_folder_path = tool_folder_path



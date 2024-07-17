from ..utils import read_JSON,write_JSON
import json

class General_dataset:
    """ dataset General_dataset

        统一的数据集格式

        Attributes:
            data (list): final data list

        Example:
            >>> dataset = General_dataset.load_data_from_single_file("")

        """
    def __init__(self, data: list):
        self.data = data
    @classmethod
    def load_data_from_single_file(cls, file_path: str):
        """ The file name of the data format standard needs to be passed in

        传入数据格式标准的文件名

        Args:
            file_path (str): file path

        Returns:
            General_dataset: final dataset

        """
        all_data = read_JSON(file_path)
        dataset = General_dataset(all_data)
        return dataset
    @classmethod
    def load_data_from_process_data(cls, data: list):
        """ pass in processed data

        传入处理好的数据

        Args:
            data (list): final processed data

        Returns:
            General_dataset: final dataset

        """
        dataset = General_dataset(data)
        return dataset



if __name__ == "__main__":
    print("dsadas")




import ast
import csv
import json
import os
import re
from typing import Dict, Set, Tuple, Optional, List, Any, Type



class VariableExtractor(ast.NodeVisitor):
    """This class is used to extract variable names and their values from a Python source code using the Abstract Syntax Tree (AST).

    Attributes:
        variables (Dict[str, Any]): A dictionary that stores variable names as keys and their corresponding values as values.

    Example:
        extractor = VariableExtractor()
        extractor.visit(ast.parse("a = 10\nb = 'hello'"))
        print(extractor.variables)  # Output: {'a': 10, 'b': 'hello'}
    """
    def __init__(self):
        self.variables = {}

    def visit_Assign(self, node):
        """Visits an Assign node in the AST and extracts variable names and their values.

        Args:
            node (ast.Assign): The Assign node in the AST.

        Returns:
            None
        """
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                try:
                    var_value = ast.literal_eval(node.value)
                    self.variables[var_name] = var_value
                except ValueError:
                    pass
                

def get_APIbank_tool_info_from_csv(tool_path: str) -> List[Dict[str, Any]]:
    """Extracts tool information from the CSV file of the APIbank dataset which contains API details.

    Args:
        tool_path (str): The path to the CSV file containing the API details, example: xxx/data/all_apis.csv

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing the details of an API tool.
    """
    
    tool_lst=[]

    with open(tool_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            
            try:
                api_description = row['api_info'].split('description = ')[1].split('\n')[0].strip('"')
            except:
                api_description = ""
                
            tool_info = {
                "name": row["类名"],
                "description": api_description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": "UNK"
                },
                "responses": {
                    "type": "object",
                    "properties": {}
                }
            }
   
            
            try:
                parts = row["api_info"].split('\noutput_parameters = ')
                input_part = parts[0].split('input_parameters = ')[1].strip()
                output_part = parts[1].strip()


                input_parameters = ast.literal_eval(input_part)
                output_parameters = ast.literal_eval(output_part)
                
                tool_info["parameters"]["properties"] = input_parameters
                tool_info["responses"]["properties"] = output_parameters
                
            except:
                pass
        
            tool_lst.append(tool_info)
    
    return tool_lst
            

def get_APIbank_tool_info_from_py(dir_path: str) -> List[Dict[str, Any]]:
    """Extracts tool information from Python files in the tool directory of the APIbank dataset.

    Args:
        dir_path (str): The path to the directory containing the Python files, example: "xxx/apis", "xxx/lv3_apis"

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing the details of an API tool.
    """
    
    tool_lst = []
    except_files = ['__init__.py', 'api.py']
    for subpath in os.listdir(dir_path):
        if subpath.endswith('.py') and subpath not in except_files:
            file_path = dir_path + "/" + subpath
            with open(file_path, 'r') as file:
                content = file.read()

            class_match = re.search(r"class (\w+)\(API\):([\s\S]*?)def __init__\(", content)

            try:
                if class_match:
                    tool_name = class_match.group(1)
                    remain = class_match.group(2)
                
                code_lines = remain.strip().split('\n')
                dedented_code_lines = [line.lstrip() for line in code_lines]
                dedented_code_text = '\n'.join(dedented_code_lines)
                
                
                tree = ast.parse(dedented_code_text)
                extractor = VariableExtractor()
                extractor.visit(tree)

                description = extractor.variables.get('description')
                parameters_value = extractor.variables.get('parameters')
                output_value = extractor.variables.get('output')

                tool_info = {
                    "name": tool_name,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": parameters_value,
                        "required": "UNK"
                    },
                    "responses": {
                        "type": "object",
                        "properties": output_value,
                    }
                }
            
            except:
                tool_info = {
                    "name": tool_name,
                    "description": "UNK",
                    "parameters": {
                        "type": "object",
                        "properties": "UNK",
                         "required": "UNK"
                    },
                    "responses": {
                        "type": "object",
                        "properties": "UNK",
                    }
                }
            tool_lst.append(tool_info)
        
    return tool_lst


def get_Tooleyes_tool_info_from_py(dir_path: str) -> List[Dict[str, Any]]:
    """Extracts tool information from Python files in the tool directory of the Tooleyes dataset.

    Args:
        dir_path (str): The path to the directory containing the Python files, example: "xxx/Tool_Library"

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing the details of an API tool.
    """
    
    tool_lst = []
   
    for sub_path in os.listdir(dir_path):
        
        for sub_sub_path in os.listdir(dir_path + "/" + sub_path):
        
            file_path = dir_path + "/" + sub_path + "/" + sub_sub_path + "/config_gpt4.json"
            with open(file_path, 'r') as file:
                tools = json.load(file)

            for tool in tools:
                tool["responses"] = {"type": "object", "properties": "UNK"}
                tool_lst.append(tool)
        
    return tool_lst

def get_Tooltalk_tool_info_from_py(dir_path: str) -> List[Dict[str, Any]]:
    """Extracts tool information from Python files in the tool directory of the Tooltalk dataset.

    Args:
        dir_path (str): The path to the directory containing the Python files, example: "xxx/src/tooltalk/apis"

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing the details of an API tool.
    """

    tool_lst = []
    except_files = ['__init__.py', 'api.py', 'utils.py', 'exceptions.py']
   
    for subpath in os.listdir(dir_path):
        if subpath.endswith('.py') and subpath not in except_files:
            file_path = dir_path + "/" + subpath
            with open(file_path, 'r') as file:
                content = file.read()
            apis = content[content.rfind("[")+1:content.rfind("]")].strip().split(",")
            for api in apis:
                tool_name = api.strip()
                if tool_name != "":
                    class_match = re.search("class " + tool_name + "\(.*?\):([\s\S]*?)def call\(", content)
                    remain = class_match.group(1)
                    code_lines = remain.strip().split('\n')
                    dedented_code_lines = [line.lstrip() for line in code_lines]
                    dedented_code_text = '\n'.join(dedented_code_lines)
                    
                    
                    tree = ast.parse(dedented_code_text)
                    extractor = VariableExtractor()
                    extractor.visit(tree)

                    # 提取值
                    description = extractor.variables.get('description')
                    parameters_value = extractor.variables.get('parameters')
                    output_value = extractor.variables.get('output')
                    
                    #转化格式并且识别required参数
                    required = []
                    new_parameters = {}
                    for key,value in parameters_value.items():
                        if value["required"]:
                            required.append(key)
                        del[value["required"]]
                        new_parameters[key] = value
                    
                    tool_info = {
                        "name": tool_name,
                        "description": description,
                        "parameters": {
                            "type": "object",
                            "properties": new_parameters,
                            "required": required
                        },
                        "responses": {
                            "type": "object",
                            "properties": output_value
                        }
                    }
                    
                    tool_lst.append(tool_info)
                
    return tool_lst

    
                    
                    
if __name__ == '__main__':
    pass
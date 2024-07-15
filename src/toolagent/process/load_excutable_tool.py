import re
import json
import os
from typing import Dict, Set, Tuple, Optional, List, Any, Type

from tool.tool import SysTool
from ....doc.API.apibank.apis.api import API
from ....doc.API.tooltalk.apis import ALL_APIS
from ....doc.API.tooltalk.apis.account import ACCOUNT_DB_NAME, DeleteAccount, UserLogin, LogoutUser, RegisterUser

class BasicLoader:

    def __init__(self) -> None:
        pass

    def load_executable_tools(self):
        pass

    def get_executable_tools(self):
        pass

class APIbankLoader(BasicLoader):
    def __init__(self, apis_dir: str, database_dir: str):
        """Initialize the APIbankLoader with the directories for APIs and databases.

        Args:
            apis_dir (str): The directory path where the API files are stored.
            database_dir (str): The directory path where the initial database files are stored.
        """
        self.apis_dir = apis_dir  # xx/api-bank/lv3_apis
        self.database_dir = database_dir # xx/api-bank/init_database
        
        self.apis = list()
        self.init_databases = dict()
        self.inited_tools = dict() # the dict for callable module
        self.token_checker = None
        self.executable_tools = dict() # the dict for SysTool class
        self.load_executable_tools()
        
    
    def load_executable_tools(self) -> None:
        """Loads executable tools from the specified directories.

        This method imports all Python files in the APIs directory, loads all classes,
        and initializes them if they are subclasses of API. It also loads initial databases
        from the database directory.

        Returns:
            None
        """
        import importlib.util

        all_apis = []
        # import all the file in the apis folder, and load all the classes
        except_files = ['__init__.py', 'api.py']
        for file in os.listdir(self.apis_dir):
            if file.endswith('.py') and file not in except_files:
                api_file = file.split('.')[0]
                basename = os.path.basename(self.apis_dir)
                module = importlib.import_module(f'{basename}.{api_file}')
                classes = [getattr(module, x) for x in dir(module) if isinstance(getattr(module, x), type)]
                for cls in classes:
                    if issubclass(cls, API) and cls is not API:
                        all_apis.append(cls)

        classes = all_apis

        init_database_dir = self.database_dir
        for file in os.listdir(init_database_dir):
            if file.endswith('.json'):
                database_name = file.split('.')[0]
                with open(os.path.join(init_database_dir, file), 'r') as f:
                    self.init_databases[database_name] = json.load(f)

        # Get the description parameter for each class
        for cls in classes:
            if issubclass(cls, object) and cls is not object:
                name = cls.__name__
                cls_info = {
                    'source': "APIbank",
                    'name': name,
                    'class': cls,
                    'description': cls.description,
                    'input_parameters': cls.input_parameters,
                    'output_parameters': cls.output_parameters,
                    'callable': True,
                    'remote': False,
                }
                
                if hasattr(cls, 'database_name') and cls.database_name in self.init_databases:
                    cls_info['database'] = self.init_databases[cls.database_name]
                
                self.executable_tools[cls_info["name"]] = SysTool(**cls_info)  
                
                self.apis.append(cls_info)
        
        
        for cls_info in self.apis:
            self.init_tool(cls_info["name"])
        
        for key, value in self.executable_tools.items():
            value["module"] = self.inited_tools[key]
            self.executable_tools[key] = value
        
        if 'CheckToken' in [api['name'] for api in self.apis]:
            self.token_checker = self.inited_tools["CheckToken"] #change the value of the self.token_checker
            
        
        # return self.executable_tools
            
    def get_api_by_name(self, name: str) -> Dict[str, Any]:
        """Gets the API with the given name.

        Parameters:
            name (str): the name of the API to get.

        Returns:
            api (dict): the API with the given name.
        """
        for api in self.apis:
            if api['name'] == name:
                return api
        raise Exception('invalid tool name.')
    

    def init_tool(self, tool_name: str, *args, **kwargs):
        """Initializes a tool with the given name and parameters.

        Parameters:
            tool_name (str): the name of the tool to initialize.
            args (list): the positional arguments to initialize the tool with.
            kwargs (dict): the parameters to initialize the tool with.

        Returns:
            tool (object): the initialized tool.
        """
        # Get the class for the tool
        api_class = self.get_api_by_name(tool_name)['class']#gte the class of the excutable tool
        temp_args = []

        if 'init_database' in self.get_api_by_name(tool_name):
            # Initialize the tool with the init database
            temp_args.append(self.get_api_by_name(tool_name)['init_database'])
        
        if tool_name != 'CheckToken' and 'token' in self.get_api_by_name(tool_name)['input_parameters']:
            temp_args.append(self.token_checker)

        args = temp_args + list(args)
        tool = api_class(*args, **kwargs)

        self.inited_tools[tool_name] = tool
        return tool
    
    def get_executable_tools(self) -> Dict[str, SysTool]:
        """Return the dictionary of executable tools.

        Returns:
            Dict[str, SysTool]: A dictionary where keys are tool names and values are SysTool instances.
        """
        return self.executable_tools
        
    def test(self): # test sample
        mode = 'function_call' 
        if mode == 'qa':
            while True:
                tool_keywords = input('Please enter the keywords for the tool you want to use (\'exit\' to exit):\n')
                tool_searcher = self.executable_tools['ToolSearcher']
                d = {"module": self.inited_tools['ToolSearcher'], "param_dict": {"keywords": tool_keywords}}
                response = tool_searcher(**d)
                api_name = response['output']['name'] 
                
                api_name = "QueryMeeting"
                param_dict = {"user_name": "John"}
                    
                if api_name not in self.executable_tools:
                    raise Exception('Tool is not within the scope of executable tools')
                else:
                    t = self.executable_tools[api_name]
                    d = {"module": self.inited_tools[api_name], "param_dict": param_dict}
                    d = {"param_dict": param_dict}
                    result = t(**d)
                    return result
                        
        elif mode == 'function_call':
            while True:
                command = "API-Request: [ToolSearcher(keywords='QueryMeeting')]"
                command = "API-Request: [QueryMeeting(user_name='John')]"
                
                api_name = "QueryMeeting"
                param_dict = {"user_name": "John"}
            
                if api_name not in self.executable_tools:
                    raise Exception('Tool is not within the scope of executable tools')
                else:
                    t = self.executable_tools[api_name]
                    # d = {"module": self.inited_tools[api_name], "param_dict": param_dict}
                    d = {"param_dict": param_dict} # By default, only parameter dict needs to be passed in
                    result = t(**d)
                    return result
    
    

class TooleyesLoader(BasicLoader):
    def __init__(self, apis_dir: str) -> None:
        """Initialize the TooleyesLoader with the directory containing the APIs.

        Args:
            apis_dir (str): The directory path where the API tools are stored.
        """
        self.apis_dir = apis_dir # /public/home/wlchen/hhan/my-tool-learning/Open-Tool-Learning/src/otl/tooleyes/Tool_Library
        self.executable_tools = dict()
        self.load_executable_tools()
        
    
    def load_executable_tools(self) -> None: #Tooleyes需要进行同名API排查
        """Load executable tools from the specified directory and subdirectories.

        This method iterates through the directories and subdirectories to find JSON configuration files
        for tools. It then loads these tools into the `executable_tools` dictionary, ensuring that
        tools with the same name are grouped together in a list.

        Returns:
            None
        """
   
        for sub_path in os.listdir(self.apis_dir):
            
            for sub_sub_path in os.listdir(self.apis_dir + "/" + sub_path):
            
                file_path = self.apis_dir + "/" + sub_path + "/" + sub_sub_path + "/config_gpt4.json"
                callable_path = self.apis_dir + "/" + sub_path + "/" + sub_sub_path + "/tool.py"
                with open(file_path, 'r') as file:
                    tools = json.load(file)

                for tool in tools:
                    name = tool["name"]
                    if name not in ["ask_to_user", "finish"]:
                        cls_info = {
                            'source': "Tooleyes",
                            'name': name,
                            'description': tool["description"],
                            'input_parameters': tool["parameters"]["properties"],
                            'output_parameters': None,
                            'callable': True,
                            "required" : tool["parameters"]["required"],
                            'remote': None,
                            "py_path": callable_path
                        }
                    if name not in self.executable_tools:
                        self.executable_tools[name] = [SysTool(**cls_info)]
                    else:
                        self.executable_tools[name].append(SysTool(**cls_info))
        
        # return self.executable_tools
    
    
    def get_executable_tools(self) -> Dict[str, List[SysTool]]:
        """Return the dictionary of executable tools.

        This method returns the `executable_tools` dictionary, which contains tool names as keys
        and lists of `SysTool` instances as values.

        Returns:
            Dict[str, List[SysTool]]: A dictionary where each key is a tool name and the value is a list
            of `SysTool` instances with the same tool name.
        """
        return self.executable_tools
    
    def test(self): #test sample
        
        test_sample = {
        "id": "Turn 1: I'm in need of assistance in generating a random string with a length of 8,please give me one.",
        "conversations": [
            {
                "from": "system",
                "value": "the prompt of conversation"
            },
            {
                "from": "user",
                "value": "I'm in need of assistance in generating a random string with a length of 8,please give me one."
            }
        ],
        "path": "ToolEyes/Tool_Library/Random/Random",
        "scenario": "TG"
        }
        
        api_name = ""
        input_parameters = {}
        path_in_dataset = test_sample["path"].replace("ToolEyes/", "")
        
        import_path = "Open-Tool-Learning/docs/API/tooleyes/" + path_in_dataset
        
        
        if api_name not in self.executable_tools:
            raise Exception('Tool is not within the scope of executable tools')
        else:
            for api in self.executable_tools[api_name]:
                callable_path = api.callable_path
                if re.search(path_in_dataset, callable_path):
                    d = {"func_name": api_name, "param_dict": input_parameters, "py_path": import_path}
                    d = {"param_dict": input_parameters}
                    result = api(**d)
                    return result
        


class TooltalkLoader(BasicLoader):
    def __init__(self, init_database_dir: str, ignore_list: Optional[List], account_database: Optional[str]) -> None:
        """Initialize the TooltalkLoader with the directory containing the initial databases, an optional ignore list, and an optional account database name.

        Args:
            init_database_dir (str): The directory path where the initial databases are stored.
            ignore_list (Optional[List]): A list of API names to ignore.
            account_database (Optional[str]): The name of the account database.
        """
        self.init_database_dir = init_database_dir
        self.ignore_list = ignore_list if ignore_list is not None else list()
        self.account_database = account_database if account_database is not None else ACCOUNT_DB_NAME # ACCOUNT_DB_NAME = "Account"
        
        self.databases = dict()
        self.database_files = dict()
        self.session_token = None
        self.inited_tools = dict() 
        self.now_timestamp = None
        self.apis = {api.__name__: api for api in ALL_APIS if api.__name__ not in self.ignore_list}
        self.executable_tools = dict() #the dict for SysTool class
        
        for file_name, file_path in self.get_names_and_paths(self.init_database_dir):
            database_name, ext = os.path.splitext(file_name)
            if ext == ".json":
                self.database_files[database_name] = file_path
                with open(file_path, 'r', encoding='utf-8') as reader:
                    self.databases[database_name] = json.load(reader)
        if self.account_database not in self.databases:
            raise ValueError(f"Account database {self.account_database} not found")
        
        self.load_executable_tools()


    def load_executable_tools(self) -> None:
        """Load executable tools from the APIs.
        
        Returns:
            None
        """
        for key, value in self.apis.items():
            self.init_tool(key)
            
        for api_name, cls in self.apis.items():
            description = cls.description
            input_parameters = {}
            output_parameters = cls.output
            required = []
            for k, v in cls.parameters.items():
                if v["required"]:
                    required.append(k)
                del v["required"]
                input_parameters[k] = v
            cls_info = {
                    'source': "Tooltalk",
                    'name': api_name,
                    'class': cls,
                    'description': description,
                    'input_parameters': input_parameters,
                    'output_parameters': output_parameters,
                    'callable': True,
                    'remote': None,
                    'required': required,
                    'module': self.inited_tools.get(api_name, None)
                }
            if hasattr(cls, 'database_name') and cls.database_name in self.databases:
                cls_info['database'] = self.databases[cls.database_name]
            
            self.executable_tools[api_name] = SysTool(**cls_info)
        
        # return self.executable_tools
            

    def init_tool(self, tool_name: str) -> object:
        """Initialize a tool with the given name.

        Args:
            tool_name (str): The name of the tool to initialize.

        Returns:
            tool (object): The initialized tool class.
        """
        cls = self.apis[tool_name]
        account_db = self.databases.get(self.account_database)
        if cls.database_name is not None:
            database = self.databases.get(cls.database_name)
            tool = cls(
                account_database=account_db,
                now_timestamp=self.now_timestamp,
                api_database=database,
            )
        else:
            tool = cls(
                account_database=account_db,
                now_timestamp=self.now_timestamp,
            )

        self.inited_tools[tool_name] = tool
        return tool
    
    def get_executable_tools(self) -> Dict[str, SysTool]:
        """Return the dictionary of executable tools.

        Returns:
            Dict[str, SysTool]: A dictionary where keys are tool names and values are SysTool instances.
        """
        return self.executable_tools
    
    def get_names_and_paths(self, input_path) -> List[Tuple[str, str]]:
        """Retrieve file names and their paths from the given input path.

        Args:
            input_path (str): The path to the directory or file.

        Returns:
            List[Tuple[str, str]]: A list of tuples where each tuple contains a file name and its path.
        """
        if os.path.isdir(input_path):
            files = os.listdir(input_path)
            file_paths = [os.path.join(input_path, name) for name in files]
            file_names_and_paths = [(name, path) for name, path in zip(files, file_paths)]
            return file_names_and_paths
        elif os.path.isfile(input_path):
            return [(os.path.basename(input_path), input_path)]
        else:
            raise ValueError(f"Unknown input path: {input_path}")
    
    def test(self): # test sample
        api_name = "QueryUser"
        param_dict = {"usename": "justinkool", "email": "justintime@fmail.com"}
        request = {
            "api_name":  api_name,
            "parameters":  param_dict
        }
        if api_name not in self.apis:
            response = {
                "response": None,
                "exception": f"API {api_name} not found"
            }
            return request, response
        if api_name not in self.executable_tools:
            response = {
                "response": None,
                "exception": f"Tool is not excutable"
            }
            return request, response

        tool_module = self.inited_tools[api_name]
        t = self.executable_tools[api_name]
 
        d = {"module":  tool_module, "param_dict": param_dict}
        d = {"param_dict": param_dict}
        result = t(**d)
        return result
                      

if __name__ == "__main__":
    pass
import json
import os
import re
from typing import Dict, Set, Tuple, Optional, List, Any, Type



class SysTool:
    """This class is used to define the overall tool class SysTool, which inherits BasicTool.

    Attributes:
        name (str): the name of the tool, which must be passed in
        source (str): the dataset source of the tool, if not given, set to None
        description (str): the description of the tool, if not given, set to None
        input_parameters (Dict[str, Any]): the detailed information of the input parameters, if not given, set to None
        output_parameters (Dict[str, Any]): the detailed information of the output parameters, if not given, set to None
        required (List[str]): the list of the names of the requried input parameters, if not given, set to None
        callable (bool): whether the tool is executable, if not given, set to None
        module (Type): an executable module that defines a .call method, if not given, set to None
        py_path (str): the path to the Python file where the tool is located, if not given, set to None
        remote (bool): whether the tool is called through a remote URL, if not given, set to None
        database (Dict[str, Any]): the database information of the tool, if not given, set to None
            

    Example:
        pass
    """
    
    def __init__(self, **args: Dict[str, Any]) -> None:
        """Initialize the SysTool class with the given information.

        Args:
            **args (Dict[str, Any]): a dict shaped like {'name': ..., 'description': ..., 'input_parameters': ..., ...}
        
        Raises:
            AssertionError: the passed args lack the tool name
            Exception: miss the necessary instructions to execute this tool

        Returns:
            None
        """
        
        assert "name" in args
        self.name: str = args.get("name")
        self.source: Optional[str] = args.get("source", None)
        self.description: Optional[str] = args.get("description", None)
        self.input_parameters: Optional[Dict[str, Any]] = args.get("input_parameters", None)
        self.output_parameters: Optional[Dict[str, Any]] = args.get("output_parameters", None)
        self.required: Optional[List[str]] = args.get("required", None)
        self.callable: Optional[bool] = args.get("callable", None)
        self.module: Optional[Type] = args.get("module", None)
        self.py_path: Optional[str] = args.get("py_path", None)
        self.remote: Optional[bool] = args.get("remote", None)  
        self.database: Optional[Optional[Dict[str, Any]]] = args.get("database", None)
        
        if self.callable:
            if not (self.module or self.py_path):
                raise Exception("miss the necessary instructions to execute this tool")
                
        

    def __call__(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Implement the calling part of the class.

        Args:
            **kwargs (Dict[str, Any]): A dict contains the required information of 
        
        Raises:
            pass

        Returns:
            result: a dict contains the information of the calling, successful return is shaped like {"response": ...}, while the unsuccessful return is shaped like {"error": ...}
        """
        
        # allow passing in new py paths or modules to overwrite predefined information when calling
        module = kwargs.get("module", None) if kwargs.get("module", None) is not None else self.module
        py_path = kwargs.get("py_path", None) if kwargs.get("py_path", None) is not None else self.py_path
        param_dict = kwargs.get("param_dict", None)
        func_name = kwargs.get("func_name", None) if kwargs.get("func_name", None) is not None else self.name # use the tool name as the default reference module name
        
        if module: # determine whether the module has a .call method
            if not (hasattr(module, 'call') and callable(module.call)):
                module = None
            
        if module and py_path:
            result = self.execute_tool_from_module(module, param_dict)
            if result.get("error"):
                another_result = self.execute_tool_from_py(py_path, param_dict, func_name)
                if another_result.get("error"):
                    error_message = {"error": "Error occurs during trying module: {}, error occurs during trying python_path: {}".format(result["error"], another_result["error"])}
                    return error_message           
                else:
                    return another_result
            else:
                return result
                    
        elif module and not py_path:
            result = self.execute_tool_from_module(module, param_dict)
            return result
        
        elif py_path and not module:
            result = self.execute_tool_from_py(py_path, param_dict, func_name)
            return result
            
        else:
            return {"error": "miss the necessary instructions to execute this tool"}
        
            
    def execute_tool_from_module(self, module: Optional[Type], param_dict: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute the tool from the callable module

        Args:
            module (Type): the module with .call method
            param_dict (Dict[str, Any]): parameters required to execute the tool

        Returns:
            result: a dict contains the information of the calling, successful return is shaped like {"response": ...}, while the unsuccessful return is shaped like {"error": ...}
        """
        try:
            result = module.call(**param_dict)
            return {"response": result}
        except Exception as e:
            return {"error": str(e)}
        
    def execute_tool_from_py(self, py_path: Optional[str], param_dict: Optional[Dict[str, Any]], func_name: Optional[str]) -> Dict[str, Any]:
        """Execute the tool from the callable module

        Args:
            module (Type): the module
            param_dict (Dict[str, Any]): parameters required to execute the tool

        Returns:
            result: a dict contains the information of the calling, successful calling return is shaped like {"response": ...}, while the unsuccessful calling return is shaped like {"error": ...}
        """
        # example: Open-Tool-Learning/data/dependency/tooleyes/Tool_Library/Advice/Advice_slip/tool.py
        # Pass in an absolute py_path for checking and parsing
        
        current_file_path = "Open-Tool-Learning/src/toolagent/tool/xxx.py"
        try: 
            target_file_path = re.search(r"Open-Tool-Learning/.*", py_path).group(0)
            
            current_dir = os.path.dirname(current_file_path)
            target_dir = os.path.dirname(target_file_path)
            relative_path = os.path.relpath(target_dir, current_dir)
            import_path = relative_path.replace(os.sep, '.')
            module_name = os.path.basename(target_file_path).replace('.py', '')
            if relative_path.startswith('..'):
                relative_depth = relative_path.split(os.sep).count('..')
                import_path = import_path.lstrip('.')
                relative_import = '.' * relative_depth + import_path
            elif relative_path == '.':
                relative_import = module_name
            else:
                relative_import = import_path
            
            # f"from .{relative_import}.{module_name} import {func_name}"
            # from ..dependency.tooleyes.Tool_Library.Random.Random.tool import random
            
            exec(
                f"""from .{relative_import}.{module_name} import {func_name}""")
            result = eval(func_name)(param_dict)
            # result = json.dumps(result, ensure_ascii=False)
            return {"response": result}
        except Exception as e:
            return {"error": str(e)}
                

    def __eq__(self, other):
        # if isinstance(other, class_name):
        #     return self.name == other.name
        # return False
        raise NotImplementedError

    def __hash__(self):
        # return hash((self.name, self.description))
        raise NotImplementedError
    
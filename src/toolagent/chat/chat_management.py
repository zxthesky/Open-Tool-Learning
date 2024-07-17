from ._prototype import BasicChatManagementModule
from jinja2 import Template


class ChatManagementModule(BasicChatManagementModule):
    """ Chat management

    管理对话，利用template将多轮对话转化为模型的输入，同时存储历史信息

    Attributes:
        system_message (str): raw system_message
        chat_history (list): the history of conversation
        chat_template (str): the template of model

    Examples:
        >>> template = "your model chat template"
        >>> system = "you are helpful assistant..."
        >>> now_chat = ChatManagementModule(system, template)
        >>> now_chat.add_message({"role":"user", "content":"your first query"})

    """
    def __init__(self, system_message: str, template: str) -> None:
        self.system_message: str = system_message

        self.chat_history: list = []
        self.chat_template: str = template
        self.clear_history()

    def add_message(self, data: dict)->None:
        """ add history data

        加入历史信息

        Args:
            data (dict): history information

        Returns:
            None

        """
        self.chat_history.append(data)

    def clear_history(self) -> None:
        """clear history information

        清空历史信息


        Returns:
            None

        """
        self.chat_history = [{"role": "system", "content": self.system_message}]

    def delete_last_message(self)->None:
        """delete final messagge

        删掉最后一个历史信息

        Returns:
            None

        """
        self.chat_history.pop(-1)

    def get_model_input(self)->str:
        """get model input text

        利用template获得模型的输入文本

        Returns:
            str: final model input text

        """

        tmpl = Template(self.chat_template)
        ret = tmpl.render(
           messages=self.chat_history
        )
        return ret

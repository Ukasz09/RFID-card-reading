import app.utils as utils
from app.terminal import Terminal


class TerminalManagement:
    def __init__(self, terminal_paths):
        self.__terminals_list = self.__make_terminals(terminal_paths)

    def __make_terminals(self, terminal_paths):
        terminals_list_of_dic = utils.read_json_data(terminal_paths)
        terminals_list = []
        for term_dic in terminals_list_of_dic:
            terminals_list.append(Terminal(term_dic["id"]))
        return terminals_list

    def get_terminals_list(self):
        return self.__terminals_list

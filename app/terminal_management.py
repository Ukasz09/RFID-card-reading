from app.exceptions.server_exceptions import DataInputError

#todo: nie potrzebne?
class TerminalManagement:
    def __init__(self, terminals_dict=None):
        if terminals_dict is None:
            terminals_dict = {}
        self.__terminals_dict = terminals_dict

    def add_terminal(self, terminal):
        self.__terminals_dict[terminal.term_id] = terminal

    def remove_terminal(self, term_id):
        if term_id in self.__terminals_dict:
            del self.__terminals_dict[term_id]
        else:
            raise DataInputError("Terminal with id: " + term_id + " not exist")

    def get_terminals_list(self):
        return self.__terminals_dict.values()

class TerminalManagement:
    def __init__(self, database_connection):
        self.database_connection = database_connection
        self.__terminals_list = database_connection.make_terminals()

    def add_terminal(self, terminal):
        print(self.__terminals_list)
        self.__terminals_list.append(terminal)
        self.database_connection.save_terminals(self.__terminals_list)

    def get_terminals_list(self):
        return self.__terminals_list

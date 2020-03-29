from app.terminal_management import TerminalManagement
from app.terminal import Terminal
from app.database_connection.local_using_json import LocalDatabase

terminal_json_path = "../data/terminals.json"

if __name__ == "__main__":
    database = LocalDatabase(terminal_json_path)
    terminal_management = TerminalManagement(database)
    terminal_management.add_terminal(Terminal("909090"))
    print(*terminal_management.get_terminals_list())

from app.terminal_management import TerminalManagement

if __name__ == "__main__":
    terminal_management = TerminalManagement("terminals.json")
    print(*terminal_management.get_terminals_list())


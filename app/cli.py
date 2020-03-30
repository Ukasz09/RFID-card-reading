from enum import Enum
from collections import namedtuple

# SERVER
CHOOSE_MENU_OPTION_MSG = "Choose menu option: "
UNKNOWN_OPTION_MSG = "Given unknown menu option"

# CLIENT
TERMINAL_ID_CHOOSE_MSG = "Enter terminal id: "
CARD_SCAN_PROMPT_MSG = "Scan your RFID card"
CARD_SCANNED_PROPERLY_MSG = "Card scanned properly"
CARD_USAGE_REGISTERED_MSG = "Saved in database usage of RFID card"
UNKNOWN_CARD_OWNER_MSG = "Card owner unknown"
CARD_OWNER_IS_KNOWN_MSG = "Card owner: "
NOT_REGISTERED_ANY_TERMINAL_MSG = "Not found any registered terminal in database. Ask server admin for adding one: "
NEW_SESSION_SEPARATOR_MSG = "\n___________________________________________________________________________________\n"
WAIT_WITH_EXIT_MSG = "Press any key to exit"
NOT_FOUND_TERMINAL_MSG = "Terminal not assigned in database"


def read_data(prompt=""):
    return input(prompt)


def show_msg(msg):
    print(msg)


class ServerMenu(Enum):
    ServerMenuTuple = namedtuple('Menu', ['number', 'display_string'])

    @property
    def display_string(self):
        return self.value.display_string

    @property
    def number(self):
        return self.value.number

    add_terminal = ServerMenuTuple(1, "Add new terminal to database")
    remove_terminal = ServerMenuTuple(2, "Remove terminal to database")
    add_worker = ServerMenuTuple(3, "Add worker to database")
    remove_worker = ServerMenuTuple(4, "Remove worker from database")
    add_card_to_worker = ServerMenuTuple(5, "Add card to worker")
    remove_worker_card = ServerMenuTuple(6, "Remove card from worker")
    exit_menu = ServerMenuTuple(7, "Exit - press enter without giving any text to console")


def show_server_menu():
    print(NEW_SESSION_SEPARATOR_MSG)
    print(ServerMenu.add_terminal.number, ServerMenu.add_terminal.display_string, sep=") ")
    print(ServerMenu.remove_terminal.number, ServerMenu.remove_terminal.display_string, sep=") ")
    print(ServerMenu.add_worker.number, ServerMenu.add_worker.display_string, sep=") ")
    print(ServerMenu.remove_worker.number, ServerMenu.remove_worker.display_string, sep=") ")
    print(ServerMenu.add_card_to_worker.number, ServerMenu.add_card_to_worker.display_string, sep=") ")
    print(ServerMenu.remove_worker_card.number, ServerMenu.remove_worker_card.display_string, sep=") ")
    print(ServerMenu.exit_menu.number, ServerMenu.exit_menu.display_string, sep=") ")
    print(NEW_SESSION_SEPARATOR_MSG)

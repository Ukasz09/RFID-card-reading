from enum import Enum
from collections import namedtuple

# CLIENT
TERMINAL_ID_INPUT_MSG = "Enter terminal id: "
TERMINAL_NAME_INPUT_MSG = "Enter terminal name: "
CARD_SCAN_PROMPT_MSG = "Scan your RFID card"
CARD_SCANNED_PROPERLY_MSG = "Card scanned properly"
CARD_USAGE_REGISTERED_MSG = "Saved in database usage of RFID card"
UNKNOWN_CARD_OWNER_MSG = "Card owner unknown"
CARD_OWNER_IS_KNOWN_MSG = "Card owner: "
NOT_REGISTERED_ANY_TERMINAL_MSG = "Not found any registered terminal in database. Ask server admin for adding one: "
NEW_SESSION_SEPARATOR_MSG = "\n___________________________________________________________________________________\n"
WAIT_FOR_INPUT_MSG = "Press any key ..."
NOT_FOUND_TERMINAL_MSG = "Terminal not assigned in database"


def read_data(prompt=""):
    return input(prompt)


def show_msg(msg):
    print(msg)


# SERVER
CHOOSE_MENU_OPTION_MSG = "Choose menu option: "
UNKNOWN_OPTION_MSG = "Given unknown menu option"
ADDED_TERMINAL_MSG = "Added terminal to server database"
ADDED_WORKER_MSG = "Added worker to server database"
REMOVED_TERMINAL_MSG = "Removed terminal from server database"
WORKER_NAME_INPUT_MSG = "Enter worker name: "
WORKER_SURNAME_INPUT_MSG = "Enter worker surname: "
WORKER_ID_INPUT_MSG = "Enter worker id: "
CARD_ID_INPUT_MSG = "Enter card id: "
REMOVED_WORKER_MSG = "Removed worker from server database"
REMOVED_CARD_MSG = "Removed card from worker: "
ADDED_CARD_TO_WORKER_MSG = "Assigned card to worker"
EMPTY_MSG = "Empty - nothing to show"
INCORRECT_DATE_FORMAT_MSG = "Incorrect date value or format - should be YYYY-MM-DD, e.g. "
DATE_INPUT_MSG = "Enter date in format YYYY-MM-DD (or nothing for choosing current day) and press enter: "
SAVED_REPORT_IN_DATABASE_MSG = "Saved report in database server"

ServerMenuTuple = namedtuple('Menu', ['number', 'display_string'])


class ServerMenu(Enum):
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
    show_workers = ServerMenuTuple(7, "Print workers database")
    show_logs = ServerMenuTuple(8, "Print database records log")
    show_terminals = ServerMenuTuple(9, "Print terminals saved in database")
    generate_reports = ServerMenuTuple(10, "Generate reports")
    exit_menu = ServerMenuTuple(11, "Exit - press enter without giving any text to console")

    @staticmethod
    def show():
        print(NEW_SESSION_SEPARATOR_MSG)
        for s in ServerMenu:
            print(s.number, s.display_string, sep=") ")
        print(NEW_SESSION_SEPARATOR_MSG)


class ServerReportMenu(Enum):
    @property
    def display_string(self):
        return self.value.display_string

    @property
    def number(self):
        return self.value.number

    report_log_from_day = ServerMenuTuple(1, "Generate logs from given day ")
    report_log_from_day_worker = ServerMenuTuple(2, "Generate logs from given day and worker")
    report_work_time_from_day_worker = ServerMenuTuple(3, "Generate work time report for given worker and day")
    report_work_time_from_day = ServerMenuTuple(4, "Generate work time report for all workers for given day")
    report_general_work_time = ServerMenuTuple(5, "Generate general work time report for all")

    @staticmethod
    def show():
        print(NEW_SESSION_SEPARATOR_MSG)
        for s in ServerReportMenu:
            print(s.number, s.display_string, sep=") ")
        print(NEW_SESSION_SEPARATOR_MSG)

from enum import Enum
from collections import namedtuple


def read_data(prompt=""):
    """
    Read data from user via Command Line Interface (CLI)
    :param prompt: Prompt for input
    """
    return input(prompt)


def show_msg(msg):
    """
    Show message in Command Line Interface (CLI)
    :param msg: Message to show
    """
    print(msg)


# -------------------------------------------------------------------------------------------------------------------- #
TERM_GUID_INPUT = "Enter terminal GUID: "
TERM_NAME_INPUT = "Enter terminal name: "
CARD_USAGE_REGISTERED = "Saved in database usage of RFID card"
UNKNOWN_CARD_OWNER = "Card owner unknown"
CARD_OWNER_IS_KNOWN = "Card owner is: "
SEPARATOR = "\n___________________________________________________________________________________\n"
WAIT_FOR_INPUT = "Press any key ..."
CHOOSE_MENU_OPTION = "Choose menu option: "
UNKNOWN_OPTION = "Given unknown menu option"
ADDED_TERM = "Added terminal to server database"
ADDED_WORKER = "Added worker to server database"
REMOVED_TERM = "Removed terminal from server database"
WORKER_NAME_INPUT = "Enter worker name: "
WORKER_SURNAME_INPUT = "Enter worker surname: "
WORKER_ID_INPUT = "Enter worker GUID: "
CARD_ID_INPUT = "Enter card GUID: "
REMOVED_WORKER = "Removed worker from server database"
REMOVED_CARD = "Removed card from worker: "
ADDED_CARD = "Assigned card to worker"
EMPTY = "Empty - nothing to show"
INCORRECT_DATE_FORMAT = "Incorrect date value or format - should be YYYY-MM-DD, e.g. "
DATE_INPUT = "Enter date in format YYYY-MM-DD (or nothing for choosing current day) and press enter: "
INCORRECT_DIGIT_INPUT = "Incorrect input - must be digit"
INCORRECT_LITERALS_INPUT = "Incorrect input - cannot be empty or contain digit"
TRACKING_ACTIVITY_MENU = "Tracking activity on server. Press 0 to exit"

# -------------------------------------------------------------------------------------------------------------------- #
ServerMenuTuple = namedtuple('Menu', ['number', 'display_string'])


class ServerMenu(Enum):
    @property
    def display_string(self):
        """
        :return: Display string assigned to particular menu option
        """
        return self.value.display_string

    @property
    def number(self):
        """
        :return: Number assigned to particular menu option
        """
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
    tracking_activity = ServerMenuTuple(11, "Track activity - show interactive logs with terminals activity")
    exit_menu = ServerMenuTuple(12, "Exit - press enter without giving any text to console")

    @staticmethod
    def show():
        """
        Show server menu in UI
        """
        print(SEPARATOR)
        for s in ServerMenu:
            print(s.number, s.display_string, sep=") ")
        print(SEPARATOR)


# -------------------------------------------------------------------------------------------------------------------- #
class ServerReportsMenu(Enum):
    @property
    def display_string(self):
        """
        :return: Display string assigned to particular menu option
        """
        return self.value.display_string

    @property
    def number(self):
        """
        :return: Number assigned to particular menu option
        """
        return self.value.number

    report_log_from_day = ServerMenuTuple(1, "Generate logs from given day ")
    report_log_from_day_worker = ServerMenuTuple(2, "Generate logs from given day and worker")
    report_work_time_from_day_worker = ServerMenuTuple(3, "Generate work time report for given worker and day")
    report_work_time_from_day = ServerMenuTuple(4, "Generate work time report for all workers for given day")
    report_general_work_time = ServerMenuTuple(5, "Generate general work time report for all")

    @staticmethod
    def show():
        """
        Show server submenu in UI for report generations
        """
        print(SEPARATOR)
        for s in ServerReportsMenu:
            print(s.number, s.display_string, sep=") ")
        print(SEPARATOR)

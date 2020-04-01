from datetime import datetime
from app.logic.server import Server, DataInputError
import app.cli as ui


def read_literal(prompt):
    """
    Read user input data until it is not empty, not single char and not digit containing value
    :param prompt: Prompt text used in input
    :return: Readed literal converted to upper case
    """
    literal = ui.read_data(prompt)
    while any(char.isdigit() for char in literal) or len(literal.strip()) < 2:
        ui.show_msg(ui.INCORRECT_LITERALS_INPUT_MSG)
        literal = ui.read_data(prompt)
    return literal.upper()


def read_digit(prompt):
    """
    Read user input data until it is not empty and correct digit containing value
    :param prompt: Prompt text used in input
    :return: Readed digit
    """
    digit = ui.read_data(prompt)
    while not digit.isdigit():
        ui.show_msg(ui.INCORRECT_DIGIT_INPUT_MSG)
        digit = ui.read_data(prompt)
    return digit


class ClientController:
    def __init__(self):
        self.server = Server()
        self.terminal = None

    def setup(self):
        """
        Prepare client machine as specific terminal
        """
        self.check_any_terminal_registered()
        self.terminal = self.get_terminal_from_user()

    def check_any_terminal_registered(self):
        """
        Check if at least one terminal is added in database. If not exit program
        :return: True - at least one terminal is added in database, False - otherwise
        """
        if not self.server.is_any_terminal_registered():
            ui.show_msg(ui.NOT_REGISTERED_ANY_TERMINAL_MSG)
            ui.read_data(ui.WAIT_FOR_INPUT_MSG)
            exit(0)

    def get_terminal_from_user(self):
        """
        Readed terminal GUID until not find it in database
        :return: Terminal from databse with given GUID from user input
        """
        term_guid = ui.read_data(ui.TERMINAL_GUID_INPUT_MSG)
        while not self.server.terminal_in_database(term_guid):
            ui.show_msg(term_guid + ": " + ui.NOT_FOUND_TERMINAL_MSG)
            ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
            term_guid = ui.read_data(ui.TERMINAL_GUID_INPUT_MSG)
        return self.server.get_terminals()[term_guid]

    def run(self):
        """
        Run client application. Executed in loop until specific exit input not given
        """
        self.setup()
        while True:
            ui.show_msg(ui.CARD_SCAN_PROMPT_MSG)
            card_guid = self.terminal.scan_card()
            if card_guid == "":
                exit(0)
            self.register_card_usage(card_guid)

    def register_card_usage(self, card_guid):
        """
        Register RFID card usage in database and save results in database and show in CLI
        :param card_guid:
        """
        ui.show_msg(ui.CARD_SCANNED_PROPERLY_MSG)
        card_owner = self.server.register_card_usage(card_guid, self.terminal.term_id)
        ui.show_msg(ui.CARD_USAGE_REGISTERED_MSG)
        if card_owner is None:
            ui.show_msg(ui.UNKNOWN_CARD_OWNER_MSG)
        else:
            owner_id = card_owner.worker_id
            owner_fullname = card_owner.name + " " + card_owner.surname
            ui.show_msg(ui.CARD_OWNER_IS_KNOWN_MSG + owner_id + ", " + owner_fullname)
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)


class ServerController:
    def __init__(self):
        self.server = Server()

    def run(self):
        """
        Run server application. Executed in loop until specific exit input given
        """
        while True:
            ui.ServerMenu.show()
            menu_option = self.get_menu_option()
            self.open_menu_option(menu_option)

    def get_menu_option(self):
        """
        Read user input for menu option choose, until given input is digit
        :return: Number - selected menu number
        """
        user_input = input(ui.CHOOSE_MENU_OPTION_MSG)
        while not user_input.isdigit():
            self.show_incorrect_menu_option_msg()
            user_input = input(ui.CHOOSE_MENU_OPTION_MSG)
        menu_option = float(user_input)

        return menu_option

    def show_incorrect_menu_option_msg(self):
        """
        Show message in CLI, that given menu option in unknown / incorrect
        """
        ui.show_msg(ui.UNKNOWN_OPTION_MSG)
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)

    def open_menu_option(self, option):
        """
        choosing correct action in regard to given option
        :param option: selected menu option
        """
        if option == ui.ServerMenu.add_terminal.number:
            self.show_add_terminal_ui()
        elif option == ui.ServerMenu.exit_menu.number:
            exit(0)
        elif option == ui.ServerMenu.remove_terminal.number:
            self.show_remove_terminal_ui()
        elif option == ui.ServerMenu.add_worker.number:
            self.show_add_worker_ui()
        elif option == ui.ServerMenu.remove_worker.number:
            self.show_remove_worker_ui()
        elif option == ui.ServerMenu.add_card_to_worker.number:
            self.show_assign_card_ui()
        elif option == ui.ServerMenu.remove_worker_card.number:
            self.show_unassign_card_ui()
        elif option == ui.ServerMenu.show_workers.number:
            self.show_data(self.server.get_workers().values())
        elif option == ui.ServerMenu.show_logs.number:
            self.show_data(self.server.get_registered_logs().values())
        elif option == ui.ServerMenu.show_terminals.number:
            self.show_data(self.server.get_terminals().values())
        elif option == ui.ServerMenu.generate_reports.number:
            self.show_reports_generate_menu()
        else:
            self.show_incorrect_menu_option_msg()
        ui.read_data(ui.WAIT_FOR_INPUT_MSG)

    def show_add_terminal_ui(self):
        """
        Show UI and take action for adding new terminal to database
        """
        term_guid = read_digit(ui.TERMINAL_GUID_INPUT_MSG)
        term_name = ui.read_data(ui.TERMINAL_NAME_INPUT_MSG)
        try:
            self.server.add_terminal(term_guid, term_name)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.ADDED_TERMINAL_MSG)

    def show_remove_terminal_ui(self):
        """
        Show UI and take action for removing terminal from database
        """
        term_guid = ui.read_data(ui.TERMINAL_GUID_INPUT_MSG)
        try:
            self.server.remove_terminal(term_guid)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.REMOVED_TERMINAL_MSG)

    def show_add_worker_ui(self):
        """
        Show UI and take action for adding new worker to database
        """
        worker_guid = read_digit(ui.WORKER_ID_INPUT_MSG)
        worker_name = read_literal(ui.WORKER_NAME_INPUT_MSG)
        worker_surname = read_literal(ui.WORKER_SURNAME_INPUT_MSG)

        try:
            self.server.add_worker(worker_name, worker_surname, worker_guid)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.ADDED_WORKER_MSG)

    def show_remove_worker_ui(self):
        """
        Show UI and take action for removing worker from database
        """
        worker_id = ui.read_data(ui.WORKER_ID_INPUT_MSG)
        try:
            self.server.remove_worker(worker_id)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.REMOVED_WORKER_MSG)

    def show_assign_card_ui(self):
        """
        Show UI and take action for assigning new RFID card to worker
        """
        worker_guid = ui.read_data(ui.WORKER_ID_INPUT_MSG)
        card_guid = read_digit(ui.CARD_ID_INPUT_MSG)
        try:
            self.server.assign_card_to_worker(card_guid, worker_guid)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.ADDED_CARD_TO_WORKER_MSG)

    def show_unassign_card_ui(self):
        """
        Show UI and take action for unassigning card from worker
        """
        term_id = ui.read_data(ui.CARD_ID_INPUT_MSG)
        try:
            worker_id = self.server.unassign_card_from_worker(term_id)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.REMOVED_CARD_MSG + worker_id)

    def show_data(self, list):
        """
        Print every element from given arr, separated with text separator from CLI
        :param list: List of elements to show
        """
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
        if list.__len__() > 0:
            for element in list:
                ui.show_msg(element.__str__())
                ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
        else:
            ui.show_msg(ui.EMPTY_MSG)
            ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)

    def show_reports_generate_menu(self):
        """
        Show submenu and take action for selected report type
        """
        ui.ServerReportsMenu.show()
        option = self.get_menu_option()
        if option == ui.ServerReportsMenu.report_log_from_day.number:
            date = self.read_player_date_input()
            if date is not None:
                generated_data = self.server.report_log_from_day(True, date)
                self.show_data(generated_data)
        elif option == ui.ServerReportsMenu.report_log_from_day_worker.number:
            worker_id = ui.read_data(ui.WORKER_ID_INPUT_MSG)
            date = self.read_player_date_input()
            if date is not None:
                generated_data = self.server.report_log_from_day_worker(worker_id, True, date)
                self.show_data(generated_data)
        elif option == ui.ServerReportsMenu.report_work_time_from_day_worker.number:
            worker_id = ui.read_data(ui.WORKER_ID_INPUT_MSG)
            date = self.read_player_date_input()
            if date is not None:
                generated_data = self.server.report_work_time_from_day_worker(worker_id, date)
                ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
                ui.show_msg(generated_data)
                ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
        elif option == ui.ServerReportsMenu.report_work_time_from_day.number:
            date = self.read_player_date_input()
            if date is not None:
                generated_data = self.server.report_work_time_from_day(True, date)
                self.show_worker_with_time_report(generated_data)
        elif option == ui.ServerReportsMenu.report_general_work_time.number:
            generated_data = self.server.general_report(True)
            self.show_worker_with_time_report(generated_data)
        else:
            self.show_incorrect_menu_option_msg()

    def show_worker_with_time_report(self, tuple_list):
        """
        Show in CLI data from generated report
        :param tuple_list: Data saved in tuples (worked GUID, work time) in list
        """
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
        for tup in tuple_list:
            ui.show_msg("Worker GUID: " + tup[0] + " Work time: " + tup[1].__str__())
            ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)

    def read_player_date_input(self):
        """
        Read player data input. If incorrect value or format show message about it in CLI
        :return: Readed date <datatime> or None if give incorrect
        """
        date_str = ui.read_data(ui.DATE_INPUT_MSG)
        if date_str == "":
            return datetime.now()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            return date
        except ValueError:
            ui.show_msg(ui.INCORRECT_DATE_FORMAT_MSG + datetime.now().date().__str__())
            return None

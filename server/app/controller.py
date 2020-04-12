from datetime import datetime
from app.logic.server import Server, DataInputError
import app.cli as ui
import paho.mqtt.client as mqtt


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


class ServerController:
    def __init__(self):
        self.server = Server()
        self.__broker_address = "127.0.0.1"
        self.__client = mqtt.Client("SERVER_CONTROLLER")
        self.__server_active = True

    def run(self):
        """
        Run server application. Executed in loop until specific exit input given
        """
        self.connect_to_broker()
        while self.__server_active:
            ui.ServerMenu.show()
            menu_option = self.get_menu_option()
            self.open_menu_option(menu_option)
        self.disconnect_from_broker()

    def connect_to_broker(self):
        self.__client.connect(self.__broker_address)
        self.__client.on_message = self.process_message
        self.__client.subscribe("app/server")
        self.__client.loop_start()

    def process_message(self, client, userdata, message):
        message_decoded = (str(message.payload.decode("utf-8"))).split(".")
        if self.terminal_reading_msg(message_decoded):
            term_msg = ""
            for k in self.server.get_terminals().keys():
                term_msg += k
                term_msg += "."
            self.__client.publish("app/terminal", term_msg)
            print(message_decoded[0])  # todo
        elif self.card_reading_msg(message_decoded):
            print(message_decoded[0])  # todo
            card_owner = self.server.register_card_usage(message_decoded[0], message_decoded[1])
            self.show_card_usage_msg(card_owner)
        else:
            ui.show_msg(message_decoded[0])

    def card_reading_msg(self, message_decoded):
        return message_decoded[0] != "Terminal connected" and message_decoded[0] != "Terminal disconnected"

    def terminal_reading_msg(self, message_decoded):
        return message_decoded[0] == "terminals_reading"

    def show_card_usage_msg(self, card_owner):
        ui.show_msg(ui.CARD_USAGE_REGISTERED_MSG)
        if card_owner is None:
            ui.show_msg(ui.UNKNOWN_CARD_OWNER_MSG)
        else:
            owner_guid = card_owner.worker_guid
            owner_fullname = card_owner.name + " " + card_owner.surname
            ui.show_msg(ui.CARD_OWNER_IS_KNOWN_MSG + owner_guid + ", " + owner_fullname)
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)

    def disconnect_from_broker(self):
        self.__client.loop_stop()
        self.__client.disconnect()

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
            self.__server_active = False
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

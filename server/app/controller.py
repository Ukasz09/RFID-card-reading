from datetime import datetime
from app.logic.server import Server, DataInputError
import app.cli as ui
import paho.mqtt.client as mqtt

TERM_READING_QUERY = "Terminals reading"
TERM_CONNECTING_QUERY = "Terminal connected"
TERM_DISCONNECTING_QUERY = "Terminal disconnected"
TERM_SELECTED_QUERY = "Terminal selected"
CARD_READING_QUERY = "Card readed"


def read_literal(prompt):
    """
    Read user input data until it is not empty, not single char and not digit containing value
    :param prompt: Prompt text used in input
    :return: Readed literal converted to upper case
    """
    literal = ui.read_data(prompt)
    while any(char.isdigit() for char in literal) or len(literal.strip()) < 2:
        ui.show_msg(ui.INCORRECT_LITERALS_INPUT)
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
        ui.show_msg(ui.INCORRECT_DIGIT_INPUT)
        digit = ui.read_data(prompt)
    return digit


class ServerController:
    def __init__(self):
        self.server = Server()
        self.__client = mqtt.Client("SERVER_CONTROLLER")
        self.__server_active = True
        self.tracking_activity = False

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
        """
        Connect via MQTT and subscribe `server` topic
        """
        config = self.server.get_configs()
        self.__client.tls_set(config["cert_path"])
        self.__client.username_pw_set(username=config["username"], password=config["password"])
        self.__client.connect(config["broker"], config["port"])
        self.__client.on_message = self.process_message
        self.__client.subscribe(config["server_topic"])
        self.__client.loop_start()

    def process_message(self, client, userdata, message):
        """
        Decode and process message from client (terminals list query, terminal connecting, terminal selected, RFID usage)
        :param message: message to process
        """
        decoded = (str(message.payload.decode("utf-8"))).split(".")
        if decoded[0] == TERM_READING_QUERY:
            self.term_reading_query()
        elif decoded[0] == TERM_CONNECTING_QUERY:
            self.term_connecting_query(decoded[0])
        elif decoded[0] == TERM_DISCONNECTING_QUERY:
            self.term_disconnection_query(decoded[0], decoded[1])
        elif decoded[0] == TERM_SELECTED_QUERY:
            self.term_selected_query(decoded[1], decoded[2])
        elif decoded[0] == CARD_READING_QUERY:
            self.card_reading_query(decoded[1], decoded[2])
        else:
            ui.show_msg("Unknown query")

    def term_reading_query(self):
        self.__client.publish(self.server.get_configs()["term_topic"], self.available_term_query())

    def term_connecting_query(self, msg):
        if self.tracking_activity:
            ui.show_msg(msg)
            ui.show_msg(ui.SEPARATOR)

    def term_disconnection_query(self, msg, term_guid):
        if self.tracking_activity:
            ui.show_msg(msg)
            ui.show_msg(ui.SEPARATOR)
        self.server.set_terminal_engage(term_guid, False)

    def term_selected_query(self, msg, term_guid):
        self.server.set_terminal_engage(term_guid, True)
        if self.tracking_activity:
            ui.show_msg(msg + term_guid)
        ui.show_msg(ui.SEPARATOR)

    def card_reading_query(self, card_guid, term_guid):
        card_owner = self.server.register_card_usage(card_guid, term_guid)
        if self.tracking_activity:
            self.show_card_usage_msg(card_guid, card_owner, term_guid)

    def show_card_usage_msg(self, card_guid, card_owner, terminal_id):
        """
        Show information to console about RFID card usage
        :param card_guid: GUID of RFID card
        :param card_owner: card owner
        :param terminal_id: used terminal ID
        """
        ui.show_msg(ui.CARD_USAGE_REGISTERED)
        ui.show_msg("Card GUID= " + card_guid)
        if card_owner is None:
            ui.show_msg(ui.UNKNOWN_CARD_OWNER)
        else:
            owner_guid = card_owner.worker_guid
            owner_fullname = card_owner.name + " " + card_owner.surname
            ui.show_msg(ui.CARD_OWNER_IS_KNOWN + owner_guid + ", " + owner_fullname)
        ui.show_msg("Terminal ID= " + terminal_id)
        ui.show_msg(ui.SEPARATOR)

    def available_term_query(self):
        """
        :return: message with available terminals (only not engaged)
        """
        term_msg = ""
        for k in self.server.get_terminals().keys():
            if not self.server.terminal_is_engaged(k):
                term_msg += (k + ".")
        if term_msg == "":
            return term_msg
        return term_msg[:-1]  # skipping last dot

    def disconnect_from_broker(self):
        """
        Disconnect server from MQTT
        :return:
        """
        self.__client.loop_stop()
        self.__client.disconnect()

    def get_menu_option(self):
        """
        Read user input for menu option choose, until given input is digit
        :return: Number - selected menu number
        """
        user_input = input(ui.CHOOSE_MENU_OPTION)
        while not user_input.isdigit():
            self.incorrect_option_msg()
            user_input = input(ui.CHOOSE_MENU_OPTION)
        return float(user_input)

    def incorrect_option_msg(self):
        """
        Show message in CLI, that given menu option in unknown / incorrect
        """
        ui.show_msg(ui.UNKNOWN_OPTION)
        ui.show_msg(ui.SEPARATOR)

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
            self.show_data(self.server.get_logs().values())
        elif option == ui.ServerMenu.show_terminals.number:
            self.show_data(self.server.get_terminals().values())
        elif option == ui.ServerMenu.generate_reports.number:
            self.show_reports_generate_menu()
        elif option == ui.ServerMenu.tracking_activity.number:
            self.show_tracking_activity_menu()
        else:
            self.incorrect_option_msg()
        ui.read_data(ui.WAIT_FOR_INPUT)

    def show_add_terminal_ui(self):
        """
        Show UI and take action for adding new terminal to database
        """
        term_guid = read_digit(ui.TERM_GUID_INPUT)
        term_name = ui.read_data(ui.TERM_NAME_INPUT)
        try:
            self.server.add_term(term_guid, term_name)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.ADDED_TERM)

    def show_remove_terminal_ui(self):
        """
        Show UI and take action for removing terminal from database
        """
        term_guid = ui.read_data(ui.TERM_GUID_INPUT)
        try:
            self.server.remove_term(term_guid)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.REMOVED_TERM)

    def show_add_worker_ui(self):
        """
        Show UI and take action for adding new worker to database
        """
        worker_guid = read_digit(ui.WORKER_ID_INPUT)
        worker_name = read_literal(ui.WORKER_NAME_INPUT)
        worker_surname = read_literal(ui.WORKER_SURNAME_INPUT)

        try:
            self.server.add_worker(worker_name, worker_surname, worker_guid)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.ADDED_WORKER)

    def show_remove_worker_ui(self):
        """
        Show UI and take action for removing worker from database
        """
        worker_id = ui.read_data(ui.WORKER_ID_INPUT)
        try:
            self.server.remove_worker(worker_id)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.REMOVED_WORKER)

    def show_assign_card_ui(self):
        """
        Show UI and take action for assigning new RFID card to worker
        """
        worker_guid = ui.read_data(ui.WORKER_ID_INPUT)
        card_guid = read_digit(ui.CARD_ID_INPUT)
        try:
            self.server.assign_card(card_guid, worker_guid)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.ADDED_CARD)

    def show_unassign_card_ui(self):
        """
        Show UI and take action for unassigning card from worker
        """
        term_id = ui.read_data(ui.CARD_ID_INPUT)
        try:
            worker_id = self.server.unassign_card(term_id)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.REMOVED_CARD + worker_id)

    def show_data(self, list):
        """
        Print every element from given arr, separated with text separator from CLI
        :param list: List of elements to show
        """
        ui.show_msg(ui.SEPARATOR)
        if list.__len__() > 0:
            for element in list:
                ui.show_msg(element.__str__())
                ui.show_msg(ui.SEPARATOR)
        else:
            ui.show_msg(ui.EMPTY)
            ui.show_msg(ui.SEPARATOR)

    def show_reports_generate_menu(self):
        """
        Show submenu and take action for selected report type
        """
        ui.ServerReportsMenu.show()
        option = self.get_menu_option()
        if option == ui.ServerReportsMenu.report_log_from_day.number:
            self.log_from_day()
        elif option == ui.ServerReportsMenu.report_log_from_day_worker.number:
            self.log_from_day_for_worker()
        elif option == ui.ServerReportsMenu.report_work_time_from_day_worker.number:
            self.work_time_from_day_for_worker()
        elif option == ui.ServerReportsMenu.report_work_time_from_day.number:
            self.work_time_from_day()
        elif option == ui.ServerReportsMenu.report_general_work_time.number:
            self.show_worker_with_time_report(self.server.general_report(True))
        else:
            self.incorrect_option_msg()

    def log_from_day(self):
        date = self.read_player_date_input()
        if date is not None:
            generated_data = self.server.report_log_from_day(True, date)
            self.show_data(generated_data)

    def log_from_day_for_worker(self):
        worker_id = ui.read_data(ui.WORKER_ID_INPUT)
        date = self.read_player_date_input()
        if date is not None:
            generated_data = self.server.report_log_from_day_worker(worker_id, True, date)
            self.show_data(generated_data)

    def work_time_from_day_for_worker(self):
        worker_id = ui.read_data(ui.WORKER_ID_INPUT)
        date = self.read_player_date_input()
        if date is not None:
            generated_data = self.server.report_work_time_from_day_worker(worker_id, date)
            ui.show_msg(ui.SEPARATOR)
            ui.show_msg(generated_data)
            ui.show_msg(ui.SEPARATOR)

    def work_time_from_day(self):
        date = self.read_player_date_input()
        if date is not None:
            generated_data = self.server.report_work_time_from_day(True, date)
            self.show_worker_with_time_report(generated_data)

    def show_tracking_activity_menu(self):
        """
        Show console panel in which appeared on runtime current activity logs noticed on server
        """
        self.tracking_activity = True
        ui.show_msg(ui.TRACKING_ACTIVITY_MENU)
        ui.show_msg(ui.SEPARATOR)
        user_input = input()
        while user_input != "0":
            user_input = input()
        self.tracking_activity = False

    def show_worker_with_time_report(self, tuple_list):
        """
        Show in CLI data from generated report
        :param tuple_list: Data saved in tuples (worked GUID, work time) in list
        """
        ui.show_msg(ui.SEPARATOR)
        for tup in tuple_list:
            ui.show_msg("Worker GUID: " + tup[0] + " Work time: " + tup[1].__str__())
            ui.show_msg(ui.SEPARATOR)

    def read_player_date_input(self):
        """
        Read player data input. If incorrect value or format show message about it in CLI
        :return: Readed date <datatime> or None if give incorrect
        """
        date_str = ui.read_data(ui.DATE_INPUT)
        if date_str == "":
            return datetime.now()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            return date
        except ValueError:
            ui.show_msg(ui.INCORRECT_DATE_FORMAT + datetime.now().date().__str__())
            return None

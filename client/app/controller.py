import app.cli as ui
import paho.mqtt.client as mqtt

BROKER_ADDRESS = "127.0.0.1"
EXIT_BTN = ""


class ClientController:
    def __init__(self):
        self.__current_term_guid = None
        self.__client_active = True
        self.__broker_address = BROKER_ADDRESS
        self.__client = mqtt.Client("CLIENT CONTROLLER")
        self.__not_logged = True
        self.__term_list = None

    def run(self):
        """
        Run client application. Executed in loop until specific exit input not given
        """
        self.setup()
        # waiting for response from server
        ui.show_data(ui.WAITING_FOR_RESPONSE_MSG)
        while self.__term_list is None:
            pass

        self.check_any_terminal_registered()
        ui.show_data(ui.TERMINALS_READED_CORRECTLY)
        self.__current_term_guid = self.choose_terminal()
        while self.__client_active:
            ui.show_data(ui.CARD_SCAN_PROMPT_MSG)
            card_guid = self.scan_card()
            if card_guid == "":
                self.__client_active = False
            else:
                self.register_card_usage(card_guid)
        self.disconnect_from_broker()

    def setup(self):
        """
        Prepare client machine as specific terminal
        """

        self.connect_to_broker()
        self.get_terminals_from_database()
        self.__client.loop_start()

    def process_message(self, client, userdata, message):
        print("OTRZYMAM")
        if self.__not_logged:
            self.__term_list = (str(message.payload.decode("utf-8"))).split(".")
        print("ZDEKOD: ", message[0])
        print("TERM:", self.__term_list)

    def connect_to_broker(self):
        self.__client.connect(self.__broker_address)
        self.__client.subscribe("app/terminal")
        self.__client.on_message = self.process_message
        self.__client.publish("app/server", "Terminal connected")

    def disconnect_from_broker(self):
        self.__client.publish("app/server", "Terminal disconnected")
        self.__client.disconnect()

    def get_terminals_from_database(self):
        self.__client.publish("app/server", "terminals_reading")

    def check_any_terminal_registered(self):
        """
        Check if at least one terminal is added in database. If not exit program
        :return: True - at least one terminal is added in database, False - otherwise
        """
        if len(self.__term_list) == 0:
            ui.show_data(ui.NOT_REGISTERED_ANY_TERMINAL_MSG)
            ui.read_data(ui.WAIT_FOR_INPUT_MSG)
            exit(0)

    def choose_terminal(self):
        """
        Readed terminal GUID until not find it in database
        :return: Terminal from databse with given GUID from user input
        """
        ui.show_data(ui.TERMINALS_MENU)
        ui.show_data(self.__term_list)
        term_guid = ui.read_data(ui.USER_TERMINALS_INPUT)

        while term_guid not in self.__term_list:
            ui.show_data(term_guid + ": " + ui.NOT_FOUND_TERMINAL_MSG)
            ui.show_data(ui.NEW_SESSION_SEPARATOR_MSG)
            term_guid = ui.read_data(ui.USER_TERMINALS_INPUT)
        return term_guid

    def register_card_usage(self, card_guid):
        """
        Register RFID card usage in database and save results in database and show in CLI
        :param card_guid:
        """
        ui.show_data(ui.CARD_SCANNED_PROPERLY_MSG)
        self.notify_server_about_card_usage(card_guid, self.__current_term_guid)

    def notify_server_about_card_usage(self, card_guid, terminal_guid):
        self.__client.publish("app/server", card_guid + "." + terminal_guid)

    def scan_card(self):
        """
        Scan and return card GUID - temporary mocked to read RFID card code from user console
        :return: card GUID
        """
        return self.read_card("Mocked - put card id from keyboard or nothing to exit: ", EXIT_BTN)

    def read_card(self, prompt, exit_btn):
        """
        Read input from user as long as given string will be correct digit or equals <exit_btn>
        :param prompt: Prompt text used in input
        :param exit_btn: Text string used to recognize when program should exit
        :return: User input string
        """
        user_input = ui.read_data(prompt)
        while not user_input.isdigit() and not user_input == exit_btn:
            ui.show_data(ui.INCORRECT_DIGIT_INPUT_MSG)
            user_input = ui.read_data(prompt)
        return user_input

from app.server import Server
from app.terminal import Terminal
import app.cli as ui


class ClientController:
    def __init__(self):
        self.server = ServerController()
        self.terminal = None

    def setup(self):
        self.check_any_terminal_registered()
        self.terminal = self.get_terminal_id()

    def check_any_terminal_registered(self):
        if not self.server.is_any_terminal_registered():
            ui.show_msg(ui.NOT_REGISTERED_ANY_TERMINAL_MSG)
            input(ui.WAIT_WITH_EXIT_MSG)
            exit(0)

    def get_terminal_id(self):
        term = Terminal(ui.read_data(ui.TERMINAL_ID_CHOOSE_MSG))
        while not self.server.terminal_in_database(term.term_id):
            ui.show_msg(term.term_id + ": " + ui.NOT_FOUND_TERMINAL_MSG)
            ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
            term = Terminal(ui.read_data(ui.TERMINAL_ID_CHOOSE_MSG))
        return term

    def run(self):
        self.setup()
        while True:
            ui.show_msg(ui.CARD_SCAN_PROMPT_MSG)
            card_id = self.terminal.scan_card()
            if card_id == "":
                exit(0)
            self.register_card(card_id)

    def register_card(self, card_id):
        ui.show_msg(ui.CARD_SCANNED_PROPERLY_MSG)
        card_owner = self.server.register_card_in_system(card_id, self.terminal.term_id)
        ui.show_msg(ui.CARD_USAGE_REGISTERED_MSG)
        if card_owner is None:
            ui.show_msg(ui.UNKNOWN_CARD_OWNER_MSG)
        else:
            ui.show_msg(ui.CARD_OWNER_IS_KNOWN_MSG + card_owner.worker_id)
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)


class ServerController:
    def __init__(self):
        self.server = Server()

    def run(self):
        while True:
            ui.show_server_menu()
            menu_option = self.get_menu_option()
            print("temp", menu_option)  # todo

    def get_menu_option(self):
        user_input = input(ui.CHOOSE_MENU_OPTION_MSG)
        if not user_input.isdigit():
            self.show_incorrect_menu_option_msg()
            self.get_menu_option()
        menu_option = float(user_input)
        exit_menu_number = ui.ServerMenu.exit_menu.number
        if menu_option < 1 or menu_option > exit_menu_number:
            self.show_incorrect_menu_option_msg()
            self.get_menu_option()
        if menu_option == exit_menu_number:
            exit(0)
        return menu_option

    def show_incorrect_menu_option_msg(self):
        ui.show_msg(ui.UNKNOWN_OPTION_MSG)
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)

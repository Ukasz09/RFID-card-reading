from app.logic.server import Server, DataInputError
import app.cli as ui


class ClientController:
    def __init__(self):
        self.server = Server()
        self.terminal = None

    def setup(self):
        self.check_any_terminal_registered()
        self.terminal = self.get_terminal_from_user()

    def check_any_terminal_registered(self):
        if not self.server.is_any_terminal_registered():
            ui.show_msg(ui.NOT_REGISTERED_ANY_TERMINAL_MSG)
            input(ui.WAIT_FOR_INPUT_MSG)
            exit(0)

    def get_terminal_from_user(self):
        term_id = ui.read_data(ui.TERMINAL_ID_INPUT_MSG)
        while not self.server.terminal_in_database(term_id):
            ui.show_msg(term_id + ": " + ui.NOT_FOUND_TERMINAL_MSG)
            ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
            term_id = ui.read_data(ui.TERMINAL_ID_INPUT_MSG)
        return self.server.get_terminals()[term_id]

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
            owner_id = card_owner.worker_id
            owner_fullname = card_owner.name + " " + card_owner.surname
            ui.show_msg(ui.CARD_OWNER_IS_KNOWN_MSG + owner_id + ", " + owner_fullname)
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)


class ServerController:
    def __init__(self):
        self.server = Server()

    def run(self):
        while True:
            ui.ServerMenu.show()
            menu_option = self.get_menu_option()
            self.open_menu_option(menu_option)

    def get_menu_option(self):
        user_input = input(ui.CHOOSE_MENU_OPTION_MSG)
        if not user_input.isdigit():
            self.show_incorrect_menu_option_msg()
            self.get_menu_option()
        menu_option = float(user_input)

        return menu_option

    def show_incorrect_menu_option_msg(self):
        ui.show_msg(ui.UNKNOWN_OPTION_MSG)
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)

    def open_menu_option(self, option):
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
            self.show_add_card_ui()
        elif option == ui.ServerMenu.remove_worker_card.number:
            self.show_remove_card_ui()
        elif option == ui.ServerMenu.show_workers.number:
            self.show_data(self.server.get_workers().values())
        elif option == ui.ServerMenu.show_logs.number:
            self.show_data(self.server.get_registered_logs().values())
        elif option == ui.ServerMenu.show_terminals.number:
            self.show_data(self.server.get_terminals().values())
        else:
            self.show_incorrect_menu_option_msg()

    def show_add_terminal_ui(self):
        term_id = ui.read_data(ui.TERMINAL_ID_INPUT_MSG)
        term_name = ui.read_data(ui.TERMINAL_NAME_INPUT_MSG)
        try:
            self.server.add_terminal(term_id, term_name)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.ADDED_TERMINAL_MSG)

    def show_remove_terminal_ui(self):
        term_id = ui.read_data(ui.TERMINAL_ID_INPUT_MSG)
        try:
            self.server.remove_terminal(term_id)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.REMOVED_TERMINAL_MSG)

    def show_add_worker_ui(self):
        worker_id = ui.read_data(ui.WORKER_ID_INPUT_MSG)
        worker_name = ui.read_data(ui.WORKER_NAME_INPUT_MSG)
        worker_surname = ui.read_data(ui.WORKER_SURNAME_INPUT_MSG)
        try:
            self.server.add_worker(worker_name, worker_surname, worker_id)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.ADDED_WORKER_MSG)

    def show_remove_worker_ui(self):
        worker_id = ui.read_data(ui.WORKER_ID_INPUT_MSG)
        try:
            self.server.remove_worker(worker_id)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.REMOVED_WORKER_MSG)

    def show_add_card_ui(self):
        worker_id = ui.read_data(ui.WORKER_ID_INPUT_MSG)
        card_id = ui.read_data(ui.CARD_ID_INPUT_MSG)
        try:
            self.server.add_card_to_worker(card_id, worker_id)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.ADDED_CARD_TO_WORKER_MSG)

    def show_remove_card_ui(self):
        term_id = ui.read_data(ui.CARD_ID_INPUT_MSG)
        try:
            worker_id = self.server.remove_card_from_worker(term_id)
        except DataInputError as err:
            ui.show_msg(err.message)
        else:
            ui.show_msg(ui.REMOVED_CARD_MSG + worker_id)

    def show_data(self, arr):
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
        if arr.__len__() > 0:
            for worker in arr:
                ui.show_msg(worker.__str__())
                ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
        else:
            ui.show_msg(ui.EMPTY_MSG)
            ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)

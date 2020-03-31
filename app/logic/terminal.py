import app.cli as ui


def read_digit_or_exit_btn(prompt, exit_btn):
    user_input = ui.read_data(prompt)
    while not user_input.isdigit() and not user_input == exit_btn:
        ui.show_msg(ui.INCORRECT_DIGIT_INPUT_MSG)
        user_input = ui.read_data(prompt)
    return user_input


class Terminal(object):
    def __init__(self, term_id, name):
        self.term_id = term_id
        self.name = name

    # temp - mock to rfid card reading (id given via console)
    def scan_card(self):
        card_id = read_digit_or_exit_btn("Temporary mocked - put card id from keyboard or nothing to exit: ", "")
        return card_id


def __str__(self):
    return "Terminal ID: " + self.term_id + "\nTerminal name: " + self.name

import app.cli as ui


def read_digit_or_exit_btn(prompt, exit_btn):
    """
    Read input from user as long as given string will be correct digit or equals <exit_btn>
    :param prompt: Prompt text used in input
    :param exit_btn: Text string used to recognize when program should exit
    :return: User input string
    """
    user_input = ui.read_data(prompt)
    while not user_input.isdigit() and not user_input == exit_btn:
        ui.show_msg(ui.INCORRECT_DIGIT_INPUT_MSG)
        user_input = ui.read_data(prompt)
    return user_input


class Terminal(object):
    def __init__(self, term_guid, name):
        self.term_guid = term_guid
        self.name = name

    def scan_card(self):
        """
        Scan and return card GUID - temporary mocked to read RFID card code from user console
        :return: card GUID
        """
        card_id = read_digit_or_exit_btn("Temporary mocked - put card id from keyboard or nothing to exit: ", "")
        return card_id

    def __str__(self):
        return "Terminal GUID: " + self.term_guid + "\nTerminal name: " + self.name

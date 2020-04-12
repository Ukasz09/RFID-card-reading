def read_data(prompt=""):
    """
    Read data from user vi Command Line Interface (CLI)
    :param prompt: Prompt for input
    """
    return input(prompt)


def show_data(msg):
    """
    Show message in Command Line Interface (CLI)
    :param msg: Message to show
    """
    print(msg)


CARD_SCAN_PROMPT_MSG = "Scan your RFID card"
CARD_SCANNED_PROPERLY_MSG = "Card scanned properly"
NOT_REGISTERED_ANY_TERMINAL_MSG = "Not found any registered terminal in database. Ask server admin for adding one: "
NEW_SESSION_SEPARATOR_MSG = "\n___________________________________________________________________________________\n"
WAIT_FOR_INPUT_MSG = "Press any key ..."
NOT_FOUND_TERMINAL_MSG = "Terminal not assigned in database"
WAITING_FOR_RESPONSE_MSG = "Waiting for response from server to read available terminals..."
TERMINALS_READED_CORRECTLY = "Terminals readed correctly from server"
TERMINALS_MENU = "\nChoose one of registered terminals in server:"
USER_TERMINALS_INPUT = "Chosen terminal ID: "
INCORRECT_DIGIT_INPUT_MSG = "Given card GUID is incorrect"

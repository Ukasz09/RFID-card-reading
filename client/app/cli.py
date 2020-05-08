def read_data(prompt=""):
    """
    Read config from user via Command Line Interface (CLI)
    :param prompt: Prompt for input
    """
    return input(prompt)


def show_data(msg):
    """
    Show message in Command Line Interface (CLI)
    :param msg: Message to show
    """
    print(msg)


# -------------------------------------------------------------------------------------------------------------------- #
SCAN_CARD_PROMPT = "Scan RFID card"
CARD_SCANNED = "RFID card scanned properly"
NOT_FOUND_TERMINAL = "Not found any registered terminal in database or all terminals are engaged. Contact with server admin"
SEPARATOR = "\n___________________________________________________________________________________\n"
INPUT_WAITING = "Press any key ..."
INCORRECT_TERMINAL = "Terminal not assigned to server database"
WAITING_FOR_SERVER = "Waiting for response from server, to read available terminals..."
TERMINALS_READED = "Terminals read correctly from server"
TERMINALS_MENU = "\nChoose one of registered terminals:"
TERMINAL_INPUT = "Chosen terminal ID: "
WRONG_CARD_GUID = "Given card GUID is incorrect"

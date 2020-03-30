TERMINAL_ID_CHOOSE_MSG = "Enter terminal id: "
CARD_SCAN_PROMPT_MSG = "Scan your RFID card"
CARD_SCANNED_PROPERLY_MSG = "Card scanned properly"
CARD_USAGE_REGISTERED_MSG = "Saved in database usage of RFID card"
# CARD_USAGE_NOT_REGISTERED_MSG = "Usage of RFID card not registered in database. Please contact with server admin"
UNKNOWN_CARD_OWNER_MSG = "Card owner unknown"
CARD_OWNER_IS_KNOWN_MSG = "Card owner: "
NOT_REGISTERED_ANY_TERMINAL_MSG = "Not found any registered terminal in database. Ask server admin for adding one: "
NEW_SESSION_SEPARATOR_MSG = "\n___________________________________________________________________________________\n"
WAIT_WITH_EXIT_MSG = "Press any key to exit"
NOT_FOUND_TERMINAL_MSG = "Terminal not assigned in database"


def read_data(prompt=""):
    return input(prompt)


def show_msg(msg):
    print(msg)

class Terminal(object):
    def __init__(self, term_id, name):
        self.term_id = term_id
        self.name = name

    # temp - mock to rfid card reading (id given via console)
    def scan_card(self):
        card_id = input("Temporary mocked - put card id from keyboard or nothing to exit: ")
        return card_id

    def __str__(self):
        return "Terminal ID: " + self.term_id + "\nTerminal name: " + self.name

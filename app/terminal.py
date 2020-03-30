class Terminal(object):
    def __init__(self, term_id):
        self.term_id = term_id

    # temp - mock to rfid card reading (id given via console)
    def scan_card(self):
        card_id = input()
        return card_id

    def __str__(self):
        return self.term_id

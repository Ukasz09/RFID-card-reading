class Terminal:
    def __init__(self, term_id):
        self.term_id = term_id

    def scan_card(self, card_id):
        print("Scanned: ", card_id)

    def __str__(self):
        return self.term_id

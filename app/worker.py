class Worker:
    def __init__(self, name, worker_id, cards=[]):
        self.worker_id = worker_id
        self.name = name
        self.cards = cards

    def add_card(self, rfid_code):
        self.cards.append(rfid_code)

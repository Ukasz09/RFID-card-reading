class Worker:
    def __init__(self, name, worker_id):
        self.name = name
        self.worker_id = worker_id
        self.cards = []

    def add_card(self, rfid_code):
        if rfid_code not in self.cards:
            self.cards.append(rfid_code)

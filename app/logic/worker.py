class Worker(object):
    def __init__(self, name, surname, worker_id, cards=[]):
        self.worker_id = worker_id
        self.name = name
        self.surname = surname
        self.cards = cards

    def add_card(self, rfid_code):
        self.cards.append(rfid_code)

    def __str__(self):
        id_msg = "ID: " + self.worker_id + "\n"
        name_msg = "Full name: " + self.name + " " + self.surname + "\n"
        cards_msg = "Cards: " + self.cards.__str__()
        return id_msg + name_msg + cards_msg

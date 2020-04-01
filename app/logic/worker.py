class Worker(object):
    def __init__(self, name, surname, worker_guid, cards=[]):
        self.worker_guid = worker_guid
        self.name = name
        self.surname = surname
        self.cards = cards

    def add_card(self, guid):
        """
        Add RFID card to worker
        :param guid: RFID card GUID code
        """
        self.cards.append(guid)

    def __str__(self):
        id_msg = "GUID: " + self.worker_guid + "\n"
        name_msg = "Full name: " + self.name + " " + self.surname + "\n"
        cards_msg = "Cards: " + self.cards.__str__()
        return id_msg + name_msg + cards_msg

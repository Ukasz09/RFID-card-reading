class Worker(object):
    def __init__(self, name, surname, worker_guid, cards=[]):
        """
        :param name: Name of worker
        :param surname: Surname of worker
        :param worker_guid: GUID number of worker
        :param cards: cards GUID which belong to worker
        """
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
        """
        :return: Text representation of RegistryLog object
        """
        id_msg = "GUID: " + self.worker_guid + "\n"
        name_msg = "Full name: " + self.name + " " + self.surname + "\n"
        cards_msg = "Cards: " + self.cards.__str__()
        return id_msg + name_msg + cards_msg

class RegistryLog:
    def __init__(self, time, term_guid, card_guid, worker_guid=None):
        """
        :param time: Time of registered event
        :param term_guid: GUID of terminal on which event appear
        :param card_guid: GUID of RFID card used in terminal
        :param worker_guid: GUID of worker to which card is assigned
        """
        self.time = time
        self.term_guid = term_guid
        self.card_guid = card_guid
        self.worker_guid = worker_guid

    def __str__(self):
        """
        :return: Text representation of RegistryLog object
        """
        time_msg = "Time: " + self.time + "\n"
        term_msg = "Terminal GUID: " + self.term_guid + "\n"
        if self.worker_guid is None:
            worker_msg = "Worker GUID: unknown (not registered)\n"
        else:
            worker_msg = "Worker GUID: " + self.worker_guid + "\n"
        card_msg = "Card GUID: " + self.card_guid
        return time_msg + term_msg + worker_msg + card_msg

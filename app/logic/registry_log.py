class RegistryLog:
    def __init__(self, time, term_id, card_id, worker_id=None):
        self.time = time
        self.term_id = term_id
        self.card_id = card_id
        self.worker_id = worker_id

    def __str__(self):
        time_msg = "Time: " + self.time + "\n"
        terminal_msg = "Terminal ID: " + self.term_id + "\n"
        if self.worker_id is None:
            worker_msg = "Worker ID: unknown (not registered)\n"
        else:
            worker_msg = "Worker ID: " + self.worker_id + "\n"
        card_msg = "Card ID: " + self.card_id
        return time_msg + terminal_msg + worker_msg + card_msg

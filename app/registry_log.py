class RegistryLog:
    def __init__(self, time, term_id, card_id, worker_id=None):
        self.time = time
        self.term_id = term_id
        self.card_id = card_id
        self.worker_id = worker_id

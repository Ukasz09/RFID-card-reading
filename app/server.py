from app.terminal import Terminal
from app.database_connection.local_database import LocalDatabase
from app.worker import Worker
from app.registry_log import RegistryLog
from datetime import datetime

terminal_json = "../data/terminals.json"
workers_json = "../data/workers.json"
logs_json = "../data/registrations.json"


class DataInputError(BaseException):
    def __init__(self, message):
        self.message = message


class Server:
    def __init__(self):
        self.database = LocalDatabase(terminal_json, workers_json, logs_json)
        self.terminals_dict = self.database.read_terminals()
        self.workers_dict = self.database.read_workers()
        self.logs_dict = self.database.read_logs()

    def add_terminal(self, term_id):
        if term_id not in self.terminals_dict:
            new_term = Terminal(term_id)
            self.terminals_dict[term_id] = new_term
            self.database.write_terminals(self.terminals_dict.values())
        else:
            raise DataInputError("Terminal with id: " + term_id + " already exist")

    def remove_terminal(self, term_id):
        if term_id in self.terminals_dict:
            del self.terminals_dict[term_id]
            self.database.write_terminals(self.terminals_dict.values())
        else:
            raise DataInputError("Terminal with id: " + term_id + " not exist")

    def add_worker(self, name, worker_id):
        new_worker = Worker(name, worker_id)
        if worker_id not in self.workers_dict:
            self.workers_dict[worker_id] = new_worker
            self.database.write_workers(self.workers_dict.values())
        else:
            raise DataInputError("Worker with id:" + worker_id + " already exist in database")

    def remove_worker(self, worker_id):
        if worker_id in self.workers_dict:
            del self.workers_dict[worker_id]
            self.database.write_workers(self.workers_dict.values())
        else:
            raise DataInputError("Worker with id: " + worker_id + " not exist")

    def add_card_to_worker(self, card_id, worker_id):
        if worker_id in self.workers_dict:
            card_owner = self.get_card_owner(card_id)
            if card_owner is not None:
                raise DataInputError("Card with id: " + card_id + "assigned to worker with id: " + card_owner.worker_id)
            self.workers_dict[worker_id].cards.append(card_id)
            self.database.write_workers(self.workers_dict.values())
        else:
            raise DataInputError("Worker with id: " + worker_id + " not exist")

    def get_card_owner(self, card_id):
        for w in self.workers_dict.values():
            if card_id in w.cards:
                return w
        return None

    def remove_card_from_worker(self, card_id):
        for w in self.workers_dict.values():
            if card_id in w.cards:
                w.cards.remove(card_id)
                self.database.write_workers(self.workers_dict.values())
                return None
        raise DataInputError("Card with id: " + card_id + " hasn't been signed to any worker")

    def register_card_in_system(self, card_id, term_id):
        """
        :return: card owner id or none if card without owner
        """
        card_owner = self.get_card_owner(card_id)
        if not self.terminal_in_database(term_id):
            raise DataInputError("Terminal with id: " + term_id + " not assigned in database")
        if card_owner is None:
            owner_id = None
        else:
            owner_id = card_owner.worker_id
        self.add_log(card_id, term_id, owner_id)
        return card_owner

    def terminal_in_database(self, term_id):
        return term_id in self.terminals_dict

    def add_log(self, card_id, term_id, worker_id):
        time = datetime.now()
        self.logs_dict[time] = RegistryLog(time, term_id, card_id, worker_id)
        self.database.write_logs(self.logs_dict.values())

    def is_any_terminal_registered(self):
        return bool(self.terminals_dict)

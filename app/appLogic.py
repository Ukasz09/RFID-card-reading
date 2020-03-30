from app.terminal_management import TerminalManagement
from app.terminal import Terminal
from app.database_connection.local_using_json import LocalDatabase
from app.worker import Worker
from app.exceptions.server_exceptions import DataInputError

terminal_json = "../data/terminals.json"
workers_json = "../data/workers.json"


class Server:
    def __init__(self):
        self.database = LocalDatabase(terminal_json, workers_json)
        self.terminals = TerminalManagement(self.database.read_terminals())
        self.workers_dict = {}

    def add_terminal(self, term_id):
        new_term = Terminal(term_id)
        self.terminals.add_terminal(new_term)
        self.database.write_terminals(self.terminals.get_terminals_list())

    def remove_terminal(self, term_id):
        self.terminals.remove_terminal(term_id)
        self.database.write_terminals(self.terminals.get_terminals_list())

    def add_worker(self, name, worker_id):
        new_worker = Worker(name, worker_id)
        if worker_id not in self.workers_dict:
            self.workers_dict[worker_id] = new_worker
            self.database.write_workers(self.workers_dict.values())
        else:
            raise DataInputError("Worker with id:" + worker_id + " already exist in database")

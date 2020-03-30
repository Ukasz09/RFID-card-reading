import json
from app.terminal import Terminal
from app.worker import Worker


class LocalDatabase:
    def __init__(self, terminals_json, workers_json):
        self.term_path = terminals_json
        self.workers_path = workers_json

    @staticmethod
    def __save_data(json_path, objects_arr):
        methods_dict_arr = []
        for i in objects_arr:
            methods_dict_arr.append(i.__dict__)
        with open(json_path, "w") as f:
            json_txt = json.dumps(methods_dict_arr, indent=2, default=str)
            f.write(json_txt)

    @staticmethod
    def __read_data(json_path):
        with open(json_path, "r") as f:
            return f.read()

    def read_terminals(self):
        result_dict = {}
        f_content = LocalDatabase.__read_data(self.term_path)
        for term_dict in json.loads(f_content):
            term_id = term_dict["term_id"]
            result_dict[term_id] = Terminal(term_id)
        return result_dict

    def read_workers(self):
        result_dict = {}
        f_content = LocalDatabase.__read_data(self.workers_path)
        for workers_dict in json.loads(f_content):
            worker_id = workers_dict["worker_id"]
            name = workers_dict["name"]
            cards = workers_dict["cards"]
            result_dict[worker_id] = Worker(name, worker_id, cards)
        return result_dict

    def write_terminals(self, arr):
        LocalDatabase.__save_data(self.term_path, arr)

    def write_workers(self, arr):
        LocalDatabase.__save_data(self.workers_path, arr)

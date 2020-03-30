import json
from app.terminal import Terminal


class LocalDatabase:
    def __init__(self, terminals_json, workers_json):
        self.term_path = terminals_json
        self.workers_path = workers_json

    @staticmethod
    def __write_file(file, arr):
        json_txt = json.dumps(arr, indent=2, default=str)
        file.write(json_txt)

    @staticmethod
    def __save_data(json_path, arr):
        new_arr = []
        for i in arr:
            new_arr.append(i.__dict__)
        with open(json_path, "w") as f:
            LocalDatabase.__write_file(f, new_arr)

    def read_terminals(self):
        result_dict = {}
        with open(self.term_path, "r") as f:
            f_content = f.read()
        for term_dict in json.loads(f_content):
            term_id = term_dict["term_id"]
            result_dict[term_id] = Terminal(term_id)
        return result_dict

    def write_terminals(self, arr):
        LocalDatabase.__save_data(self.term_path, arr)

    def write_workers(self, arr):
        LocalDatabase.__save_data(self.workers_path, arr)

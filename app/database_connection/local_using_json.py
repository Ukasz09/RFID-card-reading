import json
from app.terminal import Terminal


class LocalDatabase:
    def __init__(self, terminals_json):
        self.term_path = terminals_json

    # @staticmethod
    # def __read_json_data(path):
    #     return open(path, "r+")

    @staticmethod
    def __write_file(file, arr):
        json_txt = json.dumps(arr, indent=2, default=str)
        file.write(json_txt)

    def make_terminals(self):
        terminals_list = []
        with open(self.term_path, "r") as f:
            f_content = f.read()
        for term_dict in json.loads(f_content):
            terminals_list.append(Terminal(term_dict["term_id"]))
        return terminals_list

    def save_terminals(self, arr):
        new_arr = []
        for i in arr:
            new_arr.append(i.__dict__)

        with open(self.term_path, "w") as f:
            self.__write_file(f,new_arr)
        # LocalDatabase.__write_file(f_content, new_arr)

# todo: close files

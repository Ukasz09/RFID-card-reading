import json
from app.logic.terminal import Terminal
from app.logic.worker import Worker
from app.logic.registry_log import RegistryLog


class LocalDatabase:
    def __init__(self, terminals_json, workers_json, registry_json):
        """
        :param terminals_json, workers_json, registry_json: path to local database files, saved with .json extension
        """
        self.term_path = terminals_json
        self.workers_path = workers_json
        self.logs_path = registry_json

    @staticmethod
    def __save_data(json_path, objects_list):
        """
        Save data to .json file via making association between objects methods and it's values
        :param json_path: path to .json file
        :param objects_list: list containing objects which needs to be written into file <json_path>
        """
        methods_dict_list = []
        for i in objects_list:
            methods_dict_list.append(i.__dict__)
        with open(json_path, "w") as f:
            json_txt = json.dumps(methods_dict_list, indent=2, default=str)
            f.write(json_txt)

    @staticmethod
    def __read_data(json_path):
        """
        Content of opened file
        :param json_path: file path with .json extension
        :return: file content
        """
        with open(json_path, "r") as f:
            return f.read()

    def read_terminals(self):
        """
        Reading saved terminals from .json file
        :return: Dictionary collection (term_id : Terminal)
        """
        result_dict = {}
        f_content = LocalDatabase.__read_data(self.term_path)
        for term_dict in json.loads(f_content):
            term_id = term_dict["term_id"]
            term_name = term_dict["name"]
            result_dict[term_id] = Terminal(term_id, term_name)
        return result_dict

    def read_logs(self):
        """
         Reading saved terminals registry logs from .json file
        :return: Dictionary collection (time : RegistryLog)
        """
        result_dict = {}
        f_content = LocalDatabase.__read_data(self.logs_path)
        for term_dict in json.loads(f_content):
            time = term_dict["time"]
            term_id = term_dict["term_id"]
            card_id = term_dict["card_id"]
            worker_id = term_dict["worker_id"]
            result_dict[time] = RegistryLog(time, term_id, card_id, worker_id)
        return result_dict

    def read_workers(self):
        """
        Reading saved workers from .json file
        :return:  Dictionary collection (worker id : Worker)
        """
        result_dict = {}
        f_content = LocalDatabase.__read_data(self.workers_path)
        for workers_dict in json.loads(f_content):
            worker_id = workers_dict["worker_id"]
            name = workers_dict["name"]
            surname = workers_dict["surname"]
            cards = workers_dict["cards"]
            result_dict[worker_id] = Worker(name, surname, worker_id, cards)
        return result_dict

    def write_terminals(self, objects_list):
        """
        Save terminals in local database (.json files)
        :param objects_list:  list of objects to save in database
        """
        LocalDatabase.__save_data(self.term_path, objects_list)

    def write_workers(self, objects_list):
        """
        Save workers in local database (.json files)
        :param objects_list:  list of objects to save in database
        """
        LocalDatabase.__save_data(self.workers_path, objects_list)

    def write_logs(self, objects_list):
        """
        Save register logs in local database (.json files)
        :param objects_list:  list of objects to save in database
        """
        LocalDatabase.__save_data(self.logs_path, objects_list)

    def write_reports_with_objects(self, objects_list, report_name):
        """
        Save reports result in local database (.json files)
        :param report_name: filename of new  generated report
        :param objects_list:  list of objects to save in report file
        """
        path = "../data/" + report_name + ".json"
        LocalDatabase.__save_data(path, objects_list)

    def write_reports_with_tuples(self, tuples_list, report_name):
        """
        Save work time result in local database (.json files)
        :param report_name: filename of new  generated report
        :param tuples_list:  list of tuples to save in report file
        """
        path = "../data/" + report_name + ".json"
        list_of_dict = list(map(lambda tup: {"worker_id": tup[0], "work_time": tup[1]}, tuples_list))
        with open(path, "w") as f:
            json_txt = json.dumps(list_of_dict, indent=2, default=str)
            f.write(json_txt)

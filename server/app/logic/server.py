from app.logic.terminal import Terminal
from app.logic.worker import Worker
from app.logic.registry_log import RegistryLog
from datetime import datetime
import app.json_data as json_data

CONFIG_PATH = "data/conf.json"


class DataInputError(BaseException):
    def __init__(self, message):
        self.message = message


class Server:
    def __init__(self):
        self.__conf_dict = json_data.read(CONFIG_PATH)
        self.__term_dict = Server.read_terminals(self.__conf_dict["terms_path"])
        self.__workers_dict = Server.read_workers(self.__conf_dict["workers_path"])
        self.__logs_dict = Server.read_logs(self.__conf_dict["logs_path"])

    @staticmethod
    def read_terminals(path):
        result = {}
        for data in json_data.read(path):
            result[data["term_guid"]] = Terminal(data["term_guid"], data["name"])
        return result

    @staticmethod
    def read_workers(path):
        result = {}
        for data in json_data.read(path):
            result[data["worker_guid"]] = Worker(data["name"], data["surname"], data["worker_guid"], data["cards"])
        return result

    @staticmethod
    def read_logs(path):
        result = {}
        for data in json_data.read(path):
            result[data["time"]] = RegistryLog(data["time"], data["term_guid"], data["card_guid"], data["worker_guid"])
        return result

    def write_terminals(self):
        json_data.write(self.__conf_dict["terms_path"], self.__term_dict.values())

    def write_workers(self):
        json_data.write(self.__conf_dict["workers_path"], self.__workers_dict.values())

    def write_logs(self):
        json_data.write(self.__conf_dict["logs_path"], self.__logs_dict.values())

    @staticmethod
    def write_reports(name, reports_obj):
        path = "data/" + name + ".json"
        json_data.write(path, reports_obj)

    @staticmethod
    def write_reports_dict_list(name, list_of_dict):
        path = "data/" + name + ".json"
        json_data.write_dict_list(path, list_of_dict)

    # --------------------------------------------------------------------------------------------------------------- #
    def add_term(self, term_guid, term_name):
        """
        Add terminal and save it in database
        :param term_guid: GUID of new terminal
        :param term_name: Name assigned to new terminal
        """
        if term_guid not in self.__term_dict:
            self.__term_dict[term_guid] = Terminal(term_guid, term_name)
            self.write_terminals()
        else:
            raise DataInputError("Terminal with GUID: " + term_guid + " already exist")

    def remove_term(self, term_guid):
        """
        Remove terminal from database
        :param term_guid:  GUID of terminal to remove
        """
        if term_guid in self.__term_dict:
            del self.__term_dict[term_guid]
            self.write_terminals()
        else:
            raise DataInputError("Terminal with GUID: " + term_guid + " not exist")

    def add_worker(self, name, surname, worker_guid):
        """
        Add/register new worker in system and save it database
        :param name: Name of new worker
        :param surname: Surname of new worker
        :param worker_guid: GUID of new worker
        """
        if worker_guid not in self.__workers_dict:
            self.__workers_dict[worker_guid] = Worker(name, surname, worker_guid)
            self.write_workers()
        else:
            raise DataInputError("Worker with GUID: " + worker_guid + " already exist in database")

    def remove_worker(self, worker_guid):
        """
        Remove worker from database
        :param worker_guid: GUID of worker to remove
        """
        if worker_guid in self.__workers_dict:
            del self.__workers_dict[worker_guid]
            self.write_workers()
        else:
            raise DataInputError("Worker with GUID: " + worker_guid + " not exist")

    def assign_card(self, card_guid, worker_guid):
        """
        Assign RFID card to worker
        :param card_guid: GUID of RFID card to assign
        :param worker_guid: GUID of worker to whose card will be assigned
        """
        if worker_guid in self.__workers_dict:
            card_owner = self.get_card_owner(card_guid)
            if card_owner is not None:
                err_msg = "Card with GUID: " + card_guid + " already assigned to worker with GUID: " + card_owner.worker_guid
                raise DataInputError(err_msg)
            self.__workers_dict[worker_guid].cards.append(card_guid)
            self.write_workers()
        else:
            raise DataInputError("Worker with GUID: " + worker_guid + " not exist")

    def get_card_owner(self, card_guid):
        """
        Return object of worker to whose belong card or None if to no one in database
        :param card_guid: GUID of RFID card
        :return: <Worker> instance or None
        """
        for w in self.__workers_dict.values():
            if card_guid in w.cards:
                return w
        return None

    def unassign_card(self, card_guid):
        """
        Unassign card which had assigned to worker
        :param card_guid: GUID of RFID card which needs to be unassigned
        """
        for w in self.__workers_dict.values():
            if card_guid in w.cards:
                w.cards.remove(card_guid)
                self.write_workers()
                return w.worker_guid
        raise DataInputError("Card with id: " + card_guid + " hasn't been signed to any worker")

    def register_card_usage(self, card_guid, term_guid):
        """
        Register usage of RFID card in system via writing usage log into database
        :param card_guid: GUID of used RFID card
        :param term_guid: GUID of used terminal
        :return: Card owner GUID or None if card without assigned owner
        """
        if not self.term_is_registered(term_guid):
            raise DataInputError("Terminal with id: " + term_guid + " not assigned in database")
        card_owner = self.get_card_owner(card_guid)
        if card_owner is None:
            owner_guid = None
        else:
            owner_guid = card_owner.worker_guid
        self.register_log(card_guid, term_guid, owner_guid)
        return card_owner

    def term_is_registered(self, term_guid):
        """
        Check if terminal with given GUID is saved in database
        :param term_guid: GUID of checked terminal
        :return: True - is in database, False - otherwise
        """
        return term_guid in self.__term_dict

    def register_log(self, card_guid, term_guid, worker_guid):
        """
        Save new register log in database
        :param card_guid: GUID of used RFID card
        :param term_guid: GUID of used terminal
        :param worker_guid: GUID of worker to whose belong card
        """
        time = datetime.now()
        self.__logs_dict[time.__str__()] = RegistryLog(time.__str__(), term_guid, card_guid, worker_guid)
        self.write_logs()

    def any_term_registered(self):
        """
        Check if in database is registered any terminal
        :return: True - at least one terminal registerd in database, False - otherwise
        """
        return bool(self.__term_dict)

    def get_workers(self):
        """
        :return: Workers dictionary
        """
        return self.__workers_dict

    def get_logs(self):
        """
        :return: Registered logs in database
        """
        return self.__logs_dict

    def get_terminals(self):
        """
        :return: Registered terminals in database
        """
        return self.__term_dict

    def get_configs(self):
        return self.__conf_dict

    def terminal_is_engaged(self, term_guid):
        if self.term_is_registered(term_guid):
            return self.__term_dict[term_guid].is_engaged
        return False

    def set_terminal_engage(self, term_guid, engaged):
        if self.term_is_registered(term_guid):
            self.__term_dict[term_guid].is_engaged = engaged

    def report_log_from_day(self, with_saving, date=datetime.now()):
        """
        Generate report with all logs added in given date
        :param with_saving: True - save report in database, False - not save report in database
        :param date: will be returned only logs with date equals <date>
        :return: List of <RegistryLog> objects
        """
        predicate = lambda k: datetime.strptime(k, "%Y-%m-%d %H:%M:%S.%f").date() == date.date()
        filtered_keys = list(filter(predicate, self.__logs_dict.keys()))
        filtered_logs = list(map(lambda k: self.__logs_dict[k], filtered_keys))

        if with_saving:
            report_name = "Report_[LOGS]_" + date.date().__str__()
            Server.write_reports(report_name, filtered_logs)
        return filtered_logs

    def report_log_from_day_worker(self, worker_guid, with_saving, date=datetime.now()):
        """
        Generate report with all logs added in given date which relate with worker with given GUID
        :param worker_guid: GUID of worker for whose we generate reports
        :param with_saving: True - save report in database, False - not save report in database
        :param date: will be returned only logs with date equals <date>
        :return: List of <RegistryLog> objects
        """
        logs_from_day = self.report_log_from_day(False, date)
        filtered_logs = list(filter(lambda l: l.worker_guid == worker_guid, logs_from_day))

        if with_saving:
            report_name = "Report_[LOGS]_[" + worker_guid + "]_" + date.date().__str__()
            Server.write_reports(report_name, filtered_logs)
        return filtered_logs

    def general_log_for_worker(self, worker_guid):
        """
         Generate report with all logs which are relate with worker with given GUID
        :param worker_guid: GUID of worker for whose we generate reports
        :return: List of <RegistryLog> objects
        """
        filtered_logs = []
        for log in self.__logs_dict.values():
            if log.worker_guid == worker_guid:
                filtered_logs.append(log)
        return filtered_logs

    def report_work_time_from_day_worker(self, worker_guid, date=datetime.now()):
        """
        Generate datatime value which means how much time worker with given GUID work in given day
        :param worker_guid: GUID of worker for whose we generate reports
        :param date: will be returned only logs with date equals <date>
        :return: <datatime> value
        """
        worker_log_for_day = self.report_log_from_day_worker(worker_guid, False, date)
        return self.calculate_work_time_for_worker(worker_log_for_day)

    def calculate_work_time_for_worker(self, worker_log):
        """
        Generate datatime value which means how much time worker with given GUID work in general
        :param worker_log: List with reports logs, which are relate with worker for whose we searching work time for
        :return: <datatime> value
        """
        work_cycles = []
        for i in range(0, len(worker_log) - 1, 2):
            exit_date_str = worker_log[i + 1].time
            exit_date = datetime.strptime(exit_date_str, "%Y-%m-%d %H:%M:%S.%f")
            enter_date_str = worker_log[i].time
            enter_date = datetime.strptime(enter_date_str, "%Y-%m-%d %H:%M:%S.%f")
            result = exit_date - enter_date
            work_cycles.append(result)
        if len(work_cycles) == 0:
            return datetime.now().time().min
        if len(work_cycles) == 1:
            return work_cycles[0]
        return sum(work_cycles[1:], work_cycles[0])

    def report_work_time_from_day(self, with_saving, date=datetime.now()):
        """
        Generate report with tuples (worker GUID, work time) for given day
        :param with_saving: True - save report in database, False - not save report in database
        :param date: will be returned only results with date equals <date>
        :return: List of tuples (worker GUID, work time <datatime>)
        """
        fun = lambda guid: (guid, self.report_work_time_from_day_worker(guid, date))
        work_time_list = list(map(fun, self.__workers_dict.keys()))
        only_positive_work_time = list(filter(lambda time: time[1] > time[1].min, work_time_list))
        if with_saving:
            report_name = "Report_[TIME]_" + date.date().__str__()
            list_of_dict = list(map(lambda tup: {"Worker_GUID": tup[0], "Work_time": tup[1]}, only_positive_work_time))
            Server.write_reports_dict_list(report_name, list_of_dict)
        return only_positive_work_time

    def general_report(self, with_saving):
        """
        Generate general report with tuples (worker GUID, work time) with every saved in database logs
        :param with_saving: True - save report in database, False - not save report in database
        :return: List of tuples (worker GUID, work time <datatime>)
        """
        work_time_list = []
        for w in self.__workers_dict.values():
            general_work_time = self.calculate_work_time_for_worker(self.general_log_for_worker(w.worker_guid))
            work_time_list.append((w.worker_guid, general_work_time))
        if with_saving:
            report_name = "Report_[GENERAL]_" + datetime.now().__str__()
            list_of_dict = list(map(lambda tup: {"Worker_GUID": tup[0], "Work_time": tup[1]}, work_time_list))
            Server.write_reports_dict_list(report_name, list_of_dict)
        return work_time_list

import json


def write(path, objects_list):
    """
    Save data to .json file via making association between objects methods and it's values
    :param path: path to .json file
    :param objects_list: list containing objects which needs to be written into file <json_path>
    """
    methods_dict_list = []
    for i in objects_list:
        methods_dict_list.append(i.__dict__)
    with open(path, "w") as f:
        json_txt = json.dumps(methods_dict_list, indent=2, default=str)
        f.write(json_txt)


def read(path):
    with open(path, "r") as f:
        content = f.read()
    return json.loads(content)


# todo pozbyc sie
def write_reports_with_tuples(self, tuples_list, report_name):
    """
    Save work time result in local database (.json files)
    :param report_name: filename of new  generated report
    :param tuples_list:  list of tuples to save in report file
    """
    path = "data/" + report_name + ".json"
    list_of_dict = list(map(lambda tup: {"Worker_GUID": tup[0], "Work_time": tup[1]}, tuples_list))
    with open(path, "w") as f:
        json_txt = json.dumps(list_of_dict, indent=2, default=str)
        f.write(json_txt)

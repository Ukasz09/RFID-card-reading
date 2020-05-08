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
    write_dict_list(path, methods_dict_list)


def write_dict_list(path, dict_list):
    with open(path, "w") as f:
        json_txt = json.dumps(dict_list, indent=2, default=str)
        f.write(json_txt)


def read(path):
    with open(path, "r") as f:
        content = f.read()
    return json.loads(content)

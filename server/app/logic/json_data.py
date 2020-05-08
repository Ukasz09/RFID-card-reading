import json


def write(path, objects_list):
    """
    Save data to .json file via making association between objects methods and it's values
    :param path: Path to .json file
    :param objects_list: List containing objects which needs to be written into file <json_path>
    """
    methods_dict_list = []
    for i in objects_list:
        methods_dict_list.append(i.__dict__)
    write_dict_list(path, methods_dict_list)


def write_dict_list(path, list_dict):
    """
    Save data to .json file by using data from list of dictionary
    :param path: Path to .json file
    :param list_dict: List of dictionaries which needs to be written into file <json_path>
    """
    with open(path, "w") as f:
        json_txt = json.dumps(list_dict, indent=2, default=str)
        f.write(json_txt)


def read(path):
    """
    Read content from json file
    :param path: Path to json file which need to be read
    :return: Content of read json file
    """
    with open(path, "r") as f:
        content = f.read()
    return json.loads(content)

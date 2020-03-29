import json


def read_json_data(path):
    f = open(path, "r")
    return json.loads(f.read())  # convert json to python arr/dict

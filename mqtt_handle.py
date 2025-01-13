import json 


def data_to_json(data):
    data_dict = {}
    for name, value in data:
        data_dict[name] = value
    return json.dumps(data_dict)
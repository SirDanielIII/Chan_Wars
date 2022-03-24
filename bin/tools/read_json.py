# Daniel Zhuo
# Module - JSON File Editing

import json


def read_json(path):
    """
    Args:
        path:string:
            The file directory of the .json file
    Returns:
        The loaded .json file
    """
    with open(path, 'r') as config:
        return json.load(config)


def write_json(path, header_1, header_1_v):
    with open(path) as f:
        data = json.load(f)
    data[header_1] = header_1_v
    json.dump(data, open(path, "w"), indent=4)

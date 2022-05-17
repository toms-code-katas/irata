import json
import os


def to_json(o: object) -> str:
    return json.dumps(o.__dict__, default=lambda o: o.__dict__, indent=4)


def load_map(name: str = "default"):
    map_file_name = os.path.dirname(os.path.abspath(__file__)) + "/maps/" + name + ".json"
    with open(map_file_name, 'r') as map_file:
        return json.loads(map_file.read())

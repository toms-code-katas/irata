from enum import Enum
import json
import os


def to_plot(json_values):
    # TODO: Rethink json to object serialization
    if "x" in json_values and "y" in json_values:
        return Coordinates(int(json_values["x"]), int(json_values["y"]))
    elif "coordinates" in json_values:
        return Plot(coordinates=json_values["coordinates"])
    else:
        raise NotImplementedError(f"Could not deserialized dict {json_values} to any type")


def to_dict(o: object) -> {}:
    return o.__dict__


def to_json(o: object) -> str:
    to_serialize = o
    if isinstance(o, list):
        to_serialize = [ob.__dict__ for ob in o]
    return json.dumps(to_serialize, default=to_dict, indent=2)


def load_map(name: str = "default"):
    map_file_name = os.path.dirname(os.path.abspath(__file__)) + "/maps/" + name + ".json"
    with open(map_file_name, 'r') as map_file:
        return json.loads(map_file.read(), object_hook=to_plot)


class Player:
    pass


class Coordinates:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class PlotType(Enum):
    STORE = 1
    RIVER = 2
    MOUNTAIN = 3
    PLAINS = 3


class Plot:

    def __init__(self, coordinates: Coordinates, owner: Player = None, plot_type: PlotType = None):
        self.coordinates = coordinates
        self.plot_type = plot_type
        self.owner = owner


class Map:

    __plots = {}

    def __init__(self, width: int = -1, height: int = -1):
        self.width = width
        self.height = height

    def create(self):
        if self.is_default_map():
            self.create_default_map()
        else:
            self.create_custom_map()

    def create_default_map(self):
        list_of_plots = load_map("default")
        for plot in list_of_plots:
            self.__plots[plot.coordinates] = plot
        last_plot = list(self.__plots.keys())[-1]
        self.width = last_plot.x
        self.height = last_plot.y

    def create_custom_map(self):
        for x in range(self.width):
            for y in range(self.height):
                coordinates = Coordinates(x + 1, y + 1)
                p = Plot(coordinates=coordinates)
                self.__plots[coordinates] = p

    def get_plots(self):
        return self.__plots.values()

    def is_default_map(self):
        return self.width == -1 and self.height == -1


class LandGrant:
    __map: Map

    def __int__(self, mapp: Map):
        self.__map = mapp

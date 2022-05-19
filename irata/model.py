from enum import Enum
import json
import os
import random


def to_plot(json_values):
    # TODO: Rethink json to object serialization
    if "x" in json_values and "y" in json_values:
        return Coordinates(int(json_values["x"]), int(json_values["y"]))
    elif "coordinates" in json_values:
        plot_type = None
        if json_values["plot_type"]:
            plot_type = PlotType(json_values["plot_type"])
        return Plot(coordinates=json_values["coordinates"], plot_type=plot_type)
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
    def __str__(self):
        return str(self.value)

    STORE = "store"
    RIVER = "river"
    MOUNTAIN = "mountain"
    PLAINS = "plains"


class Plot:

    def __init__(self, coordinates: Coordinates, owner: Player = None, plot_type: PlotType = None):
        self.coordinates = coordinates
        self.plot_type = plot_type
        self.owner = owner


class Map:

    def __init__(self):
        self.width = -1
        self.height = -1
        self.plots = {}

    def create(self):
        if self.is_default_map():
            self.create_default_map()
        else:
            self.create_custom_map()

    def create_default_map(self):
        list_of_plots = load_map("default")
        for plot in list_of_plots:
            self.plots[plot.coordinates] = plot
        last_plot = list(self.plots.keys())[-1]
        self.width = last_plot.x
        self.height = last_plot.y

    def create_custom_map(self):
        for x in range(self.width):
            for y in range(self.height):
                coordinates = Coordinates(x + 1, y + 1)
                p = Plot(coordinates=coordinates, plot_type=self.create_plot_type())
                self.plots[coordinates] = p

    def create_plot_type(self):
        should_be_mountain = bool(random.getrandbits(1))
        if should_be_mountain:
            return PlotType.MOUNTAIN
        else:
            return PlotType.PLAINS

    def get_plots(self):
        return self.plots.values()

    def is_default_map(self):
        return self.width == -1 and self.height == -1

    def get_plot_at(self, x, y):
        return list(filter(lambda plot: plot.coordinates.x == x and plot.coordinates.y == y, self.plots.values()))[0]


class LandGrantState(Enum):
    CREATED = "created"
    ONGOING = "ongoing"
    FINISHED = "finished"


class LandGrant:

    def __init__(self, mapp: Map):
        self.state: LandGrantState = LandGrantState.CREATED
        self.__map = mapp
        self.current_plot_index = 0

    def advance(self):
        self.current_plot_index += 1
        if self.current_plot_index == len(self.__map.get_plots()):
            self.state = LandGrantState.FINISHED

    def get_state(self) -> LandGrantState:
        return self.state

    def start(self):
        self.state = LandGrantState.ONGOING
        self.advance()
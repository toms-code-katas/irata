from enum import Enum
import json
import os
import random


def to_plot(json_values):
    # TODO: Rethink json to object serialization
    if "x" in json_values and "y" in json_values:
        return Coordinates(int(json_values["x"]), int(json_values["y"]))
    elif "coordinates" in json_values:
        plot_type = PlotType.PLAINS
        if "plot_type" in json_values and json_values["plot_type"]:
            plot_type = PlotType(json_values["plot_type"])
        plot_state = PlotState.FREE
        if "state" in json_values and json_values["state"]:
            plot_state = PlotState(json_values["state"])
        owner = None
        if "owner" in json_values and json_values["owner"]:
            owner = json_values["owner"]
        return Plot(coordinates=json_values["coordinates"], plot_type=plot_type, plot_sate=plot_state, owner=owner)
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


class PlayerType:
    pass

    def __init__(self, name: str):
        self.name = name


class Player:

    def __init__(self, name: str, player_type: PlayerType):
        self.name = name
        self.type = player_type


class Coordinates:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class PlotType(Enum):
    STORE = "store"
    RIVER = "river"
    MOUNTAIN = "mountain"
    PLAINS = "plains"


class PlotState(Enum):
    FREE = "free"
    TAKEN = "taken"


class Plot:

    def __init__(self, coordinates: Coordinates, owner: Player = None, plot_type: PlotType = None, plot_sate: PlotState = PlotState.FREE):
        self.coordinates = coordinates
        self.plot_type = plot_type
        self.owner = owner
        self.state = plot_sate


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
        self.validate_map()

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

    def validate_map(self):
        if not list(filter(lambda plot: plot.plot_type == PlotType.STORE, self.plots.values())):
            raise Exception("No store on map")

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

    def __init__(self, mapp: Map, players: {} = None):
        self.state: LandGrantState = LandGrantState.CREATED
        self.players = players
        self.map = mapp
        self.current_plot_index = 0
        self.players_already_selected = {}

    def advance(self):
        if self.state == LandGrantState.FINISHED:
            raise Exception("Land grant finished")
        self.current_plot_index += 1
        if self.current_plot_index == len(self.map.get_plots()):
            self.state = LandGrantState.FINISHED

    def start(self):
        self.state = LandGrantState.ONGOING

    def get_current_plot(self):
        return list(self.map.plots.values())[self.current_plot_index]

    def select_current_plot(self, player: Player) -> bool:
        if player.name in self.players_already_selected.keys():
            return False
        current_plot: Plot = self.get_current_plot()
        if current_plot.state == PlotState.TAKEN:
            return False
        current_plot.owner = player.name
        current_plot.state = PlotState.TAKEN
        self.players_already_selected[player.name] = player
        return True

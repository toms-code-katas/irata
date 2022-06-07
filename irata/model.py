from __future__ import annotations

from enum import Enum
import json
import math
import os
import random
from typing import Dict, List


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

    def __init__(self, name: str):
        self.name = name


class ResourceState:

    def __init__(self, name: str):
        self.name = name
        self.previous_amount: int = 0
        self.usage: int = 0
        self.production: int = 0
        self.spoilage: int = 0
        self.surplus: int = 0
        self.current_amount: int = 0

    def calculate_spoilage(self):
        if self.name in ["food", "energy"]:
            self.spoilage = math.ceil((self.previous_amount - self.usage) / 2)
        elif self.name in ["smithore", "crystite"] and self.previous_amount > 50:
            self.spoilage = self.previous_amount - 50
        self.current_amount = self.previous_amount - self.spoilage

    def calculate_surplus(self, units_needed: int):
        if self.name in ["food", "energy"]:
            self.current_amount = self.current_amount - self.usage + self.production
            self.surplus = self.current_amount - units_needed


class Stock:

    def __init__(self, resource: str, ask_price: int, bid_price: int, in_stock: int):
        self.resource = resource
        self.ask_price = ask_price
        self.bid_price = bid_price
        self.in_stock = in_stock


class Store:

    def __init__(self):
        self.stock: Dict[str, Stock] = {}
        self.players: Dict[str, Player] = {}

    def get_amount_in_stock(self, resource: str) -> int:
        return self.stock[resource].in_stock

    def add_stock(self, stock: Stock):
        self.stock[stock.resource] = stock


class Player:

    def __init__(self, name: str, player_type: PlayerType):
        self.name = name
        self.type = player_type
        self.resource_states: Dict[str: ResourceState] = {}

    def calculate_spoilage(self, resource_name: str):
        resource_state = self.resource_states[resource_name]
        if resource_state:
            resource_state.calculate_spoilage()

    def calculate_surplus(self, resource_name: str, units_needed: int):
        resource_state = self.resource_states[resource_name]
        if resource_state:
            resource_state.calculate_surplus(units_needed)

    def calculate_units_needed(self, resource_name: str, mapp: Map):
        if resource_name == "food":
            # TODO: This needs to be depended on the turn of the game
            return 3
        elif resource_name == "energy":
            return len(mapp.get_plots_for_player(self)) + 1


class Auction:

    def __init__(self, resource: str, store: Store, players: [Player], game_map: Map):
        self.resource = resource
        self.store = store
        self.game_map = game_map
        self.players: Dict[str, Player] = {}
        for player in players:
            self.add_player(player)

    def add_player(self, player: Player):
        self.players[player.name] = player

    def start(self):
        for player in self.players.values():
            player.calculate_units_needed(self.resource, self.game_map)
            player.calculate_spoilage(self.resource)
            player.calculate_surplus(self.resource, player.calculate_units_needed(self.resource, self.game_map))

    def get(self, seller: bool) -> List[Player]:
        players_in_role = []
        for player in self.players.values():
            if self.is_player_seller(player.name) and seller:
                players_in_role.append(player)
            else:
                players_in_role.append(player)
        return players_in_role

    def is_player_seller(self, player_name: str):
        player = self.players[player_name]
        return player.resource_states[self.resource].surplus > 0


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

    def get_plots_for_player(self, player: Player):
        return list(filter(lambda plot: plot.owner == player.name, self.plots.values()))


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

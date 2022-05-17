from enum import Enum
from irata import utils


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

    def __init__(self, width: int = 9, height: int = 5):
        self.width = width
        self.height = height

    def create(self):
        for x in range(self.width):
            for y in range(self.height):
                coordinates = Coordinates(x + 1, y + 1)
                p = Plot(coordinates=coordinates)
                self.__plots[coordinates] = p

    def get_plots(self):
        return self.__plots.values()


class LandGrant:
    __map: Map

    def __int__(self, mapp: Map):
        self.__map = mapp

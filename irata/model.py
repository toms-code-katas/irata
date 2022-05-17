from enum import Enum


class Player:
    pass


class Coordinates:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y


class PlotType(Enum):
    STORE = 1
    RIVER = 1
    MOUNTAIN = 1


class Plot:

    def __init__(self, coordinates: Coordinates, owner: Player = None, plot_type: PlotType = None):
        self.__coordinates = coordinates
        self.__plot_type = plot_type
        self.__owner = owner


class Map:

    __plots = {}

    def __init__(self, width: int = 9, height: int = 5):
        self.width = width
        self.height = height

    def create(self):
        for x in range(self.width):
            for y in range(self.height):
                coordinates = Coordinates(x + 1, y + 1)
                self.__plots[coordinates] = Plot(coordinates)


class LandGrant:
    __map: Map

    def __int__(self, mapp: Map):
        self.__map = mapp


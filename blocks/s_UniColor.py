__author__ = 'max'
from .Node import *
from .Interface import *
import os
import json


# import pickle


class UniColor(Source):
    """
    Static single color for the whole strip
    """
    __settingsfile = os.path.dirname(
        os.path.realpath(__file__)) + "/.defaultcolor"  # JSON file storing the current color

    def __set_color(self, new_color):
        """
        Sets color and writes the value to the JSON file
        :param new_color: The new color tuple
        """
        self.__color = new_color
        try:
            fhandle = open(self.__settingsfile, "w")
            # pickle.dump(self.__color, fhandle)
            json.dump(self.__color, fhandle)
            fhandle.close()
        except Exception:
            pass

    def __get_color(self):
        return self.__color

    color = property(__get_color, __set_color)

    def __init__(self):
        """
        Reads the value from the file
        """
        Source.__init__(self)
        self.outputs.append(Output(self))
        if os.path.isfile(self.__settingsfile):
            with open(self.__settingsfile, "r") as file:
                # self.set_color(pickle.load(file))
                self.__color = tuple(json.load(file))
                file.close()
        else:
            self.set_color((200, 120, 30))
            # self.color = (0b11111111, 0, 0b01111111)

    def tick(self):
        """
        Time independant, this function emits the current color to the outputs.
        :return:
        """
        data = []
        for i in range(0, 50):  # TODO: flexible lenghts
            data.append(self.color)
        self.outputs[0].send(data)

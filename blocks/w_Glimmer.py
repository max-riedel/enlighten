__author__ = 'max'
from .Node import *
from .Interface import *
from . import en_time
import random
import math


class Glimmer(Worker):
    """
    Glimmer imitates a fire-like effect with random sinus
    """

    def __init__(self):
        Worker.__init__(self)
        self.inputs.append(Input(self))
        self.outputs.append(Output(self))
        self.speed = 0.05
        random.seed()
        self._freqs = []  # Holds frequencies for each LED

        for i in range(0, 50):  # TODO: Enable different strip lenghts
            self._freqs.append(float(random.randrange(0, 1000)))
        self.max_offset = [50, 40, 20]  # empirical values

    def _numberfence(self, number, offset, min_val=0, max_val=255):
        """
        checks if a number is in a given number range between
        min_val + offset and max_val - offset. Numbers outside are cropped to that range.
        :param number: The number to check
        :param offset: Additional offset
        :param min_val: Upper boundary
        :param max_val: Lower boundary
        :return:
        """
        if number < min_val + offset:
            return min_val + offset
        if number > max_val - offset:
            return max_val - offset
        return number

    def signal(self, data):
        """
        Uses the sin function to swipe between different colors. Each LED has an individual swipe frequency
        previously set in the constructor.
        :param data: Strpi data
        :return:
        """
        out_data = []
        for i in range(50):  # TODO: Enable different strip lenghts (II)
            # Make sure to stay within allowed boundaries
            red = self._numberfence(data[i][0], self.max_offset[0])
            green = self._numberfence(data[i][1], self.max_offset[1])
            blue = self._numberfence(data[i][2], self.max_offset[2])

            raw = math.sin(en_time.time.time * (self._freqs[i] / 100 * (float(self.speed) / 10.0)))

            val_red = self.max_offset[0] * raw + red
            val_green = self.max_offset[1] * raw + green
            val_blue = self.max_offset[2] * raw + blue

            out_data.append((int(val_red), int(val_green), int(val_blue)))
        self.outputs[0].send(out_data)

from .Node import *
from .Interface import *
from .en_time import *
from . import en_time
import colorsys as cl


class Rainbow(Source):
    """
    Emits all colors.
    """
    def __init__(self):
        Source.__init__(self)
        self.outputs.append(Output(self))
        self.speed = 800

    def tick(self):
        """
        Uses the HSV color model to calculate all colors with fixed saturation and value. Hue, the color angle,
        determines the color.
        :return:
        """
        data = []
        localtime = en_time.time.time % self.speed
        hue = localtime / self.speed  # all color parameters are 0..1
        saturation = 0.8
        value = 1

        r, g, b = cl.hsv_to_rgb(hue, saturation, value)
        r *= 255  # Convert back to 0..255
        g *= 255
        b *= 255

        for i in range(0, 50):  # TODO: flexible length
            data.append([int(r), int(g), int(b)])
        self.outputs[0].send(data)

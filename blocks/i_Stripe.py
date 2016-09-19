__author__ = 'max'

from .Node import *
from .Interface import *
from neopixel import *
import sys
from .en_time import *


class Stripe(Sink):
    """
    WS2811 sink
    """

    def __init__(self, stripe):
        Sink.__init__(self)
        self.inputs.append(Input(self))
        self._stripe = stripe
        self._gammas = (2.0, 0.45, 0.25)  # empirical values

    def _color_correction(self, color: float, gamma: float):
        """
        Gamma correction for each color channels. Applies the function (color ^ 1/gamma) on the value
        :param color: color value (single integer)
        :param gamma: gamma value > 0
        :return:
        """
        correction = int(((color / 255) ** (1 / gamma)) * 255)
        if correction > 255:
            correction = 255
        elif correction < 0:  # math. impossible
            correction = 0
        return correction

    def signal(self, data):
        """
        Invokes the setPixelColor of the WS2911 for each LED and calls the show function afterwards.
        :param data:
        :return:
        """
        # print("Stripe: Got data! Global time is " + str(en_time.time.time))
        for i in range(0, len(data)):
            # sys.stdout.write(str(data[i][0]) + str(data[i][1]) + str(data[i][2]) + ' ')
            red = self._color_correction(data[i][0], self._gammas[0])
            green = self._color_correction(data[i][1], self._gammas[1])
            blue = self._color_correction(data[i][2], self._gammas[2])

            if blue == 0xFF:  # BUG in Aldi LEDs
                blue = 0xFE
            self._stripe.setPixelColor(i, Color(red, green, blue))
        self._stripe.show()
        # sys.stdout.write("\n")

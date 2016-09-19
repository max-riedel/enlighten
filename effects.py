"""
THIS FILE IS DEPRECATED! IT WAS USED FOR TESTING IN THE BEGINNING!
"""


__author__ = 'max'

import time
import random
import math
from neopixel import *


def g(luminance):
    gamma = 1.4
    if luminance < 0.0:
        return 0
    elif luminance > 255.0:
        return 255
    return int(255 * math.pow(float(luminance) / 255, gamma))


def color_channels(color):
    return {
        'red': color >> 16 & 0x0f,
        'green': color >> 8 & 0x0f,
        'blue': color & 0x0f
    }


class Effects:
    def __init__(self, strip):
        self._strip = strip
        """:type: Adafruit_NeoPixel"""
        self._time = 0.0
        """:type: int"""
        random.seed()
        self._init_freqs()

    def timestep(self):
        val = 33.0 / 1000.0
        time.sleep(val)
        self._time += val

    def color_wipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self._strip.numPixels()):
            self._strip.setPixelColor(i, color)
            self._strip.show()
            time.sleep(wait_ms / 1000.0)

    def _init_freqs(self):
        self._freqs = []
        """:type: list"""
        for i in range(0, self._strip.numPixels()):
            self._freqs.append(float(random.randrange(0, 1000)))

    def unicolor(self, color):
        for i in range(self._strip.numPixels()):
            self._strip.setPixelColor(i, color)
        self._strip.show()

    def source_colorswipe(self, start, end, speed=10.0):
        localtime = self._time % speed
        deltas = [0, 0, 0]
        out = [0, 0, 0]
        deltas[0] = (end[0] - start[0]) / speed * 2.0
        deltas[1] = (end[1] - start[1]) / speed * 2.0
        deltas[2] = (end[2] - start[2]) / speed * 2.0

        if localtime < speed / 2:
            direction = 1
            out[0] = direction * deltas[0] * localtime + start[0]
            out[1] = direction * deltas[1] * localtime + start[1]
            out[2] = direction * deltas[2] * localtime + start[2]
        else:
            direction = -1
            out[0] = direction * deltas[0] * (localtime - speed / 2) + end[0]
            out[1] = direction * deltas[1] * (localtime - speed / 2) + end[1]
            out[2] = direction * deltas[2] * (localtime - speed / 2) + end[2]
        # return Color(out[0], out[1], out[2])
        # print 'time', str(localtime), str(out[0]), str(out[1]), str(out[2])
        return out

    def glimmer(self, base_color, max_offset=[20, 20, 20], wait_ms=33, speed=8):
        """

        :param base_color:
        :type base_color:
        :param max_offset:
        :type max_offset:
        :return:
        :rtype:
        """
        red = base_color[0]
        green = base_color[1]
        blue = base_color[2]

        for i in range(self._strip.numPixels()):
            raw = math.sin(self._time * (self._freqs[i] / 100 * (float(speed) / 10.0)))  # + 1
            val_red = g(max_offset[0] * raw + red)
            val_green = g(max_offset[1] * raw + green)
            val_blue = g(max_offset[2] * raw + blue)
            self._strip.setPixelColor(i, Color(val_red, val_green, val_blue))
        self._strip.show()

__author__ = 'max'
from .Node import *


"""
This module provides the global time.
"""

class EnTime:
    def __init__(self):
        self._time = 0

    def __get_time(self):
        return self._time

    def __set_time(self, new_time):
        self._time = new_time

    time = property(__get_time, __set_time)

    def tick(self):
        self._time += 1

time = None


def init():
    global time
    time = EnTime()


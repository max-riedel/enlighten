__author__ = 'max'
from .Node import *
from .Interface import *
from .en_time import *
from . import en_time


class Colorswipe(Source):
    """
    Swipes between two pre-defined colors forward and backward.
    """
    def __init__(self):
        Source.__init__(self)
        self.outputs.append(Output(self))   # create a new output
        self.speed = 80
        self.start = (200, 120, 30)
        self.end = (255, 150, 70)

    def tick(self):
        localtime = en_time.time.time % self.speed
        deltas = [0, 0, 0]
        out = [0, 0, 0]
        deltas[0] = (self.end[0] - self.start[0]) / self.speed * 2.0
        deltas[1] = (self.end[1] - self.start[1]) / self.speed * 2.0
        deltas[2] = (self.end[2] - self.start[2]) / self.speed * 2.0

        if localtime < self.speed / 2:
            direction = 1
            out[0] = direction * deltas[0] * localtime + self.start[0]
            out[1] = direction * deltas[1] * localtime + self.start[1]
            out[2] = direction * deltas[2] * localtime + self.start[2]
        else:
            direction = -1
            out[0] = direction * deltas[0] * (localtime - self.speed / 2) + self.end[0]
            out[1] = direction * deltas[1] * (localtime - self.speed / 2) + self.end[1]
            out[2] = direction * deltas[2] * (localtime - self.speed / 2) + self.end[2]
        # return Color(out[0], out[1], out[2])
        # print 'time', str(localtime), str(out[0]), str(out[1]), str(out[2])

        data = []
        for i in range(0, 50):
            data.append([int(out[0]), int(out[1]), int(out[2])])
        self.outputs[0].send(data)

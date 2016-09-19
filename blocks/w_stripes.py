__author__ = 'max'
from .Node import *
from .Interface import *
#from .en_time import *


class Stripes(Worker):
    """
    Under construction!
    """
    def __init__(self):
        Worker.__init__(self)
        self.inputs.append(Input(self))
        self.outputs.append(Output(self))

    def signal(self, data):
        start = en_time.time.time % 2
        for i in range(start, len(data) - 2, 2):
            data[i] = (0, 0, 0)
        self.outputs[0].send(data)

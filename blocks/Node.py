__author__ = 'max'


class Node(object):
    """
    Base class for all blocks
    """

    def __init__(self):
        self.__uid = -1
        self.description = ''
        self.name = ''

    def __get_uid(self):
        return self.__uid

    def __set_uid(self, init_uid):
        if self.__uid == -1:
            self.__uid = init_uid
        elif init_uid != self.__uid:
            raise Exception('uid cannot be redefined!')

    uid = property(__get_uid, __set_uid)


class Source(Node):
    """
    Sources only have outputs. Each time the tick function is called, they emit a new color.
    """
    def __init__(self):
        Node.__init__(self)
        self.outputs = []

    def tick(self):
        pass


class Worker(Node):
    """
    Workers have inputs and outputs. When the inputs get new data, the function signal is called.
    """
    def __init__(self):
        Node.__init__(self)
        self.inputs = []
        self.outputs = []

    def signal(self, data):
        pass


class Sink(Node):
    """
    Sinks are the connection to the hardware and transform enlighten pipeline data to hardware signals. Like workers,
    the signal function is called once new data arrives.
    """
    def __init__(self):
        Node.__init__(self)
        self.inputs = []

    def signal(self, data):
        pass

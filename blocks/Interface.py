__author__ = 'max'


class Interface(object):
    """
    Base class for inputs ans outputs. data holds the actual RGB information. Interface objects trigger the signal
    function of their parents for ingress data or their send function is called by their parents.
    """
    def __init__(self, parent):
        self._data = []
        self._parent = parent


class Input(Interface):
    def __init__(self, parent):
        Interface.__init__(self, parent)

    def signal(self, data):
        self._data = data
        self._parent.signal(data)


class Output(Interface):
    def __init__(self, parent):
        Interface.__init__(self, parent)
        self._ancestors = []

    def add_ancestor(self, ancestor):
        self._ancestors.append(ancestor)

    def send(self, data):
        for ancestor in self._ancestors:
            ancestor.signal(data)


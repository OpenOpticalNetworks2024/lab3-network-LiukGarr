#import json
# nds variable for nodes



class Signal_information(object):
    def __init__(self):
        signal_pow = 0.0
        noise_pow = 0.0
        latency = 0.0
        pass

    @property
    def signal_power(self):
        pass

    def update_signal_power(self):
        pass

    @property
    def noise_power(self):
        pass

    @noise_power.setter
    def noise_power(self):
        pass

    def update_noise_power(self):
        pass

    @property
    def latency(self):
        pass

    @latency.setter
    def latency(self):
        pass

    def update_latency(self):
        pass

    @property
    def path(self):
        pass

    @path.setter
    def path(self):
        pass

    def update_path(self):
        pass


class Node(object):
    def __init__(self, lab_nds, pos, connected):
        self._lab_nds = lab_nds
        self._pos = pos
        self._connected = connected
        self._nextnds = {}
        pass

    @property
    def label(self):
        return self._lab_nds

    @property
    def position(self):
        return self._pos

    @property
    def connected_nodes(self):
        return self._connected

    @property
    def successive(self):
        return self._nextnds

    @successive.setter
    def successive(self, next_line):
        self._nextnds = next_line
        pass

    def propagate(self):
        pass


class Line(object):
    def __init__(self, lab_line, length):
        self._lab_line = lab_line
        self._length = length
        pass

    @property
    def label(self):
        return self._lab_line

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._nextline

    @successive.setter
    def successive(self, next_nodes):
        self._nextline = next_nodes
        pass

    def latency_generation(self):
        pass

    def noise_generation(self):
        pass

    def propagate(self):
        pass


class Network(object):
    def __init__(self, data):
        self._nodes ={}
        self._lines = {}
        for nds in data:
            self._nodes[nds]=Node(nds, data[str(nds)]['position'],data[str(nds)]['connected_nodes'])
        for nds in self._nodes:
            for con_nds in self._nodes[nds].connected_nodes:
                line = nds + con_nds
                self._lines[line] = Line(line, 1)


    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        pass

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2):
        pass
    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass
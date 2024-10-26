#import json
import numpy as np
import math
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
    def __init__(self, lab_line, pos1, pos2):
        self._arr_1 = []
        self._arr_2 = []
        self._lab_line = lab_line
        self._arr_1 = pos1
        self._arr_2 = pos2
        #print(float(self._arr_1[0]), float(self._arr_1[1]))
        diff_x = pow((float(self._arr_2[0]) - float(self._arr_1[0])), 2)
        diff_y = pow((float(self._arr_2[1]) - float(self._arr_1[1])), 2)
        #print(diff_x, diff_y)
        self._length = math.sqrt(diff_x + diff_y)

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
        self._nodes = {}
        nodi = []
        linee = []
        lst_linee = []
        self._lines = {}
        for nds in data:
            self._nodes[nds]=Node(nds, data[str(nds)]['position'],data[str(nds)]['connected_nodes'])
            #nodi.setdefault(nds, []).extend((self._nodes[nds].label, self._nodes[nds].connected_nodes, self._nodes[nds].position))
            #print(nodi[nds])
            #print(f"label: {self._nodes[nds].label}, pos: {self._nodes[nds].position}, connection: {self._nodes[nds].connected_nodes}")
        for nds in self._nodes:
            for con_nds in self._nodes[nds].connected_nodes:
                line = nds + con_nds
                #lst_linee.append(line)
                pos1 = self._nodes[nds].position
                pos2 = self._nodes[con_nds].position
                self._lines[line] = Line(line, pos1, pos2)
                #print(f"Nodo 1: {self._nodes[nds].label}, Nodo 2: {self._nodes[con_nds].label}")
                #print(f"La distanza {self._lines[line].label} è {self._lines[line].length}'")
        #print(nodi, "\n", linee)
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
        self._node2line = {}
        node2line = {}
        self._line2node = {}
        line2node = {}
        for nds in self._nodes:
            for lns in self._lines:
                char = lns[0]
                if nds == char:
                    self._node2line.setdefault(nds, []).append(lns)
            node2line.setdefault(nds, []).append(self._node2line[nds])
        print(node2line)
        for lns in self._lines:
            #char1 = lns[0]
            char2 = lns[1]
            for nds in self._nodes:
                #if nds == char1:
                    #n1 = nds
                    #self._line2node.setdefault(lns, []).insert(0, n1)
                #if nds == char2:
                    #n2 = nds
                    #self._line2node.setdefault(lns, []).insert(1, n2)
                if nds == char2:
                    n = nds
                    self._line2node.setdefault(lns, []).append(n)
            line2node.setdefault(lns, []).append(self._line2node[lns])
        print(line2node)

        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass
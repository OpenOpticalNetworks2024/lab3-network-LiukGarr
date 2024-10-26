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
                lst_linee.append(line)
                self._lines[line] = Line(line, 1)
                # print(f"lines: {self._lines[line].label}")
                linee.append(self._lines[line].label)
            nodi.append(self._nodes[nds].label)
        #print(nodi, "\n", linee)
        self.connect(nodi, linee)
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
    def connect(self, nodi, linee):
        self._node2line = {}
        node2line = {}
        self._line2node = {}
        line2node = {}
        for nds in nodi:
            for lns in linee:
                char = lns[0]
                if nds == char:
                    self._node2line.setdefault(nds, []).append(lns)
            node2line.setdefault(nds, []).append(self._node2line[nds])
        print(node2line)
        for lns in linee:
            char1 = lns[0]
            char2 = lns[1]
            for nds in nodi:
                if nds == char1:
                    n1 = nds
                    self._line2node.setdefault(lns, []).insert(0, n1)
                if nds == char2:
                    n2 = nds
                    self._line2node.setdefault(lns, []).insert(1, n2)
            line2node.setdefault(lns, []).append(self._line2node[lns])
        print(line2node)

        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass
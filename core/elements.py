# import json
import math


# nds variable for nodes


class Signal_information(object):
    def __init__(self, path):
        self._signal_pow = 1e-3
        self._noise_pow = 0.0
        self._latency = 0.0
        self._path = []
        self._path.append(path)
        pass

    @property
    def signal_power(self):
        return self._signal_pow

    def update_signal_power(self, increment_sp):
        self._signal_pow += increment_sp

    @property
    def noise_power(self):
        return self._noise_pow

    @noise_power.setter
    def noise_power(self, np):
        self._noise_pow = np

    def update_noise_power(self, increment_np):
        self._noise_pow += increment_np

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, lat):
        self._latency = lat

    def update_latency(self, increment_lat):
        self._latency += increment_lat

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, selected_path):
        self._path = selected_path

    def update_path(self):
        tmp_list_path = [self._path[0][1:]]
        self._path = tmp_list_path


class Node(object):
    def __init__(self, lab_nds, pos, connected):
        self._lab_nds = lab_nds
        self._pos = pos
        self._connected = connected
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
        self._nextlines = []
        self._arr_1 = []
        self._arr_2 = []
        self._lab_line = lab_line
        self._arr_1 = pos1
        self._arr_2 = pos2
        # print(float(self._arr_1[0]), float(self._arr_1[1]))
        diff_x = pow((float(self._arr_2[0]) - float(self._arr_1[0])), 2)
        diff_y = pow((float(self._arr_2[1]) - float(self._arr_1[1])), 2)
        # print(diff_x, diff_y)
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
        return self._nextlines

    @successive.setter
    def successive(self, next_node):
        self._nextlines = next_node
        pass

    def latency_generation(self):
        pass

    def noise_generation(self):
        sig_pow = Signal_information().signal_power
        noise = 1e-9*self.length*sig_pow
        print(noise)
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
        self._node2line = {}
        self._line2node = {}
        self.path = []
        for nds in data:
            self._nodes[nds] = Node(nds, data[str(nds)]['position'], data[str(nds)]['connected_nodes'])
            # nodi.setdefault(nds, []).extend((self._nodes[nds].label, self._nodes[nds].connected_nodes, self._nodes[nds].position))
            # print(nodi[nds])
            # print(f"label: {self._nodes[nds].label}, pos: {self._nodes[nds].position}, connection: {self._nodes[nds].connected_nodes}")
        for nds in self._nodes:
            for con_nds in self._nodes[nds].connected_nodes:
                line = nds + con_nds
                # lst_linee.append(line)
                # pos1 = self._nodes[nds].position
                # pos2 = self._nodes[con_nds].position
                self._lines[line] = Line(line, self._nodes[nds].position, self._nodes[con_nds].position)
                # print(f"Nodo 1: {self._nodes[nds].label}, Nodo 2: {self._nodes[con_nds].label}")
                # print(f"La distanza {self._lines[line].label} è {self._lines[line].length} meters'")
        # print(nodi, "\n", linee)
        self.connect()

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
        path = []
        paths = []
        visited = []
        copy_n2l = {}
        copy_l2n = {}
        first_node = label1
        last_node = label2
        b_stop = False
        for nds in self._node2line:
            if nds == first_node:
                # print(f"Le linee attaccate a {self._first_node} sono {self._node2line[nds]}")
                b_stop = True
        if not b_stop:
            print("Invalid node")
        else:
            visited.append(first_node)
            for next_lns in self._node2line[first_node]:
                next_nds = self._line2node[next_lns][0]
                visited.append(next_nds)
                if next_nds == last_node:
                    paths.append(first_node + next_nds)
                else:
                    for next_lns in self._node2line[next_nds]:
                        if next_lns[1] != first_node:
                            if next_lns[1] == last_node:
                                paths.append(first_node + next_nds + self._line2node[next_lns][0])
                            else:
                                next_nds1 = self._line2node[next_lns][0]
                                visited.append(next_nds1)
                                for next_lns1 in self._node2line[next_nds1]:
                                    if next_lns1[1] == last_node:
                                        paths.append(first_node + next_nds + self._line2node[next_lns][0] +
                                                     self._line2node[next_lns1][0])
                                    else:
                                        if (next_lns1[1] != next_nds) and (next_lns1[1] != first_node):
                                            next_nds2 = self._line2node[next_lns1][0]
                                            for next_lns2 in self._node2line[next_nds2]:
                                                if next_lns2[1] == last_node:
                                                    paths.append(first_node + next_nds + self._line2node[next_lns][0] +
                                                                 self._line2node[next_lns1][0] +
                                                                 self._line2node[next_lns2][0])
                                                else:
                                                    if (next_lns2[1] != next_nds) and (next_lns2[1] != first_node):
                                                        next_nds3 = self._line2node[next_lns2][0]
                                                        for next_lns3 in self._node2line[next_nds3]:
                                                            if next_lns3[1] == last_node:
                                                                tmp = first_node + next_nds + self._line2node[next_lns][
                                                                    0] + self._line2node[next_lns1][0]
                                                                if not self._line2node[next_lns2][0] in tmp:
                                                                    paths.append(first_node + next_nds +
                                                                                 self._line2node[next_lns][0] +
                                                                                 self._line2node[next_lns1][0] +
                                                                                 self._line2node[next_lns2][0] +
                                                                                 self._line2node[next_lns3][0])
            print(Signal_information(paths).path)
            #print(paths)

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
            # node2line.setdefault(nds, []).append(self._node2line[nds])
        # print(node2line)
        for lns in self._lines:
            # char1 = lns[0]
            char2 = lns[1]
            for nds in self._nodes:
                # if nds == char1:
                # n1 = nds
                # self._line2node.setdefault(lns, []).insert(0, n1)
                # if nds == char2:
                # n2 = nds
                # self._line2node.setdefault(lns, []).insert(1, n2)
                if nds == char2:
                    n = nds
                    self._line2node.setdefault(lns, []).append(n)
            # line2node.setdefault(lns, []).append(self._line2node[lns])
        # print(line2node)
        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass

# import json
import pandas as pd
import math
from core.parameters import c
from core.math_utils import snr
from decimal import Decimal
import matplotlib.pyplot as plt

arrow = '->'

# nds variable for nodes
class Signal_information(object):
    def __init__(self, sp, sl, sn, path):
        self._signal_pow = sp
        self._noise_pow = sn
        self._latency = sl
        self._path = path
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
        self._noise_pow = self._noise_pow + increment_np

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, lat):
        self._latency = lat

    def update_latency(self, increment_lat):
        self._latency = self._latency + increment_lat

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, selected_path):
        self._path = selected_path


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

        # Length calculation
        diff_x = pow((float(self._arr_2[0]) - float(self._arr_1[0])), 2)
        diff_y = pow((float(self._arr_2[1]) - float(self._arr_1[1])), 2)
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

    def latency_generation(self, length_line):
        latency_gen = length_line / (c * 2 / 3)
        return latency_gen

    def noise_generation(self, signal_power, length_line):
        noise = 1e-9*length_line*signal_power
        return noise

    def propagate(self):
        pass


class Network(object):
    def __init__(self, data):
        self._nodes = {}
        self._lines = {}
        self._node2line = {}
        self._line2node = {}
        # Nodes, position and connected nodes gathering
        for nds in data:
            self._nodes[nds] = Node(nds, data[str(nds)]['position'], data[str(nds)]['connected_nodes'])
        # Lines definition
        for nds in self._nodes:
            for con_nds in self._nodes[nds].connected_nodes:
                line = nds + con_nds
                self._lines[line] = Line(line, self._nodes[nds].position, self._nodes[con_nds].position)
        self.connect()

    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        path_separ = "->"
        tabel = []
        column_list = ["path", "total latency", "total noise", "SNR [dB]"]
        # Data-frame construction
        for id_node1 in self._nodes:
            for id_node2 in self._nodes:
                if id_node1 != id_node2:
                    for path in self.find_paths(id_node1, id_node2):
                        sign_info = Signal_information(1e-3, 0.0, 0.0, path)
                        self.propagate(sign_info, path)
                        # self.probe(sign_info)
                        snr_evaluated = round(snr(sign_info.signal_power, sign_info.noise_power), 3)
                        latency_eng = "{:.3e}".format(sign_info.latency)
                        noisepow_eng = "{:.3e}".format(sign_info.noise_power)
                        row_list = [path_separ.join(path), latency_eng, noisepow_eng,
                                    snr_evaluated]
                        tabel.append(row_list)
        df = pd.DataFrame(tabel, columns=column_list)
        print('Dataframe of all possible paths between all possible nodes: \n', df)

        # Network map and plot
        for id_node in self._nodes:
            x0 = self._nodes[id_node].position[0]
            y0 = self._nodes[id_node].position[1]
            plt.plot(x0, y0, 'yo', markersize=10)
            plt.text(x0 + 20, y0 + 20, id_node)
            for con_node in self._nodes[id_node].connected_nodes:
                x1 = self._nodes[con_node].position[0]
                y1 = self._nodes[con_node].position[1]
                plt.plot([x0, x1], [y0, y1], 'r')
        plt.title('Network')
        plt.xlabel('X[m]')
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        plt.ylabel('Y[m]')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid()
        plt.show()

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2):
        paths = []
        visited = []
        first_node = label1
        last_node = label2
        b_stop = False

        # Pathfinder method
        for nds in self._node2line:
            if nds == first_node:
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
            return paths

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        self._node2line = {}
        self._line2node = {}
        line2node = {}
        for nds in self._nodes:
            for lns in self._lines:
                char = lns[0]
                if nds == char:
                    self._node2line.setdefault(nds, []).append(lns)
        for lns in self._lines:
            char2 = lns[1]
            for nds in self._nodes:
                if nds == char2:
                    n = nds
                    self._line2node.setdefault(lns, []).append(n)
            line2node.setdefault(lns, []).append(self._line2node[lns])
        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information, path):
        for x in range(len(path)-1):
            line = path[x]+path[x+1]
            lin_length = Line(line, self._nodes[path[x]].position, self._nodes[path[x+1]].position)
            noise = lin_length.noise_generation(signal_information.signal_power, lin_length.length)
            latency = lin_length.latency_generation(lin_length.length)
            signal_information.update_noise_power(noise)
            signal_information.update_latency(latency)
        pass

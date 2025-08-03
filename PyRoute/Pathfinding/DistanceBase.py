"""
Created on Feb 25, 2024

@author: CyberiaResurrection
"""
import numpy as np
from networkx.classes import Graph


class DistanceBase:

    def __init__(self, graph: Graph):
        raw_nodes = graph.nodes()
        self._nodes = list(raw_nodes)
        num_nodes = len(self._nodes)
        self._indexes = {node: i for (i, node) in enumerate(self._nodes)}
        positions = [
            raw_nodes[u]['star'].hex.hex_position() for u in self._nodes
        ]
        self._positions = np.zeros((num_nodes, 2), dtype=int)
        for i in range(num_nodes):
            self._positions[i, :] = np.array(positions[i])

    def __len__(self) -> int:
        return len(self._nodes)

    def lighten_edge(self, u: int, v: int, weight: float) -> None:
        raise NotImplementedError("Base Class")

    def distances_from_target(self, active_nodes, target: int) -> int:
        if len(active_nodes) == len(self):
            dq = self._positions[:, 0] - self._positions[target, 0]
            dr = self._positions[:, 1] - self._positions[target, 1]
        else:
            dq = self._positions[active_nodes, 0] - self._positions[target, 0]
            dr = self._positions[active_nodes, 1] - self._positions[target, 1]

        return (abs(dq) + abs(dr) + abs(dq + dr)) // 2

    def _lighten_arc(self, u: int, v: int, weight: float) -> None:
        self._arcs[u][1][self._arcs[u][0] == v] = weight

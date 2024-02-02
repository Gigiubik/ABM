from random import Random
from typing import Any

from mesa.experimental.cell_space.cell import Cell
from mesa.experimental.cell_space.discrete_space import DiscreteSpace


class Network(DiscreteSpace):
    def __init__(
            self,
            G: Any,
            capacity: int | None = None,
            random: Random = None,
            CellKlass: type[Cell] = Cell
    ) -> None:
        """A Networked grid

        Args:
            G: a NetworkX Graph instance.
            capacity (int) : the capacity of the cell
            random (Random):
            CellKlass (type[Cell]): The base Cell class to use in the Network

        """
        super().__init__(capacity=capacity,random=random, CellKlass=CellKlass)
        self.G = G

        for node_id in self.G.nodes:
            self.cells[node_id] = self.CellKlass(node_id, capacity, random=self.random)

        for cell in self.all_cells:
            self._connect_single_cell(cell)

    def _connect_single_cell(self, cell):
        for node_id in self.G.neighbors(cell.coordinate):
            cell.connect(self.cells[node_id])

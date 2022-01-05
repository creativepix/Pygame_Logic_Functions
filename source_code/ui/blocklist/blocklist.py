import pygame
from typing import Iterable, Tuple, Union
from source_code.ui.blocklist.cell_in_blocklist import CellInBlockList
from source_code.ui.list.list import PyList


class BlockList(PyList):
    def __init__(self, block_cells: Iterable[CellInBlockList],
                 rect: pygame.Rect,
                 color: Union[Tuple[int, int, int], pygame.Color] = None):
        super().__init__(block_cells, rect, 0, color)

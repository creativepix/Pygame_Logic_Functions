from typing import Callable, Union

import pygame
from source_code.block_scheme.blocks.base_block import BaseBlock
from source_code.constants import BLOCKS_WIDTH, BLOCKS_NAME_COLOR, \
    BLOCK_MIN_SIZE, BLOCKS_COLOR, SPACE_BLOCKS_IN_BLOCK_LIST, BACKGROUND_COLOR
from source_code.ui.list.cell_in_list import CellInList


class CellInBlockList(CellInList):
    def __init__(self, copy_block: BaseBlock, action: Callable):
        super().__init__(copy_block.name, BLOCK_MIN_SIZE, action)
        self.rect = copy_block.rect
        self.copy_block = copy_block

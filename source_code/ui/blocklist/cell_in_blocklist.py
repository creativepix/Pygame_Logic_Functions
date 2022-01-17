from typing import Callable
from source_code.constants import BLOCKS_NAME_COLOR
from source_code.ui.list.cell_in_list import CellInList
from source_code.block_scheme.blocks.base_block import BaseBlock


class CellInBlockList(CellInList):
    def __init__(self, copy_block: BaseBlock, action: Callable):
        super().__init__(copy_block.name, action, img=copy_block.img,
                         text_color=BLOCKS_NAME_COLOR)
        self.rect = copy_block.rect
        self.copy_block = copy_block

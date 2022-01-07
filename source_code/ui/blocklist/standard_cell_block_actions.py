import sqlite3

import pygame
from typing import Callable
from source_code import global_vars
from source_code.block_scheme.blocks.builder_base_block import BuilderBaseBlock
from source_code.constants import TEXT_COLOR, MAX_LEN_BLOCK_NAME
from source_code.ui.blocklist.cell_in_blocklist import CellInBlockList
from source_code.ui.input_field import PyInputField
from source_code.ui.list.cell_in_list import CellInList
from source_code.ui.table import PyTable
from source_code.windows.base_game_window import BaseGameWindow
from source_code.windows.base_window import BaseWindow


def make_copy_block(cell_block: CellInBlockList,
                    base_game_window: BaseGameWindow) -> Callable:
    """Сделать копию блока на поле"""
    def cmd() -> None:
        new_block = cell_block.copy_block.copy()
        base_game_window.all_blocks.append(new_block)

        new_block.rect.x = pygame.mouse.get_pos()[0] - new_block.rect.w // 2
        new_block.rect.y = pygame.mouse.get_pos()[1] - new_block.rect.h // 2
        new_block.is_dragging = True
        new_block.last_mouse_pos = pygame.mouse.get_pos()
    return cmd

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
    def cmd() -> None:
        new_block = cell_block.copy_block.copy()
        base_game_window.all_blocks.append(new_block)

        new_block.rect.x = pygame.mouse.get_pos()[0] - new_block.rect.w // 2
        new_block.rect.y = pygame.mouse.get_pos()[1] - new_block.rect.h // 2
        new_block.is_dragging = True
        new_block.last_mouse_pos = pygame.mouse.get_pos()
    return cmd


def choose_for_edit_block(cell_block: BuilderBaseBlock) -> Callable:
    def cmd() -> None:
        from source_code.windows.sandbox_window import SandboxWindow

        global_vars.ACTIVE_WINDOW = SandboxWindow(cell_block.name)
    return cmd


def delete_custom_block_row(del_cell_in_list: CellInList, pytable: PyTable,
                            block_list_id: int) -> Callable:
    def cmd() -> None:
        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()

        py_row_id = None
        for pylist_id, pylist in enumerate(pytable.pylists):
            if del_cell_in_list in pylist.cells:
                py_row_id = pylist.cells.index(del_cell_in_list)
        if py_row_id is None:
            return

        block_name = pytable.pylists[block_list_id].cells[py_row_id].text
        for pylist in pytable.pylists:
            del pylist.cells[py_row_id]
        print(block_name)

        cur.execute(f'DELETE FROM ALL_CUSTOM_BLOCKS '
                    f'WHERE BLOCK_NAME="{block_name}"')
        con.commit()
        con.close()
    return cmd

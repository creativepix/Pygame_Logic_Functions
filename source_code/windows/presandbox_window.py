import sqlite3

import pygame

from source_code import global_vars
from source_code.block_scheme.blocks.and_block import AndBlock
from source_code.block_scheme.blocks.custom_block import CustomBlock
from source_code.block_scheme.blocks.input_block import InputBlock
from source_code.block_scheme.blocks.not_block import NotBlock
from source_code.block_scheme.blocks.or_block import OrBlock
from source_code.block_scheme.blocks.output_block import OutputBlock
from source_code.constants import BLOCK_MIN_SIZE, BLOCK_LIST_WIDTH, TEXT_COLOR, \
    TABLE_X_SYMBOL_SIZE
from source_code.global_vars import ACTIVE_SCREEN
from source_code.ui.blocklist.blocklist import BlockList
from source_code.ui.blocklist.cell_in_blocklist import CellInBlockList
from source_code.ui.blocklist.standard_cell_block_actions import \
    choose_for_edit_block, delete_custom_block_row
from source_code.ui.list.cell_in_list import CellInList
from source_code.ui.list.list import PyList
from source_code.ui.list.standard_cell_list_actions import \
    open_entering_custom_block_name
from source_code.ui.table import PyTable
from source_code.windows.base_window import BaseWindow, disable_if_message


class PresandboxWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
        all_custom_blocks = cur.execute(
            f"""SELECT BLOCK_NAME, STRUCTURE FROM ALL_CUSTOM_BLOCKS"""). \
            fetchall()
        size_blocks = pygame.Rect(0, 0, *BLOCK_MIN_SIZE)

        cells_in_list, del_cells_in_list = [], []
        for custom_block in all_custom_blocks:
            block = CustomBlock(custom_block[0], custom_block[1],
                                self, size_blocks)
            cell_in_list = CellInList(
                custom_block[0], BLOCK_MIN_SIZE, choose_for_edit_block(block))
            cells_in_list.append(cell_in_list)

            cell_in_list = CellInList('x', TABLE_X_SYMBOL_SIZE, lambda: None)
            del_cells_in_list.append(cell_in_list)

        adding_cell_in_block_list = CellInList(
            '+', BLOCK_MIN_SIZE, lambda: None)
        adding_cell_in_block_list.action = open_entering_custom_block_name(
            self, adding_cell_in_block_list)
        cells_in_list.append(adding_cell_in_block_list)

        rect = pygame.Rect(0, 150, ACTIVE_SCREEN.get_width(),
                           ACTIVE_SCREEN.get_height() - 150)
        choose_list = PyList(cells_in_list, rect, 0, (0, 0, 0, 0))
        rect = pygame.Rect(size_blocks.w, rect.y, rect.w, rect.h)
        del_cells_list = PyList(del_cells_in_list, rect, 0, (0, 0, 0, 0))
        self.choose_edit_block_table = PyTable([choose_list, del_cells_list])

        for del_cell_in_list in del_cells_in_list:
            del_cell_in_list.action = delete_custom_block_row(
                del_cell_in_list, self.choose_edit_block_table, 0)

        con.close()

    def tick(self, screen: pygame.Surface) -> None:
        self.choose_edit_block_table.render(screen)
        font = pygame.font.Font(None, 75)
        for i, line in enumerate(['Выберите блок',
                                  'для редактирования'], start=1):
            widget = font.render(line, True, TEXT_COLOR)
            font_rect = widget.get_rect()
            font_rect.center = (self.choose_edit_block_table.rect.centerx,
                                i * 50)
            screen.blit(widget, font_rect)

    @disable_if_message
    def mouse_wheel(self, koof: int) -> None:
        self.choose_edit_block_table.mouse_wheel(koof)

    @disable_if_message
    def mouse_down(self, mouse_button: int) -> None:
        if mouse_button == 1:
            self.choose_edit_block_table.mouse_down()

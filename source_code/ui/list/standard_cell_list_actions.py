import pygame
import sqlite3
from typing import Callable
from source_code import global_vars
from source_code.ui.table import PyTable
from source_code.ui.input_field import PyInputField
from source_code.windows.base_window import BaseWindow
from source_code.ui.list.cell_in_list import CellInList
from source_code.windows.sandbox_window import SandboxWindow
from source_code.constants import TEXT_COLOR, MAX_LEN_BLOCK_NAME, \
    NOT_EDITABLE_BLOCKS


def open_entering_custom_block_name(
        base_window: BaseWindow, cell_in_block_list: CellInList) \
        -> Callable:
    """Создать новый кастомный блок с вводом его имени"""
    def cmd() -> None:
        def open_sandbox_window(block_name: str) -> None:
            if block_name in NOT_EDITABLE_BLOCKS:
                global_vars.ACTIVE_WINDOW.show_message(
                    'You cannot edit base block')
            elif any(block_name):
                global_vars.ACTIVE_WINDOW = SandboxWindow(block_name)

        inp_field = PyInputField(font=pygame.font.Font(None, 25),
                                 color=TEXT_COLOR, rect=cell_in_block_list.rect,
                                 enter_action=open_sandbox_window,
                                 max_symbols=MAX_LEN_BLOCK_NAME)
        cell_in_block_list.text = inp_field
        base_window.all_inp_fields.append(inp_field)
    return cmd


def choose_for_edit_block(cell_block_name: str) -> Callable:
    """Открыть блок для редактирования в песочнице"""
    def cmd() -> None:
        from source_code.windows.sandbox_window import SandboxWindow

        global_vars.ACTIVE_WINDOW = SandboxWindow(cell_block_name)
    return cmd


def delete_custom_block_row(del_cell_in_list: CellInList, pytable: PyTable,
                            block_list_id: int) -> Callable:
    """Удалить касмтоный блок из выпадающего списка в PresandboxWindow"""
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

        cur.execute(f'DELETE FROM ALL_CUSTOM_BLOCKS '
                    f'WHERE BLOCK_NAME="{block_name}"')
        con.commit()
        con.close()
    return cmd


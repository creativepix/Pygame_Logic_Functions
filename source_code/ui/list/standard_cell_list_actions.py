from typing import Callable

import pygame

from source_code import global_vars
from source_code.constants import TEXT_COLOR, MAX_LEN_BLOCK_NAME
from source_code.ui.input_field import PyInputField
from source_code.ui.list.cell_in_list import CellInList
from source_code.windows.base_window import BaseWindow
from source_code.windows.sandbox_window import SandboxWindow


def open_entering_custom_block_name(
        base_window: BaseWindow, cell_in_block_list: CellInList) \
        -> Callable:
    def cmd() -> None:
        def open_sandbox_window(block_name: str) -> None:
            if any(block_name):
                global_vars.ACTIVE_WINDOW = SandboxWindow(block_name)

        inp_field = PyInputField(font=pygame.font.Font(None, 25),
                                 color=TEXT_COLOR, rect=cell_in_block_list.rect,
                                 enter_action=open_sandbox_window,
                                 max_symbols=MAX_LEN_BLOCK_NAME)
        cell_in_block_list.text = inp_field
        base_window.all_inp_fields.append(inp_field)
    return cmd

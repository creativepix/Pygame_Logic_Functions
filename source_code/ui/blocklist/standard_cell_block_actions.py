import pygame
from typing import Callable
from source_code.ui.blocklist.cell_in_blocklist import CellInBlockList
from source_code.windows.base_game_window import BaseGameWindow


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

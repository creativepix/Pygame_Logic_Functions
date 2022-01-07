import pygame
from typing import List, Iterable

from source_code.constants import BLOCK_LIST_WIDTH
from source_code.global_vars import ACTIVE_SCREEN
from source_code.windows.base_window import BaseWindow, disable_if_message, \
    mouse_down_check_message


class BaseGameWindow(BaseWindow):
    def __init__(self, available_blocklists: Iterable):
        from source_code.block_scheme.blocks.builder_base_block import \
            BuilderBaseBlock
        from source_code.ui.blocklist.blocklist import BlockList

        super().__init__()

        self.all_blocks: List[BuilderBaseBlock] = []
        self.id_connections = {None: None}

        self.is_moving = False
        self.last_mouse_pos = pygame.mouse.get_pos()

        rect = pygame.Rect(ACTIVE_SCREEN.get_width() - BLOCK_LIST_WIDTH, 0,
                           BLOCK_LIST_WIDTH, ACTIVE_SCREEN.get_height())
        self.choose_block_list = BlockList(available_blocklists, rect)

    def update_id_connections(self) -> None:
        connection_id = 0
        self.id_connections = {None: None}
        for block in self.all_blocks:
            for connection in block.inputs + block.outputs:
                self.id_connections[connection] = connection_id
                connection_id += 1

    def tick(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))

        for block in self.all_blocks:
            block.render(screen)

        self.choose_block_list.render(screen)

    @mouse_down_check_message
    def mouse_down(self, mouse_button: int) -> None:
        if mouse_button == 3:
            for block in self.all_blocks:
                if block.is_selected():
                    block.delete()
            return
        elif mouse_button != 1:
            return

        if self.choose_block_list.rect.collidepoint(pygame.mouse.get_pos()):
            self.choose_block_list.mouse_down()
            return

        smth_is_selected = False
        for block in self.all_blocks:
            if not smth_is_selected and block.is_selected():
                smth_is_selected = True
            block.mouse_down()
            if not smth_is_selected:
                for connection in block.inputs + block.outputs:
                    if connection.is_selected():
                        smth_is_selected = True
        if not smth_is_selected:
            self.is_moving = True
            self.last_mouse_pos = pygame.mouse.get_pos()

        super().mouse_down(mouse_button)

    @disable_if_message
    def mouse_motion(self) -> None:
        if self.is_moving:
            for block in self.all_blocks:
                block.move(pygame.mouse.get_pos()[0] - self.last_mouse_pos[0],
                           pygame.mouse.get_pos()[1] - self.last_mouse_pos[1])
            self.last_mouse_pos = pygame.mouse.get_pos()
            return

        for block in self.all_blocks:
            block.mouse_motion()

    @disable_if_message
    def mouse_up(self) -> None:
        if self.is_moving:
            self.is_moving = False
            return

        for block in self.all_blocks:
            block.mouse_up()

    @disable_if_message
    def mouse_wheel(self, koof: int) -> None:
        if self.choose_block_list.rect.collidepoint(pygame.mouse.get_pos()):
            self.choose_block_list.mouse_wheel(koof)
            return

        for block in self.all_blocks:
            block.zoom(koof)
            if any([block.rect.colliderect(block_check.rect)
                    for block_check in self.all_blocks
                    if block_check != block]):
                block.zoom(-koof)

    @disable_if_message
    def double_mouse_click(self) -> None:
        for block in self.all_blocks:
            block.double_mouse_click()

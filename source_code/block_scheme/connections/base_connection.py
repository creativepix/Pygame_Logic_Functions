import pygame
from typing import Tuple
from source_code.block_scheme.blocks.builder_base_block import BuilderBaseBlock
from source_code.block_scheme.connections.builder_base_connection import \
    BuilderBaseConnection
from source_code.constants import BLOCK_CONNECTION_TRUE_COLOR, \
    BLOCK_CONNECTION_FALSE_COLOR, BLOCKS_INDENT_FOR_RESIZING
from source_code.windows.builder_base_game_window import BuilderBaseGameWindow


class BaseConnection(BuilderBaseConnection):
    def __init__(self, base_game_window: BuilderBaseGameWindow,
                 parent_block: BuilderBaseBlock,
                 local_coord_percents: Tuple[int, int]):
        super().__init__(base_game_window, parent_block, local_coord_percents)

    def render(self, screen: pygame.Surface) -> None:
        p_rect = self.parent_block.rect
        color = (BLOCK_CONNECTION_TRUE_COLOR if self.signal else
                 BLOCK_CONNECTION_FALSE_COLOR)
        pygame.draw.circle(screen, color, [
            int(p_rect.x + p_rect.w / 100 * self.local_coord_percents[0]),
            int(p_rect.y + p_rect.h / 100 * self.local_coord_percents[1])
        ], min(
            int(self.parent_block.rect.w / 100 * self.local_radius_percentage),
            int(self.parent_block.rect.h / 100 * 25)
        ))

        if self.is_attached_to_cursor:
            pygame.draw.line(screen, color, self.get_rect().center,
                             pygame.mouse.get_pos(),
                             width=BLOCKS_INDENT_FOR_RESIZING)

        for attached_connection in self.attached_connections:
            if attached_connection is not None:
                to_coords = attached_connection.get_rect().center
                pygame.draw.line(screen, color,
                                 self.get_rect().center, to_coords,
                                 width=BLOCKS_INDENT_FOR_RESIZING)

    def get_rect(self) -> pygame.Rect:
        p_rect = self.parent_block.rect
        return pygame.rect.Rect(
            int(p_rect.x + p_rect.w / 100 * self.local_coord_percents[0] -
                self.local_radius_percentage),
            int(p_rect.y + p_rect.h / 100 * self.local_coord_percents[1] -
                self.local_radius_percentage),
            self.local_radius_percentage * 2, self.local_radius_percentage * 2)

    def mouse_down(self) -> None:
        if self.is_selected():
            self.parent_block.connection_editing = self
            self.is_attached_to_cursor = True

    def mouse_up(self) -> None:
        self.is_attached_to_cursor = False
        if self.parent_block.connection_editing is self:
            self.parent_block.connection_editing = None
            for block in self.base_game_window.all_blocks:
                if block is not self.parent_block:
                    for connection in block.inputs + block.outputs:
                        if connection.get_rect().collidepoint(
                                pygame.mouse.get_pos()):
                            if connection in self.attached_connections:
                                self.detach(connection)
                            else:
                                self.attach(connection)
                            return

    def is_selected(self) -> bool:
        return self.get_rect().collidepoint(pygame.mouse.get_pos())

    def attach(self, to_connection: BuilderBaseConnection) -> None:
        self.attached_connections.append(to_connection)
        to_connection.attached_connections.append(self)
        to_connection.signal = self.signal

    def detach(self, connection: BuilderBaseConnection) -> None:
        if self in connection.attached_connections:
            del connection.attached_connections[
                connection.attached_connections.index(self)]
            del self.attached_connections[
                self.attached_connections.index(connection)]

    @property
    def signal(self) -> bool:
        return self._signal

    @signal.setter
    def signal(self, value) -> None:
        if self._signal != value:
            self._signal = value
            self.parent_block.update_output_signals()
            for attached_connection in self.attached_connections:
                attached_connection.signal = self._signal

    def copy(self):
        return self.__copy__()

    def __str__(self):
        return self.__repr__()

    def __repr__(self, header: str = 'BaseConnection'):
        attached_con_ids = []
        for attached_connection in self.attached_connections:
            attached_con_ids.append(
                self.base_game_window.id_connections[attached_connection])
        return f'{header}(' \
               f'{self.base_game_window.id_connections[self]},' \
               f'{attached_con_ids},' \
               f'{tuple(map(int, self.local_coord_percents))})'

    def __copy__(self):
        return BaseConnection(self.base_game_window, self.parent_block,
                              self.local_coord_percents)

import pygame
from source_code.block_scheme.blocks.base_block import BaseBlock
from source_code.block_scheme.connections.input_connection import \
    InputConnection
from source_code.windows.builder_base_game_window import BuilderBaseGameWindow


class OutputBlock(BaseBlock):
    def __init__(self, base_game_window: BuilderBaseGameWindow,
                 rect: pygame.rect.Rect):
        super().__init__(
            base_game_window, 'output', rect, lambda inputs: [],
            [InputConnection(base_game_window, self, (100 // 2, 100))], [])

    def __str__(self):
        return self.__repr__()

    def __repr__(self, *args):
        return super().__repr__('OutputBlock')

    def __copy__(self):
        new_block = OutputBlock(self.base_game_window, self.rect)
        for connection in new_block.inputs + new_block.outputs:
            connection.parent_block = new_block
        return new_block

import pygame
from source_code.block_scheme.blocks.base_block import BaseBlock
from source_code.block_scheme.connections.output_connection import \
    OutputConnection
from source_code.windows.base_game_window import BaseGameWindow


class InputBlock(BaseBlock):
    def __init__(self, base_game_window: BaseGameWindow,
                 rect: pygame.rect.Rect):
        super().__init__(
            base_game_window, 'input', rect,
            lambda inputs: [], [], [
                OutputConnection(base_game_window, self, (100 // 2, 0))
            ])

    def double_mouse_click(self) -> None:
        if self.is_selected():
            for out_con in self.outputs:
                out_con.signal = not out_con.signal

    def __str__(self):
        return self.__repr__()

    def __repr__(self, *args):
        return super().__repr__('InputBlock')

    def __copy__(self):
        new_block = InputBlock(self.base_game_window, self.rect)
        for connection in new_block.inputs + new_block.outputs:
            connection.parent_block = new_block
        return new_block

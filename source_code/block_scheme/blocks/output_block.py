import pygame
from source_code.block_scheme.blocks.base_block import BaseBlock
from source_code.block_scheme.connections.input_connection import \
    InputConnection
from source_code.constants import BLOCK_TEXT_MIN_SIZE, BLOCK_ID_BASE_COORDS, \
    BLOCKS_NAME_COLOR
from source_code.windows.builder_base_game_window import BuilderBaseGameWindow


class OutputBlock(BaseBlock):
    def __init__(self, base_game_window: BuilderBaseGameWindow,
                 rect: pygame.rect.Rect, output_id: int = None):
        super().__init__(
            base_game_window, 'output', rect, lambda inputs: [],
            [InputConnection(base_game_window, self, (100 // 2, 100))], [])
        self.output_id = output_id

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)

        if self.output_id is not None:
            font = pygame.font.Font(None, BLOCK_TEXT_MIN_SIZE *
                                    (2 ** self.size_koof))
            widget = font.render(str(self.output_id), True, BLOCKS_NAME_COLOR)
            font_rect = widget.get_rect()
            font_rect.x = self.rect.x + BLOCK_ID_BASE_COORDS[0]
            font_rect.y = self.rect.y + BLOCK_ID_BASE_COORDS[1]
            screen.blit(widget, font_rect)

    def __str__(self):
        return self.__repr__()

    def __repr__(self, *args):
        return super().__repr__('OutputBlock')

    def __copy__(self):
        new_block = OutputBlock(self.base_game_window, self.rect)
        for connection in new_block.inputs + new_block.outputs:
            connection.parent_block = new_block
        return new_block

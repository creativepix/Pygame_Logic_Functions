from typing import Union

import pygame
from source_code.block_scheme.blocks.base_block import BaseBlock
from source_code.block_scheme.connections.input_connection import \
    InputConnection
from source_code.block_scheme.connections.output_connection import \
    OutputConnection
from source_code.block_scheme.data.structure_cmds import \
    get_cmd_line_from_structure
from source_code.windows.base_game_window import BaseGameWindow


class CustomBlock(BaseBlock):
    def __init__(self, name: str, structure: str,
                 base_game_window: BaseGameWindow, rect: pygame.rect.Rect,
                 img: Union[str, pygame.Surface] = None):
        ins_len = structure.count('InputBlock')
        outs_len = structure.count('OutputBlock')

        input_connections = []
        for i in range(ins_len):
            adding = InputConnection(base_game_window, self,
                                     (int(100 / (ins_len + 1) * (i + 1)), 100))
            input_connections.append(adding)

        output_connections = []
        for i in range(outs_len):
            adding = OutputConnection(base_game_window, self,
                                      (int(100 / (outs_len + 1) * (i + 1)), 0))
            output_connections.append(adding)

        super().__init__(base_game_window, name, rect, lambda inputs: [],
                         input_connections, output_connections, img=img)
        self.structure = structure
        self.cmd_line = get_cmd_line_from_structure(self.structure)

    def update_connection_signals(self):
        pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self, *args):
        ans = f'CustomBlock({self.name},{self.rect}'
        for connection in self.inputs + self.outputs:
            ans += f',{connection}'
        return ans + ')'

    def __copy__(self):
        new_block = CustomBlock(self.name, self.structure,
                                self.base_game_window, self.rect, self.img)
        for connection in new_block.inputs + new_block.outputs:
            connection.parent_block = new_block
        return new_block

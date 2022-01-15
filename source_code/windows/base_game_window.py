import sqlite3
import pygame
from typing import List, Iterable, Type, Union, Callable
from source_code.block_scheme.blocks.and_block import AndBlock
from source_code.block_scheme.blocks.custom_block import CustomBlock
from source_code.block_scheme.blocks.input_block import InputBlock
from source_code.block_scheme.blocks.not_block import NotBlock
from source_code.block_scheme.blocks.or_block import OrBlock
from source_code.block_scheme.blocks.output_block import OutputBlock
from source_code.block_scheme.connections.base_connection import BaseConnection
from source_code.block_scheme.connections.builder_base_connection import \
    BuilderBaseConnection
from source_code.block_scheme.connections.input_connection import \
    InputConnection
from source_code.block_scheme.connections.output_connection import \
    OutputConnection
from source_code.constants import BLOCK_LIST_WIDTH, BLOCK_MIN_SIZE
from source_code.errors.block_error import BlockError
from source_code.global_vars import ACTIVE_SCREEN
from source_code.windows.base_window import BaseWindow, disable_if_message, \
    mouse_down_check_message
from source_code.windows.builder_base_game_window import BaseGameWindowBuilder


# Базовое игровое окно. На нём базируются песочница и сама игра
class BaseGameWindow(BaseWindow, BaseGameWindowBuilder):
    def __init__(self, available_blocklists: Iterable):
        from source_code.ui.blocklist.blocklist import BlockList
        super().__init__()

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
        for btn in self.all_btns:
            btn.render(screen)
        self.choose_block_list.render(screen)

        if self.message_window is not None:
            self.message_window.render(screen)

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
                block.last_rect = block.rect
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

    def load(self, structure_line: str,
             cursor: sqlite3.Cursor = None) -> None:
        """загрузка сохранённой структуры"""
        if not any(structure_line):
            return

        if cursor is None:
            con = sqlite3.connect(
                './source_code/block_scheme/data/blocks.db')
            cursor = con.cursor()

        all_con_ids = {}
        needed_con_ids = {}

        def check_digit(elem: str):
            return int(elem) if elem.isdigit() else None

        for block in structure_line.split('|'):
            name_block = block.split('(')[0]
            rect = pygame.rect.Rect(list(map(
                int, block.split('<rect(')[1].split(')>')[0].split(', '))))
            if name_block == 'InputBlock':
                new_block = InputBlock(self, rect)
            elif name_block == 'OutputBlock':
                new_block = OutputBlock(self, rect)
            elif name_block == 'AndBlock':
                new_block = AndBlock(self, rect)
            elif name_block == 'OrBlock':
                new_block = OrBlock(self, rect)
            elif name_block == 'NotBlock':
                new_block = NotBlock(self, rect)
            elif name_block == 'CustomBlock':
                name = block.split('(')[1].split(',')[0]
                info = cursor.execute(f'SELECT STRUCTURE, IMAGE_PATh '
                                      f'FROM ALL_CUSTOM_BLOCKS '
                                      f'WHERE BLOCK_NAME = "{name}"'
                                      ).fetchall()
                if any(info):
                    structure = info[0][0]
                    image_path = info[0][1]
                    new_block = CustomBlock(name, structure, self, rect,
                                            img=image_path)
                else:
                    put_cons = []
                    if 'InputConnection(' in block:
                        put_cons += block.split('InputConnection(')[1:]
                    if 'OutputConnection(' in block:
                        put_cons += block.split('OutputConnection(')[1:]
                    for put_con in put_cons:
                        put_con = put_con.split('))')[0]
                        put_con_ids = [check_digit(put_con.split(',')[0])]
                        all_con_ids[put_con_ids[0]] = None
                    continue
            else:
                raise BlockError(f'Name: {name_block}')
            new_block.name = block.split('(')[1].split(',')[0]

            new_inputs, new_outputs = [], []

            def add_con(con_class: Type[BaseConnection]):
                con_coord_percents = tuple(
                    map(int,
                        put_con.split(',(')[1].split(')')[0].split(', ')))
                if len(con_coord_percents) != 2:
                    raise BlockError

                new_connection = con_class(self, new_block,
                                           con_coord_percents)

                if isinstance(new_connection, InputConnection):
                    new_inputs.append(new_connection)
                elif isinstance(new_connection, OutputConnection):
                    new_outputs.append(new_connection)
                else:
                    raise BlockError

                con_ids = [check_digit(put_con.split(',')[0]),
                           [check_digit(elem) for elem in
                            put_con.split('[')[1].split(']')[0].split(
                                ', ')]]
                all_con_ids[con_ids[0]] = new_connection
                needed_con_ids[new_connection] = con_ids[1]

            if 'InputConnection(' in block:
                for put_con in block.split('InputConnection(')[1:]:
                    put_con = put_con.split('))')[0]
                    add_con(InputConnection)
            if 'OutputConnection(' in block:
                for put_con in block.split('OutputConnection(')[1:]:
                    put_con = put_con.split('))')[0]
                    add_con(OutputConnection)

            if len(new_block.inputs) != len(new_inputs):
                def update_wrong_connections(
                        blocks_puts: List[BuilderBaseConnection],
                        new_puts: List[BuilderBaseConnection],
                        con_class: Type[BaseConnection]):
                    if len(blocks_puts) > len(new_puts):
                        for _ in range(len(blocks_puts) - len(new_puts)):
                            new_puts.append(
                                con_class(self, new_block, (10, 10)))
                    else:
                        while len(blocks_puts) != len(new_puts):
                            needed_con_ids[new_puts[-1]] = []
                            for key, value in all_con_ids.items():
                                if value is new_puts[-1]:
                                    all_con_ids[key] = None
                                    break
                            del new_puts[-1]

                update_wrong_connections(
                    new_block.inputs, new_inputs, InputConnection)
                update_wrong_connections(
                    new_block.outputs, new_outputs, OutputConnection)

                for i, new_input in enumerate(new_inputs):
                    new_input.local_coord_percents = \
                        ((i + 1) * 100 / (len(new_inputs) + 1), 100)
                for i, new_output in enumerate(new_outputs):
                    new_output.local_coord_percents = \
                        ((i + 1) * 100 / (len(new_outputs) + 1), 0)

            new_block.inputs = new_inputs
            new_block.outputs = new_outputs

            min_side = max(BLOCK_MIN_SIZE[0],
                           min(new_block.rect.w, new_block.rect.h))
            new_block.rect.w = min_side
            new_block.rect.h = min_side

            new_block.update_output_signals()

            self.all_blocks.append(new_block)

        for con_to_edit, cons_to_edit_id in needed_con_ids.items():
            if not any(cons_to_edit_id):
                continue
            for con_to_edit_id in cons_to_edit_id:
                if con_to_edit_id is not None and \
                        all_con_ids[con_to_edit_id] is not None:
                    con_to_edit.attach(all_con_ids[con_to_edit_id])

    def _save(self, table: str, checking_parameter: str,
              value_checking_parameter: Union[int, str],
              not_in_table_action: Callable[[sqlite3.Cursor, str, str], None])\
            -> None:
        """сохранение нынешней структуры"""
        inputs = []
        structure = []
        for block in self.all_blocks:
            if isinstance(block, InputBlock):
                inputs.append(str(block.outputs[0].signal))
            structure.append(str(block))
        structure = '|'.join(structure).strip('|')
        inputs = ' '.join(inputs)

        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
        my_id = cur.execute(f"""
SELECT ID FROM {table}
WHERE {checking_parameter} = '{value_checking_parameter}'""").fetchall()
        if any(my_id):
            my_id = my_id[0][0]
            cur.execute(f"""
UPDATE {table}
SET {checking_parameter} = '{value_checking_parameter}',
STRUCTURE = '{structure}',
INPUTS = '{inputs}'
WHERE ID = {my_id}""")
        else:
            not_in_table_action(cur, structure, inputs)
        con.commit()
        con.close()

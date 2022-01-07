import sqlite3
from typing import List, Type

import pygame

from source_code import global_vars
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
from source_code.constants import BLOCK_MIN_SIZE, TEXT_COLOR, SAVE_BTN_RECT, \
    BACK_BTN_RECT
from source_code.errors.block_error import BlockError
from source_code.ui.blocklist.cell_in_blocklist import CellInBlockList
from source_code.ui.blocklist.standard_cell_block_actions import \
    make_copy_block
from source_code.ui.button import PyButton
from source_code.ui.message_window import MessageWindow
from source_code.windows.base_game_window import BaseGameWindow


class SandboxWindow(BaseGameWindow):
    def __init__(self, block_name: str):
        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
        all_custom_blocks = cur.execute(
            f"SELECT BLOCK_NAME, STRUCTURE, IMAGE_PATH "
            f"FROM ALL_CUSTOM_BLOCKS").fetchall()
        size_blocks = pygame.Rect(0, 0, *BLOCK_MIN_SIZE)

        base_blocklists, custom_blocklists = [], []
        for block in [InputBlock(self, size_blocks),
                      OutputBlock(self, size_blocks),
                      AndBlock(self, size_blocks),
                      OrBlock(self, size_blocks),
                      NotBlock(self, size_blocks)]:
            cell_block = CellInBlockList(block, lambda: None)
            cell_block.action = make_copy_block(cell_block, self)
            base_blocklists.append(cell_block)
        for custom_block in all_custom_blocks:
            if custom_block[0] == block_name:
                continue
            block = CustomBlock(custom_block[0], custom_block[1],
                                self, size_blocks, img=custom_block[2])
            cell_block = CellInBlockList(block, lambda: None)
            cell_block.action = make_copy_block(cell_block, self)
            custom_blocklists.append(cell_block)
        all_listblocks = (base_blocklists + custom_blocklists)

        super().__init__(all_listblocks)

        self.editing_block_name = block_name

        def back_action():
            from source_code.windows.main_menu_window import MainMenuWindow
            global_vars.ACTIVE_WINDOW = MainMenuWindow()

        def save_action():
            self.update_id_connections()
            try:
                self.save(self.editing_block_name)
                txt = 'Successfully saved!'
            except RecursionError:
                txt = 'Cannot save. Cause is max recursion error.!'
            message_rect = pygame.Rect(
                0, 0, *global_vars.ACTIVE_SCREEN.get_size())
            self.message_window = MessageWindow(txt, message_rect)

        self.save_btn = PyButton(text='Save', font=pygame.font.Font(None, 25),
                                 color=TEXT_COLOR, rect=SAVE_BTN_RECT,
                                 action=save_action)
        self.back_btn = PyButton(text='Back', font=pygame.font.Font(None, 25),
                                 color=TEXT_COLOR, rect=BACK_BTN_RECT,
                                 action=back_action)

        self.all_btns = [self.save_btn, self.back_btn]

        info = cur.execute(
            f"SELECT STRUCTURE, INPUTS FROM ALL_CUSTOM_BLOCKS "
            f"WHERE BLOCK_NAME = '{self.editing_block_name}'").fetchall()
        if any(info):
            self.load(info[0][0])
            if info[0][1] is not None:
                input_signals = [input_signal == 'True' for input_signal in
                                 info[0][1].split(' ')]
                input_blocks = [block for block in self.all_blocks
                                if isinstance(block, InputBlock)]
                for i, block in enumerate(input_blocks):
                    try:
                        block.outputs[0].signal = input_signals[i]
                    except IndexError:
                        block.outputs[0].signal = False
        con.close()

    def tick(self, screen: pygame.Surface) -> None:
        super().tick(screen)
        self.save_btn.render(screen)
        self.back_btn.render(screen)
        if self.message_window is not None:
            self.message_window.render(screen)

    # загрузка сохранённой структуры
    def load(self, structure_line: str, cursor: sqlite3.Cursor = None) -> None:
        if not any(structure_line):
            return

        if cursor is None:
            con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
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
                    map(int, put_con.split(',(')[1].split(')')[0].split(', ')))
                if len(con_coord_percents) != 2:
                    raise BlockError

                new_connection = con_class(self, new_block, con_coord_percents)

                if isinstance(new_connection, InputConnection):
                    new_inputs.append(new_connection)
                elif isinstance(new_connection, OutputConnection):
                    new_outputs.append(new_connection)
                else:
                    raise BlockError

                con_ids = [check_digit(put_con.split(',')[0]),
                           [check_digit(elem) for elem in
                            put_con.split('[')[1].split(']')[0].split(', ')]]
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

    # сохранение нынешней структуры
    def save(self, custom_block_name: str) -> None:
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
SELECT ID FROM ALL_CUSTOM_BLOCKS
WHERE BLOCK_NAME = '{custom_block_name}'""").fetchall()
        if any(my_id):
            my_id = my_id[0][0]
            cur.execute(f"""
UPDATE ALL_CUSTOM_BLOCKS
SET BLOCK_NAME = '{custom_block_name}',
STRUCTURE = '{structure}',
INPUTS = '{inputs}'
WHERE ID = {my_id}""")
        else:
            last_id = cur.execute(f"""SELECT MAX(ID) FROM ALL_CUSTOM_BLOCKS"""
                                  ).fetchall()[0][0]
            if last_id is None:
                last_id = 0
            last_id += 1
            cur.execute(f"""
INSERT INTO ALL_CUSTOM_BLOCKS 
VALUES({last_id},'{custom_block_name}','{structure}','{inputs}','')""")
        con.commit()
        con.close()

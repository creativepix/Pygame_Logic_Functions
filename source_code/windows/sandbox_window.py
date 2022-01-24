import os
import shutil
import random
import pygame
import sqlite3
from typing import Callable
from source_code import global_vars
from source_code.block_scheme.blocks.and_block import AndBlock
from source_code.block_scheme.blocks.custom_block import CustomBlock
from source_code.block_scheme.blocks.input_block import InputBlock
from source_code.block_scheme.blocks.not_block import NotBlock
from source_code.block_scheme.blocks.or_block import OrBlock
from source_code.block_scheme.blocks.output_block import OutputBlock
from source_code.block_scheme.data.structure_cmds import \
    custom_block_in_structure
from source_code.constants import TEXT_COLOR, SAVE_BTN_RECT, \
    BACK_BTN_RECT, SAVE_PIC_BTN_RECT, BLOCK_SIZE_IN_BLOCK_LIST, \
    CUSTOM_BLOCK_IMAGES_PATH, FONT_NAME
from source_code.errors.no_output_block_error import NoOutputBlockError
from source_code.middlewares.window_transition_actions import \
    to_main_menu_action
from source_code.ui.blocklist.cell_in_blocklist import CellInBlockList
from source_code.ui.blocklist.standard_cell_block_actions import \
    make_copy_block
from source_code.ui.button import PyButton
from source_code.ui.message_window.drop_file_window import DropFileWindow
from source_code.windows.base_game_window import BaseGameWindow
from source_code.windows.base_window import mouse_down_check_message


class SandboxWindow(BaseGameWindow):
    def __init__(self, block_name: str):
        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
        all_custom_blocks = cur.execute(
            f"SELECT BLOCK_NAME, STRUCTURE, IMAGE_PATH "
            f"FROM ALL_CUSTOM_BLOCKS").fetchall()
        size_blocks = pygame.Rect(0, 0, *BLOCK_SIZE_IN_BLOCK_LIST)

        base_blocklists, custom_blocklists = [], []
        for block in [InputBlock(self, size_blocks),
                      OutputBlock(self, size_blocks),
                      AndBlock(self, size_blocks),
                      OrBlock(self, size_blocks),
                      NotBlock(self, size_blocks)]:
            def cell_block_action(arg: CellInBlockList) -> Callable:
                def cmd():
                    make_copy_block(arg, self)()
                    self.update_input_output_ids()
                return cmd

            cell_block = CellInBlockList(block, lambda: None)
            cell_block.action = cell_block_action(cell_block)
            base_blocklists.append(cell_block)
        for custom_block in all_custom_blocks:
            custom_structure = cur.execute(
                f'SELECT STRUCTURE FROM ALL_CUSTOM_BLOCKS '
                f'WHERE BLOCK_NAME = "{custom_block[0]}"').fetchall()[0][0]
            if custom_block[0] == block_name or custom_block_in_structure(
                    custom_structure, block_name, cur):
                continue
            block = CustomBlock(custom_block[0], custom_block[1],
                                self, size_blocks, img=custom_block[2])
            cell_block = CellInBlockList(block, lambda: None)
            cell_block.action = make_copy_block(cell_block, self)
            custom_blocklists.append(cell_block)
        all_listblocks = base_blocklists + custom_blocklists

        super().__init__(all_listblocks)

        self.editing_block_name = block_name

        def save_pic_action():
            def dropped_action(path: str):
                con_now = sqlite3.connect(
                    './source_code/block_scheme/data/blocks.db')
                cur_now = con_now.cursor()

                now_img = cur_now.execute(f'SELECT IMAGE_PATH '
                                          f'FROM ALL_CUSTOM_BLOCKS '
                                          f'WHERE BLOCK_NAME = '
                                          f'"{self.editing_block_name}"').\
                    fetchall()
                if any(now_img) and any(now_img[0][0]):
                    os.remove(now_img[0][0])

                all_imgs = os.listdir(CUSTOM_BLOCK_IMAGES_PATH)
                randing = random.randint(0, 10 ** 10)
                new_path = f'{CUSTOM_BLOCK_IMAGES_PATH}/' \
                           f'{randing}{path[path.rindex("."):]}'
                while new_path in all_imgs:
                    randing = random.randint(0, 10 ** 10)
                    new_path = f'{CUSTOM_BLOCK_IMAGES_PATH}/' \
                               f'{randing}{path[path.rindex("."):]}'
                shutil.copy2(path, new_path)

                cur_now.execute(f'UPDATE ALL_CUSTOM_BLOCKS SET IMAGE_PATH = '
                                f'"{new_path}" WHERE BLOCK_NAME = '
                                f'"{self.editing_block_name}"')
                con_now.commit()
                con_now.close()

            args = ('Choose picture', 'Picture is saved',
                    global_vars.ACTIVE_SCREEN.get_rect(),
                    ['png', 'bmp', 'jpg', 'jpeg'],
                    dropped_action)
            self.message_window = DropFileWindow(*args)

        self.save_btn = PyButton(text='Save', font=pygame.font.Font(FONT_NAME, 25),
                                 color=TEXT_COLOR, rect=SAVE_BTN_RECT,
                                 action=self.save_action)
        self.save_pic_btn = PyButton(text='Load Picture',
                                     font=pygame.font.Font(FONT_NAME, 25),
                                     color=TEXT_COLOR, rect=SAVE_PIC_BTN_RECT,
                                     action=save_pic_action)
        self.back_btn = PyButton(text='Back', font=pygame.font.Font(FONT_NAME, 25),
                                 color=TEXT_COLOR, rect=BACK_BTN_RECT,
                                 action=to_main_menu_action)

        self.all_btns = [self.save_btn, self.back_btn, self.save_pic_btn]

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

    @mouse_down_check_message
    def mouse_down(self, mouse_button: int) -> None:
        super().mouse_down(mouse_button)

        if mouse_button == 3:
            self.update_input_output_ids()

    def save(self) -> None:
        def not_in_table_action(cur: sqlite3.Cursor, structure: str,
                                inputs: str):
            last_id = cur.execute(f"""SELECT MAX(ID) FROM ALL_CUSTOM_BLOCKS"""
                                  ).fetchall()[0][0]
            if last_id is None:
                last_id = 0
            last_id += 1
            cur.execute(f"""
            INSERT INTO ALL_CUSTOM_BLOCKS 
            VALUES({last_id},'{self.editing_block_name}','{structure}',
            '{inputs}','')""")

        if not any([isinstance(block, OutputBlock)
                    for block in self.all_blocks]):
            raise NoOutputBlockError

        super()._save('ALL_CUSTOM_BLOCKS', 'BLOCK_NAME',
                      self.editing_block_name, not_in_table_action)

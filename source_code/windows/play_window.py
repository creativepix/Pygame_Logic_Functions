import json
import pygame
import sqlite3
from typing import Dict
from source_code import global_vars
from source_code.block_scheme.blocks.and_block import AndBlock
from source_code.block_scheme.blocks.custom_block import CustomBlock
from source_code.block_scheme.blocks.input_block import InputBlock
from source_code.block_scheme.blocks.not_block import NotBlock
from source_code.block_scheme.blocks.or_block import OrBlock
from source_code.block_scheme.blocks.output_block import OutputBlock
from source_code.constants import BLOCK_MIN_SIZE, TEXT_COLOR, SAVE_BTN_RECT, \
    BACK_BTN_RECT
from source_code.ui.blocklist.cell_in_blocklist import CellInBlockList
from source_code.ui.blocklist.standard_cell_block_actions import \
    make_copy_block
from source_code.ui.button import PyButton
from source_code.windows.base_game_window import BaseGameWindow
from source_code.windows.base_window import mouse_down_check_message
from source_code.ui.message_window.message_window import MessageWindow


class PlayWindow(BaseGameWindow):
    def __init__(self, level_id: int):
        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
        level = cur.execute(
            f"SELECT ACCORDANCE, STRUCTURE "
            f"FROM ALL_LEVELS WHERE ID = {level_id}").fetchall()[0]
        all_custom_blocks = cur.execute(
            f"SELECT BLOCK_NAME, STRUCTURE, IMAGE_PATH "
            f"FROM ALL_CUSTOM_BLOCKS").fetchall()
        self.level_id = level_id

        def str_keys_accordance_to_tuple(dicti: Dict) -> Dict:
            new_dicti = dict()
            for key, value in dicti.items():
                key = key.strip(')').strip('(').replace(' ', '').split(',')
                new_dicti[tuple(key)] = value
            return new_dicti

        self.accordance: dict = \
            str_keys_accordance_to_tuple(json.loads(level[0]))
        self.input_count = len(list(self.accordance.keys())[0])
        self.output_count = len(list(self.accordance.values())[0])

        size_blocks = pygame.Rect(0, 0, *BLOCK_MIN_SIZE)

        base_blocklists, custom_blocklists = [], []
        for block in [AndBlock(self, size_blocks),
                      OrBlock(self, size_blocks),
                      NotBlock(self, size_blocks)]:
            cell_block = CellInBlockList(block, lambda: None)
            cell_block.action = make_copy_block(cell_block, self)
            base_blocklists.append(cell_block)
        for custom_block in all_custom_blocks:
            block = CustomBlock(custom_block[0], custom_block[1],
                                self, size_blocks, img=custom_block[2])
            cell_block = CellInBlockList(block, lambda: None)
            cell_block.action = make_copy_block(cell_block, self)
            custom_blocklists.append(cell_block)
        all_listblocks = (base_blocklists + custom_blocklists)

        super().__init__(all_listblocks)

        def back_action():
            from source_code.windows.main_menu_window import MainMenuWindow
            global_vars.ACTIVE_WINDOW = MainMenuWindow()

        def save_action():
            self.update_id_connections()
            try:
                self.save()
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

        loading = level[1]
        if loading is None or not any(loading):
            loading = []
            rect = pygame.Rect(
                SAVE_BTN_RECT.right, BLOCK_MIN_SIZE[1] * 2, *BLOCK_MIN_SIZE)
            for _ in range(self.input_count):
                loading.append(f'InputBlock(input,{rect},OutputConnection('
                               f'0,[],(50, 0)))')
                rect.x += BLOCK_MIN_SIZE[0]
            rect = pygame.Rect(SAVE_BTN_RECT.right, 0, *BLOCK_MIN_SIZE)
            for _ in range(self.output_count):
                loading.append(f'OutputBlock(output,{rect},InputConnection('
                               f'1,[],(50, 100)))')
                rect.x += BLOCK_MIN_SIZE[0]
            loading = '|'.join(loading)
        self.load(loading)
        con.close()

    @mouse_down_check_message
    def mouse_down(self, mouse_button: int) -> None:
        if mouse_button == 3:
            for block in self.all_blocks:
                if block.is_selected() and not isinstance(block, InputBlock) \
                        and not isinstance(block, OutputBlock):
                    block.delete()
            return
        else:
            super().mouse_down(mouse_button)

    def save(self) -> None:
        super()._save('ALL_LEVELS', 'ID', self.level_id, lambda: None)

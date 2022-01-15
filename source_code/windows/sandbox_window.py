import pygame
import sqlite3
from source_code import global_vars
from source_code.block_scheme.blocks.and_block import AndBlock
from source_code.block_scheme.blocks.custom_block import CustomBlock
from source_code.block_scheme.blocks.input_block import InputBlock
from source_code.block_scheme.blocks.not_block import NotBlock
from source_code.block_scheme.blocks.or_block import OrBlock
from source_code.block_scheme.blocks.output_block import OutputBlock
from source_code.constants import BLOCK_MIN_SIZE, TEXT_COLOR, SAVE_BTN_RECT, \
    BACK_BTN_RECT, SAVE_PIC_BTN_RECT
from source_code.ui.blocklist.cell_in_blocklist import CellInBlockList
from source_code.ui.blocklist.standard_cell_block_actions import \
    make_copy_block
from source_code.ui.button import PyButton
from source_code.ui.message_window.drop_file_window import DropFileWindow
from source_code.ui.message_window.message_window import MessageWindow
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

        def save_pic_action():
            def dropped_action(path: str):
                con_now = sqlite3.connect(
                    './source_code/block_scheme/data/blocks.db')
                cur_now = con_now.cursor()
                cur_now.execute(f'UPDATE ALL_CUSTOM_BLOCKS SET IMAGE_PATH = '
                                f'"{path}" WHERE BLOCK_NAME = '
                                f'"{self.editing_block_name}"')
                con_now.commit()
                con_now.close()

            args = ('Drop me picture', 'Picture is saved',
                    global_vars.ACTIVE_SCREEN.get_rect(),
                    ['png', 'bmp', 'jpg', 'jpeg'],
                    dropped_action)
            self.message_window = DropFileWindow(*args)

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
        self.save_pic_btn = PyButton(text='Load Picture',
                                     font=pygame.font.Font(None, 25),
                                     color=TEXT_COLOR, rect=SAVE_PIC_BTN_RECT,
                                     action=save_pic_action)
        self.back_btn = PyButton(text='Back', font=pygame.font.Font(None, 25),
                                 color=TEXT_COLOR, rect=BACK_BTN_RECT,
                                 action=back_action)

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

        super()._save('ALL_CUSTOM_BLOCKS', 'BLOCK_NAME',
                      self.editing_block_name, not_in_table_action)

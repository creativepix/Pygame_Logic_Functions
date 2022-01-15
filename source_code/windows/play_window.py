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
from source_code.block_scheme.data.structure_cmds import \
    get_cmd_line_from_structure, get_structure_from_blocks
from source_code.constants import BLOCK_MIN_SIZE, TEXT_COLOR, SAVE_BTN_RECT, \
    BACK_BTN_RECT, CHECK_SOLUTION_BTN_RECT, INPUTS_RESULT_TABLE_RECT, \
    NEEDED_OUTPUTS_RESULT_TABLE_RECT, OUTPUTS_RESULT_TABLE_RECT, \
    RESULT_TITLES_INDENT, RESULTS_FONT_SIZE, BLOCKS_NAME_COLOR, \
    SCORE_GAME_RECT, BEST_GAME_SCORE_RECT, SCORE_FONT_SIZE
from source_code.ui.blocklist.cell_in_blocklist import CellInBlockList
from source_code.ui.blocklist.standard_cell_block_actions import \
    make_copy_block
from source_code.ui.button import PyButton
from source_code.ui.list.cell_in_list import CellInList
from source_code.ui.list.list import PyList
from source_code.ui.table import PyTable
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

        def str_keys_accordance_to_tuple(dicti: Dict) -> Dict:
            new_dicti = dict()
            for key, value in dicti.items():
                key = key.strip(')').strip('(').replace(' ', '').split(',')
                new_dicti[tuple(key)] = value
            return new_dicti

        self.level_id = level_id
        self.accordance: dict = \
            str_keys_accordance_to_tuple(json.loads(level[0]))
        self.input_count = len(list(self.accordance.keys())[0])
        self.output_count = len(list(self.accordance.values())[0])

        max_score, best_score, last_score = cur.execute(
            f"SELECT MAX_SCORE, BEST_SCORE, LAST_SCORE "
            f"FROM ALL_LEVELS WHERE ID = {level_id}").fetchall()[0]
        self.best_score = best_score
        self.max_score = max_score
        self.last_score = last_score

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

        def check_solution_action():
            self.update_id_connections()
            structure, inputs = \
                get_structure_from_blocks(self.all_blocks)
            cmd_line = get_cmd_line_from_structure(structure)
            all_ans = dict()
            for inputs, outputs in self.accordance.items():
                now_cmd_line = cmd_line
                for i in range(len(inputs)):
                    now_cmd_line = now_cmd_line.replace(
                        f'input_blocks[{i}]', inputs[i])
                ans = [eval(line) for line in now_cmd_line.split('\n')]
                all_ans[inputs] = (list(map(str, outputs)),
                                   list(map(lambda x: str(int(x)), ans)))
            self.make_table_results(all_ans)
            score = len([ans for ans in all_ans.values() if ans[0] == ans[1]])
            score_value = int(self.max_score * score // len(self.accordance))
            if score_value == self.max_score and len(self.accordance) != score:
                score_value -= 1
            self.last_score = score_value
            if score_value >= self.best_score:
                self.best_score = score_value
                self.save_action()

        def back_action():
            from source_code.windows.main_menu_window import MainMenuWindow
            global_vars.ACTIVE_WINDOW = MainMenuWindow()

        self.save_btn = PyButton(text='Save', font=pygame.font.Font(None, 25),
                                 color=TEXT_COLOR, rect=SAVE_BTN_RECT,
                                 action=self.save_action)
        self.back_btn = PyButton(text='Back', font=pygame.font.Font(None, 25),
                                 color=TEXT_COLOR, rect=BACK_BTN_RECT,
                                 action=back_action)
        self.check_btn = PyButton(text='Check', color=TEXT_COLOR,
                                  font=pygame.font.Font(None, 25),
                                  rect=CHECK_SOLUTION_BTN_RECT,
                                  action=check_solution_action)

        self.all_btns = [self.save_btn, self.back_btn, self.check_btn]

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

        self.table_results = None
        self.make_table_results(
            {key: (list(map(str, value)), ['None'])
             for key, value in self.accordance.items()})

    def save_action(self):
        self.update_id_connections()
        try:
            self.save()
            txt = 'Successfully saved!'
        except RecursionError:
            txt = 'Cannot save. Cause is max recursion error.!'
        message_rect = pygame.Rect(
            0, 0, *global_vars.ACTIVE_SCREEN.get_size())
        self.message_window = MessageWindow(txt, message_rect)

    def make_table_results(self, results: Dict):
        # идёт распределение на правильные/неправильные для того, чтобы
        # в таблицу результатов сначала вывести плохие результаты
        font = pygame.font.Font(None, RESULTS_FONT_SIZE)

        wrong_results = {key: value for key, value in results.items()
                         if value[0] != value[1]}
        correct_results = {key: value for key, value in results.items()
                           if value[0] == value[1]}
        inputs_lists, needed_outputs_lists, outputs_lists = [], [], []
        for dicti_results in (wrong_results, correct_results):
            for inputs, (needed_outputs, outputs) in dicti_results.items():
                cell_size = (50, 25)
                inputs_lists.append(
                    CellInList(''.join(inputs), size=cell_size,
                               font=font))
                needed_outputs_lists.append(
                    CellInList(''.join(needed_outputs), size=cell_size,
                               font=font))
                outputs_lists.append(
                    CellInList(''.join(outputs), size=cell_size,
                               font=font))

        result_lists = [PyList(inputs_lists, INPUTS_RESULT_TABLE_RECT, 0),
                        PyList(needed_outputs_lists,
                               NEEDED_OUTPUTS_RESULT_TABLE_RECT, 0),
                        PyList(outputs_lists, OUTPUTS_RESULT_TABLE_RECT, 0)]
        self.table_results = PyTable(
            result_lists, ['    inputs', '  outputs', 'your outputs'],
            font, RESULT_TITLES_INDENT)

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

    def mouse_wheel(self, koof: int) -> None:
        if self.table_results.rect.collidepoint(pygame.mouse.get_pos()):
            self.table_results.mouse_wheel(koof)
        else:
            super().mouse_wheel(koof)

    def tick(self, screen: pygame.Surface) -> None:
        super().tick(screen)

        self.table_results.render(screen)

        font = pygame.font.Font(None, SCORE_FONT_SIZE)
        widget = font.render(
            f'Last score: {self.last_score} / {self.max_score}', True,
            BLOCKS_NAME_COLOR)
        screen.blit(widget, SCORE_GAME_RECT)
        widget = font.render(
            f'Best score: {self.best_score} / {self.max_score}', True,
            BLOCKS_NAME_COLOR)
        screen.blit(widget, BEST_GAME_SCORE_RECT)

        if self.message_window is not None:
            self.message_window.render(screen)

    def save(self) -> None:
        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
        cur.execute(f'UPDATE ALL_LEVELS '
                    f'SET BEST_SCORE = {self.best_score}, '
                    f'LAST_SCORE = {self.last_score} '
                    f'WHERE ID = {self.level_id}')
        super()._save('ALL_LEVELS', 'ID', self.level_id, lambda: None, cur)
        con.commit()
        con.close()

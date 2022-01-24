import json
import math
import pygame
import sqlite3
from typing import Dict, Tuple, Union, List
from source_code.block_scheme.blocks.and_block import AndBlock
from source_code.block_scheme.blocks.custom_block import CustomBlock
from source_code.block_scheme.blocks.input_block import InputBlock
from source_code.block_scheme.blocks.not_block import NotBlock
from source_code.block_scheme.blocks.or_block import OrBlock
from source_code.block_scheme.blocks.output_block import OutputBlock
from source_code.block_scheme.data.structure_cmds import \
    get_cmd_line_from_structure, get_structure_from_blocks
from source_code.constants import TEXT_COLOR, SAVE_BTN_RECT, \
    BACK_BTN_RECT, CHECK_SOLUTION_BTN_RECT, INPUTS_RESULT_TABLE_RECT, \
    NEEDED_OUTPUTS_RESULT_TABLE_RECT, OUTPUTS_RESULT_TABLE_RECT, \
    RESULT_TITLES_INDENT, RESULTS_FONT_SIZE, SCORE_GAME_RECT, \
    BEST_GAME_SCORE_RECT, SCORE_FONT_SIZE, RESULTS_MAX_SYMBOLS, RESULTS_WIDTH, \
    STARTING_LEFTTOP_BLOCKS_WITHOUT_STRUCTURE, BLOCK_SIZE_IN_BLOCK_LIST, \
    DESCRIPTION_BTN_RECT, FONT_NAME
from source_code.middlewares.screen_ration import get_current_rect_ration, \
    get_current_vertical_ration
from source_code.middlewares.splitting_line import split_line
from source_code.middlewares.window_transition_actions import \
    to_main_menu_action
from source_code.ui.blocklist.cell_in_blocklist import CellInBlockList
from source_code.ui.blocklist.standard_cell_block_actions import \
    make_copy_block
from source_code.ui.button import PyButton
from source_code.ui.list.cell_in_list import CellInList
from source_code.ui.list.list import PyList
from source_code.ui.table import PyTable
from source_code.windows.base_game_window import BaseGameWindow
from source_code.windows.base_window import mouse_down_check_message, \
    disable_if_message


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

        size_blocks = pygame.Rect(0, 0, *BLOCK_SIZE_IN_BLOCK_LIST)

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
        all_listblocks = base_blocklists + custom_blocklists

        super().__init__(all_listblocks)
        self.show_message('Initializing level...')

        self.save_btn = PyButton(text='Save', font=pygame.font.Font(FONT_NAME, 25),
                                 color=TEXT_COLOR, rect=SAVE_BTN_RECT,
                                 action=self.save_action)
        self.back_btn = PyButton(text='Back', font=pygame.font.Font(FONT_NAME, 25),
                                 color=TEXT_COLOR, rect=BACK_BTN_RECT,
                                 action=to_main_menu_action)
        self.check_btn = PyButton(text='Check', color=TEXT_COLOR,
                                  font=pygame.font.Font(FONT_NAME, 25),
                                  rect=CHECK_SOLUTION_BTN_RECT,
                                  action=self.check_solution_action)
        self.description_btn = PyButton(text='Description', color=TEXT_COLOR,
                                        font=pygame.font.Font(FONT_NAME, 25),
                                        rect=get_current_rect_ration(
                                            DESCRIPTION_BTN_RECT),
                                        action=self.show_description_action)

        self.all_btns = [self.save_btn, self.back_btn, self.check_btn,
                         self.description_btn]

        loading = level[1]
        if loading is None or not any(loading):
            loading = []
            rect = pygame.Rect(STARTING_LEFTTOP_BLOCKS_WITHOUT_STRUCTURE[0],
                               STARTING_LEFTTOP_BLOCKS_WITHOUT_STRUCTURE[1]
                               + BLOCK_SIZE_IN_BLOCK_LIST[1] * 2,
                               *BLOCK_SIZE_IN_BLOCK_LIST)
            for _ in range(self.input_count):
                loading.append(f'InputBlock(input,{rect},OutputConnection('
                               f'0,[],(50, 0)))')
                rect.x += BLOCK_SIZE_IN_BLOCK_LIST[0]
            rect = pygame.Rect(
                *STARTING_LEFTTOP_BLOCKS_WITHOUT_STRUCTURE,
                *BLOCK_SIZE_IN_BLOCK_LIST)
            for _ in range(self.output_count):
                loading.append(f'OutputBlock(output,{rect},InputConnection('
                               f'1,[],(50, 100)))')
                rect.x += BLOCK_SIZE_IN_BLOCK_LIST[0]
            loading = '|'.join(loading)
        self.load(loading)

        info = cur.execute(
            f"SELECT DESCRIPTION FROM ALL_LEVELS WHERE "
            f"ID = {level_id}").fetchall()[0]
        self.description = info[0]

        self.table_results = None
        self.make_table_results(
            {key: (list(map(str, value)), ['None'])
             for key, value in self.accordance.items()})

        self.hide_message()
        con.close()

    def get_score_from_test_answers(
            self, all_ans: Dict[Tuple[Union[str]],
                                Tuple[List[str], List[str]]]) -> int:
        score = len([ans for ans in all_ans.values() if ans[0] == ans[1]])
        score_value = int(self.max_score * score // len(self.accordance))
        if score_value == self.max_score and len(self.accordance) != score:
            score_value -= 1
        return score_value

    def get_all_test_answers(self) -> \
            Dict[Tuple[Union[str]], Tuple[List[str], List[str]]]:
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
        return all_ans

    def show_description_action(self):
        self.show_message(self.description)

    def check_solution_action(self):
        self.show_message('Checking solution...')

        all_ans = self.get_all_test_answers()
        score_value = self.get_score_from_test_answers(all_ans)
        self.make_table_results(all_ans)
        self.last_score = score_value
        if score_value >= self.best_score:
            self.best_score = score_value

        self.show_message(f'Your score: {self.last_score}/{self.max_score}')

        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
        cur.execute(f'UPDATE ALL_LEVELS '
                    f'SET BEST_SCORE = {self.best_score}, '
                    f'LAST_SCORE = {self.last_score} '
                    f'WHERE ID = {self.level_id}')
        con.commit()
        con.close()

    def make_table_results(self, results: Dict):
        font = pygame.font.Font(FONT_NAME, RESULTS_FONT_SIZE)
        max_rows = max(
            math.ceil(len(list(results.keys())[0]) / RESULTS_MAX_SYMBOLS),
            math.ceil(len(list(results.values())[0][0]) / RESULTS_MAX_SYMBOLS),
            math.ceil(len(list(results.values())[0][1]) / RESULTS_MAX_SYMBOLS))
        cell_size = (RESULTS_WIDTH, 20 * max_rows)

        # идёт распределение на правильные/неправильные для того, чтобы
        # в таблицу результатов сначала вывести плохие результаты
        wrong_results = {key: value for key, value in results.items()
                         if value[0] != value[1]}
        correct_results = {key: value for key, value in results.items()
                           if value[0] == value[1]}
        inputs_lists, needed_outputs_lists, outputs_lists = [], [], []
        for i, dicti_results in enumerate([wrong_results, correct_results]):
            for inputs, (needed_outputs, outputs) in dicti_results.items():
                txt = split_line(''.join(inputs), RESULTS_MAX_SYMBOLS)
                inputs_lists.append(
                    CellInList('\n'.join(txt), size=cell_size, font=font))
                txt = split_line(''.join(needed_outputs), RESULTS_MAX_SYMBOLS)
                needed_outputs_lists.append(
                    CellInList('\n'.join(txt), size=cell_size, font=font))
                txt = split_line(''.join(outputs), RESULTS_MAX_SYMBOLS)
                txt[0] = ('+' if i == 1 else '-') + txt[0]
                outputs_lists.append(
                    CellInList('\n'.join(txt), size=cell_size, font=font))

        inputs_rect = INPUTS_RESULT_TABLE_RECT.copy()
        needed_outputs_rect = NEEDED_OUTPUTS_RESULT_TABLE_RECT.copy()
        outputs_rect = OUTPUTS_RESULT_TABLE_RECT.copy()
        inputs_rect.h = get_current_vertical_ration(inputs_rect.h)
        needed_outputs_rect.h = get_current_vertical_ration(
            needed_outputs_rect.h)
        outputs_rect.h = get_current_vertical_ration(outputs_rect.h)

        result_lists = [PyList(inputs_lists, inputs_rect, 0,
                               color=(0, 0, 0, 0)),
                        PyList(needed_outputs_lists, needed_outputs_rect, 0,
                               color=(0, 0, 0, 0)),
                        PyList(outputs_lists, outputs_rect, 0,
                               color=(0, 0, 0, 0))]
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

    @disable_if_message
    def mouse_wheel(self, koof: int) -> None:
        if self.table_results.rect.collidepoint(pygame.mouse.get_pos()):
            self.table_results.mouse_wheel(koof)
        else:
            super().mouse_wheel(koof)

    def tick(self, screen: pygame.Surface) -> None:
        self.table_results.render(screen)

        font = pygame.font.Font(FONT_NAME, SCORE_FONT_SIZE)
        widget = font.render(
            f'Last score: {self.last_score} / {self.max_score}', True,
            TEXT_COLOR)
        screen.blit(widget, get_current_rect_ration(SCORE_GAME_RECT))
        widget = font.render(
            f'Best score: {self.best_score} / {self.max_score}', True,
            TEXT_COLOR)
        screen.blit(widget, get_current_rect_ration(BEST_GAME_SCORE_RECT))

        super().tick(screen)

    def save(self) -> None:
        super()._save('ALL_LEVELS', 'ID', self.level_id, lambda: None)

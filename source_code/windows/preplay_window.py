import pygame
import sqlite3
from source_code import global_vars
from source_code.middlewares.screen_ration import get_current_horizontal_ration
from source_code.middlewares.splitting_line import split_line
from source_code.ui.button import PyButton
from source_code.ui.table import PyTable
from source_code.ui.list.list import PyList
from source_code.global_vars import ACTIVE_SCREEN
from source_code.windows.play_window import PlayWindow
from source_code.ui.list.cell_in_list import CellInList
from source_code.constants import TEXT_COLOR, PREPLAY_LEVEL_HEIGHT, \
    BACK_BTN_RECT, PREPLAY_MAX_SYMBOLS_DESCRIPTION, PREPLAY_MAX_SYMBOLS_NAMES
from source_code.windows.base_window import BaseWindow, disable_if_message


# окно, в котором происходит выбор блока для редактирования в песочнице
class PreplayWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
        all_levels = cur.execute(
            f"SELECT ID, NAME, DESCRIPTION, BEST_SCORE, MAX_SCORE "
            f"FROM ALL_LEVELS WHERE ID > 0 ORDER BY ID").fetchall()

        names_cells, descriptions_cells, scores_cells, play_btns_cells = \
            [], [], [], []
        for level in all_levels:
            def load_level(level_id: int):
                def cmd():
                    global_vars.ACTIVE_WINDOW = PlayWindow(level_id)
                return cmd
            names_cells.append(CellInList(
                '\n'.join(
                    split_line(level[1],
                               PREPLAY_MAX_SYMBOLS_NAMES)),
                size=(get_current_horizontal_ration(215),
                      PREPLAY_LEVEL_HEIGHT)))
            descriptions_cells.append(CellInList(
                '\n'.join(
                    split_line(level[2], PREPLAY_MAX_SYMBOLS_DESCRIPTION)),
                size=(get_current_horizontal_ration(775),
                      PREPLAY_LEVEL_HEIGHT)))
            scores_cells.append(CellInList(
                f'{level[3]}/{level[4]}',
                size=(get_current_horizontal_ration(75),
                      PREPLAY_LEVEL_HEIGHT)))
            play_btns_cells.append(CellInList(
                f'Play', load_level(level[0]),
                size=(get_current_horizontal_ration(75),
                      PREPLAY_LEVEL_HEIGHT)))

        rect = pygame.Rect(get_current_horizontal_ration(10),
                           150, get_current_horizontal_ration(200),
                           ACTIVE_SCREEN.get_height() - 150)
        names = PyList(names_cells, rect, 0, (0, 0, 0, 0))
        rect = pygame.Rect(rect.x + rect.w, 150,
                           get_current_horizontal_ration(775),
                           ACTIVE_SCREEN.get_height() - 150)
        descriptions = PyList(descriptions_cells, rect, 0, (0, 0, 0, 0))
        rect = pygame.Rect(rect.x + rect.w, 150,
                           get_current_horizontal_ration(75),
                           ACTIVE_SCREEN.get_height() - 150)
        scores = PyList(scores_cells, rect, 0, (0, 0, 0, 0))
        rect = pygame.Rect(rect.x + rect.w + 30, 150,
                           get_current_horizontal_ration(75),
                           ACTIVE_SCREEN.get_height() - 150)
        play_btns = PyList(play_btns_cells, rect, 0, (0, 0, 0, 0))
        self.choose_level_table = PyTable(
            [names, descriptions, scores, play_btns])

        def back_action():
            from source_code.windows.main_menu_window import MainMenuWindow
            global_vars.ACTIVE_WINDOW = MainMenuWindow()

        self.back_btn = PyButton(text='Back', font=pygame.font.Font(None, 25),
                                 color=TEXT_COLOR, rect=BACK_BTN_RECT,
                                 action=back_action)
        self.all_btns.append(self.back_btn)

        con.close()

    def tick(self, screen: pygame.Surface) -> None:
        self.choose_level_table.render(screen)
        font = pygame.font.Font(None, 75)
        for i, line in enumerate(['Выберите уровень',
                                  'для прохождения'], start=1):
            widget = font.render(line, True, TEXT_COLOR)
            font_rect = widget.get_rect()
            font_rect.center = (self.choose_level_table.rect.centerx,
                                i * 50)
            screen.blit(widget, font_rect)
        super().tick(screen)

    @disable_if_message
    def mouse_wheel(self, koof: int) -> None:
        self.choose_level_table.mouse_wheel(koof)

    @disable_if_message
    def mouse_down(self, mouse_button: int) -> None:
        super().mouse_down(mouse_button)
        if mouse_button == 1:
            self.choose_level_table.mouse_down()

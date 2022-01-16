import pygame
import sqlite3
from source_code.middlewares.window_transition_actions import quit_action, \
    start_training_action, start_presandbox_action, start_preplay_action
from source_code.ui.button import PyButton
from source_code.constants import START_MENU_SIZE, TEXT_COLOR, \
    SCORE_FONT_SIZE, BLOCKS_NAME_COLOR, MAIN_MENU_SCORE_RECT
from source_code.windows.base_window import BaseWindow


class MainMenuWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
        sum_score = sum([score[0] for score in
                         cur.execute(f"SELECT BEST_SCORE FROM ALL_LEVELS "
                                     f"WHERE ID > 0").
                         fetchall()])
        max_score = sum([score[0] for score in
                         cur.execute(f"SELECT MAX_SCORE FROM ALL_LEVELS "
                                     f"WHERE ID > 0").
                         fetchall()])
        self.sum_score = sum_score
        self.max_score = max_score
        con.close()

    def tick(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        text_w, text_h = 200, 70
        otstyp = 150

        b1 = PyButton(text='Play', font=pygame.font.Font(None, 50),
                      color=TEXT_COLOR, rect=pygame.Rect(
                START_MENU_SIZE[0] // 2 - text_w // 2,
                START_MENU_SIZE[1] // 2 - text_h // 2 - otstyp // 1.35,
                text_w, text_h), action=start_preplay_action)
        b2 = PyButton(text='Sandbox', font=pygame.font.Font(None, 50),
                      color=TEXT_COLOR, rect=pygame.Rect(
                START_MENU_SIZE[0] // 2 - text_w // 2,
                START_MENU_SIZE[1] // 2 - text_h // 2 - otstyp // 4,
                text_w, text_h), action=start_presandbox_action)
        b3 = PyButton(text='Training', font=pygame.font.Font(None, 50),
                      color=TEXT_COLOR, rect=pygame.Rect(
                START_MENU_SIZE[0] // 2 - text_w // 2,
                START_MENU_SIZE[1] // 2 - text_h // 2 + otstyp // 4,
                text_w, text_h), action=start_training_action)
        b4 = PyButton(text='Exit', font=pygame.font.Font(None, 50),
                      color=TEXT_COLOR, rect=pygame.Rect(
                START_MENU_SIZE[0] // 2 - text_w // 2,
                START_MENU_SIZE[1] // 2 - text_h // 2 + otstyp // 1.35,
                text_w, text_h), action=quit_action)

        self.all_btns = [b1, b2, b3, b4]

        for btn in self.all_btns:
            btn.render(screen)

        font = pygame.font.Font(None, SCORE_FONT_SIZE)
        widget = font.render(f'Sum score: {self.sum_score} / {self.max_score}',
                             True, BLOCKS_NAME_COLOR)
        screen.blit(widget, pygame.Rect(MAIN_MENU_SCORE_RECT))

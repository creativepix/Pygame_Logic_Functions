import pygame
from source_code import global_vars
from source_code.constants import START_MENU_SIZE, TEXT_COLOR
from source_code.ui.button import PyButton
from source_code.windows.base_window import BaseWindow


class MainMenuWindow(BaseWindow):
    def tick(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        text_w, text_h = 200, 70
        otstyp = 100

        def start_game_action():
            pass

        def start_sandbox_action():
            from source_code.windows.presandbox_window import PresandboxWindow
            global_vars.ACTIVE_WINDOW = PresandboxWindow()

        def quit_action():
            global_vars.RUNNING = False
            pygame.quit()

        b1 = PyButton(text='Play', font=pygame.font.Font(None, 50),
                      color=TEXT_COLOR, rect=pygame.Rect(
                START_MENU_SIZE[0] // 2 - text_w // 2,
                START_MENU_SIZE[1] // 2 - text_h // 2 - otstyp,
                text_w, text_h), action=start_game_action)
        b2 = PyButton(text='Sandbox', font=pygame.font.Font(None, 50),
                      color=TEXT_COLOR, rect=pygame.Rect(
                START_MENU_SIZE[0] // 2 - text_w // 2,
                START_MENU_SIZE[1] // 2 - text_h // 2,
                text_w, text_h), action=start_sandbox_action)
        b3 = PyButton(text='Exit', font=pygame.font.Font(None, 50),
                      color=TEXT_COLOR, rect=pygame.Rect(
                START_MENU_SIZE[0] // 2 - text_w // 2,
                START_MENU_SIZE[1] // 2 - text_h // 2 + otstyp,
                text_w, text_h), action=quit_action)

        self.all_btns.clear()
        self.all_btns.append(b1)
        self.all_btns.append(b2)
        self.all_btns.append(b3)

        for btn in self.all_btns:
            btn.render(screen)

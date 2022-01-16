import pygame
from source_code import global_vars


def to_main_menu():
    from source_code.windows.main_menu_window import MainMenuWindow
    global_vars.ACTIVE_WINDOW = MainMenuWindow()


def start_preplay_action():
    from source_code.windows.preplay_window import PreplayWindow
    global_vars.ACTIVE_WINDOW = PreplayWindow()


def start_presandbox_action():
    from source_code.windows.presandbox_window import PresandboxWindow
    global_vars.ACTIVE_WINDOW = PresandboxWindow()


def start_training_action():
    from source_code.windows.training_window import TrainingWindow
    global_vars.ACTIVE_WINDOW = TrainingWindow()


def quit_action():
    global_vars.RUNNING = False
    pygame.quit()

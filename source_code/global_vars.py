import pygame_gui
from pygame.surface import Surface
from source_code.windows.base_window import BaseWindow


ACTIVE_SCREEN: Surface = None
ACTIVE_WINDOW: BaseWindow = None
UI_MANAGER: pygame_gui.UIManager = None
RUNNING = True

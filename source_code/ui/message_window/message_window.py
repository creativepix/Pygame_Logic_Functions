import pygame
from source_code import global_vars
from source_code.py_base import PyObjectBase
from source_code.constants import MESSAGE_WINDOW_TEXT_COLOR


class MessageWindow(PyObjectBase):
    """Что-то наподобии диалогового окна"""
    def __init__(self, text: str, rect: pygame.Rect):
        self.text = text
        self.rect = rect
        self.is_rendered = False

        global_vars.ACTIVE_WINDOW.mouse_up()

    def render(self, screen: pygame.Surface) -> None:
        surf = pygame.Surface(screen.get_size())
        surf.fill((255, 255, 255))
        surf.set_alpha(50)
        screen.blit(surf, self.rect)

        widget = pygame.font.Font(None, 50).render(
            self.text, True, MESSAGE_WINDOW_TEXT_COLOR)
        font_rect = widget.get_rect()
        font_rect.center = self.rect.center
        screen.blit(widget, font_rect)

        self.is_rendered = True

    def mouse_down(self) -> None:
        if self.is_rendered and self.rect.collidepoint(pygame.mouse.get_pos()):
            global_vars.ACTIVE_WINDOW.hide_message()

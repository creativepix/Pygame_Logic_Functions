import pygame
from source_code import global_vars
from source_code.middlewares.splitting_line import split_line
from source_code.py_base import PyObjectBase
from source_code.constants import MESSAGE_WINDOW_TEXT_COLOR, \
    MESSAGE_WINDOW_TEXT_LINES_INDENT, MESSAGE_WINDOW_TEXT_MAX_SYMBOLS, \
    MESSAGE_WINDOW_ALPHA, FONT_NAME


class MessageWindow(PyObjectBase):
    """UI: Диалоговое окно с всплывающим текстом"""
    def __init__(self, text: str, rect: pygame.Rect):
        self.text_lines = split_line(text, MESSAGE_WINDOW_TEXT_MAX_SYMBOLS)
        self.rect = rect
        self.is_rendered = False

        global_vars.ACTIVE_WINDOW.mouse_up()

    def render(self, screen: pygame.Surface) -> None:
        surf = pygame.Surface(screen.get_size())
        surf.fill((255, 255, 255))
        surf.set_alpha(MESSAGE_WINDOW_ALPHA)
        screen.blit(surf, self.rect)

        if len(self.text_lines) > 1:
            if len(self.text_lines) % 2 == 0:
                plus = MESSAGE_WINDOW_TEXT_LINES_INDENT // 2
            else:
                plus = 0
            r = range(-MESSAGE_WINDOW_TEXT_LINES_INDENT *
                      (len(self.text_lines) // 2) + plus,
                      MESSAGE_WINDOW_TEXT_LINES_INDENT *
                      (len(self.text_lines) // 2),
                      MESSAGE_WINDOW_TEXT_LINES_INDENT)
            indents = list(r)
            if len(self.text_lines) % 2 != 0:
                indents.append(indents[-1] + MESSAGE_WINDOW_TEXT_LINES_INDENT)
        else:
            indents = [0]
        for i, line in enumerate(self.text_lines):
            widget = pygame.font.Font(FONT_NAME, 50).render(
                line, True, MESSAGE_WINDOW_TEXT_COLOR)
            font_rect = widget.get_rect()
            font_rect.center = self.rect.center
            font_rect.centery += indents[i]
            screen.blit(widget, font_rect)

        self.is_rendered = True

    def mouse_down(self) -> None:
        if self.is_rendered and self.rect.collidepoint(pygame.mouse.get_pos()):
            global_vars.ACTIVE_WINDOW.hide_message()

    @property
    def text(self) -> str:
        return '\n'.join(self.text_lines)

    @text.setter
    def text(self, value):
        self.text_lines = split_line(value, MESSAGE_WINDOW_TEXT_MAX_SYMBOLS)

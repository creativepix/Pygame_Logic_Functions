import string
from typing import Callable

import pygame

from source_code.py_base import PyObjectBase


class PyInputField(PyObjectBase):
    def __init__(self, font: pygame.font.Font, color: pygame.Color,
                 rect: pygame.Rect, enter_action: Callable[[str], None],
                 max_symbols: int, started_text: str = ''):
        self.font = font
        self.text = started_text
        self.color = color
        self.rect = rect
        self.enter_action = enter_action
        self.max_symbols = max_symbols

    def key_down(self, key: int) -> None:
        if key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
            self.enter_action(self.text)
        elif key == pygame.K_BACKSPACE:
            if any(self.text):
                self.text = self.text[:-1]

    def text_input(self, text: str) -> None:
        if text in string.ascii_letters + string.digits:
            if len(self.text) + 1 <= self.max_symbols:
                self.text += text

    def render(self, screen: pygame.Surface) -> None:
        widget = self.font.render(self.text, True, self.color)
        font_rect = widget.get_rect()
        font_rect.center = self.rect.center
        screen.blit(widget, font_rect)

    def __call__(self, *args, **kwargs):
        return self.text

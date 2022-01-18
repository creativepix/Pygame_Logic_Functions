import pygame
from typing import Callable
from source_code.py_base import PyObjectBase
from source_code.constants import BLOCKS_WIDTH, BUTTON_RECT_COLOR


# Такие классы хранятся в BaseWindow`ах в списке all_bts
class PyButton(PyObjectBase):
    """UI: Кнопка"""
    def __init__(self, text: str, font: pygame.font.Font, color: pygame.Color,
                 rect: pygame.Rect, action: Callable):
        self.text = text
        self.font = font
        self.color = color
        self.rect = rect
        self.action = action

    def mouse_down(self) -> None:
        if self.is_clicked():
            self.click()

    def is_clicked(self) -> bool:
        return self.rect.collidepoint(*pygame.mouse.get_pos())

    def click(self) -> None:
        self.action()

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, BUTTON_RECT_COLOR, self.rect,
                         width=BLOCKS_WIDTH)
        widget = self.font.render(self.text, True, self.color)
        font_rect = widget.get_rect()
        font_rect.center = self.rect.center
        screen.blit(widget, font_rect)

import math
import pygame
from typing import List, Callable, Union
from source_code.ui.list.list import PyList
from source_code.py_base import PyObjectBase
from source_code.constants import BLOCKS_NAME_COLOR
from source_code.errors.table_error import TableError


class PyTable(PyObjectBase):
    def __init__(self, pylists: List[PyList],
                 titles: Union[List[str], Callable[[], str]] = None,
                 title_font: pygame.font.Font = None, indent: int = 0):
        if titles is None:
            self.titles = []
        else:
            self.titles = titles
            if title_font is None or len(self.titles) != len(pylists):
                raise TableError
        self.title_font = title_font
        self.indent = indent

        self.orientation = pylists[0].orientation

        rect = [math.inf, math.inf, -math.inf, -math.inf]
        for pylist in pylists:
            if pylist.orientation != self.orientation:
                raise TableError

            if pylist.rect.x < rect[0]:
                rect[0] = pylist.rect.x
            if pylist.rect.y < rect[1]:
                rect[1] = pylist.rect.y
            if pylist.rect.x + pylist.rect.w > rect[2]:
                rect[2] = pylist.rect.x + pylist.rect.w
            if pylist.rect.y + pylist.rect.h > rect[3]:
                rect[3] = pylist.rect.y + pylist.rect.h

        self.rect = pygame.Rect(
            *(rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]))
        self.pylists = pylists

    def mouse_down(self) -> None:
        for pylist in self.pylists:
            pylist.mouse_down()

    def mouse_wheel(self, koof: int) -> None:
        for pylist in self.pylists:
            pylist.scroll(koof)

    def render(self, screen: pygame.Surface) -> None:
        for i, pylist in enumerate(self.pylists):
            pylist.render(screen)
            if any(self.titles):
                widget = self.title_font.render(
                    self.titles[i] if isinstance(self.titles[i], str) else
                    self.titles[i], True, BLOCKS_NAME_COLOR)
                font_rect = widget.get_rect()
                if self.orientation == 0:
                    font_rect.y = pylist.rect.y - self.indent
                    font_rect.x = pylist.cells[0].rect.x
                else:
                    font_rect.x = pylist.rect.x - self.indent
                    font_rect.y = pylist.cells[0].rect.y
                screen.blit(widget, font_rect)

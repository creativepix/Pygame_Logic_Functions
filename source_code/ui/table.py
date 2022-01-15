import math
import pygame
from typing import List
from source_code.errors.table_error import TableError
from source_code.py_base import PyObjectBase
from source_code.ui.list.list import PyList


class PyTable(PyObjectBase):
    def __init__(self, pylists: List[PyList]):
        if not any(pylists):
            raise TableError
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
        for pylist in self.pylists:
            pylist.render(screen)

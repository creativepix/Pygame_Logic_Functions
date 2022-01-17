import pygame
from typing import Tuple, Union, List
from source_code.py_base import PyObjectBase
from source_code.ui.list.cell_in_list import CellInList
from source_code.constants import SPACE_BLOCKS_IN_BLOCK_LIST


# Горизонтальность нетестирована, поэтому с ней могут быть проблемы
class PyList(PyObjectBase):
    """Ui-список"""
    def __init__(self, cells: List[CellInList],
                 rect: pygame.Rect,
                 orientation: int,
                 color: Union[Union[Tuple[int, int, int],
                                    Tuple[int, int, int, int]],
                              pygame.Color] = None):
        """orientation - 0 = vertical, 1 = horizontal"""
        if color is None:
            color = (15, 15, 15)
        self.color = color
        self.local_var = 10
        self.orientation = orientation
        self.rect: pygame.Rect = rect

        self._cells = cells
        # len_cells нужна для оптимизации, чтобы python в методе tick постоянно
        # не просчитывал длину self.cells
        self.len_cells = len(self.cells)

    def scroll(self, koof: int) -> None:
        self.local_var += koof * 10  # Заменил -= на +=: скроллить надо в противоположную сторону

    def mouse_down(self) -> None:
        for cell in self.cells:
            if cell.rect.collidepoint(pygame.mouse.get_pos()):
                cell.do_action()

    def mouse_wheel(self, koof: int) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.scroll(koof)

    def render(self, screen: pygame.Surface) -> None:
        surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        surf.fill(self.color)
        screen.blit(surf, self.rect.topleft)

        starting_koof = (-self.local_var) // \
                        (SPACE_BLOCKS_IN_BLOCK_LIST + self.cells[0].size[1])
        ending_koof = (self.rect.bottom - self.rect.y - self.local_var) // \
                      (SPACE_BLOCKS_IN_BLOCK_LIST + self.cells[0].size[1]) + 1
        if starting_koof < 0:
            starting_koof = 0
        if ending_koof > self.len_cells:
            ending_koof = self.len_cells
        if ending_koof < 0:
            ending_koof = 1

        for koof, cell in enumerate(self.cells[starting_koof:ending_koof],
                                    start=starting_koof):
            cell.render(screen, self.rect, koof, self.local_var,
                        self.orientation)

    @property
    def cells(self) -> List[CellInList]:
        return self._cells

    @cells.setter
    def cells(self, value):
        self._cells = value
        self.len_cells = len(self._cells)

import pygame
from typing import Callable, Union, Tuple
from source_code.constants import BLOCKS_WIDTH, SPACE_BLOCKS_IN_BLOCK_LIST, \
    BASE_CELL_IN_BLOCK_SIZE, TEXT_COLOR, LIST_CELLS_COLOR


class CellInList:
    """Ячейка в списке"""
    def __init__(self, text: Union[str, Callable[[], str]],
                 action: Callable = lambda: None, size: Tuple[int, int] = None,
                 font: pygame.font.Font = pygame.font.Font(None, 20),
                 img: Union[pygame.Surface, str] = None,
                 text_color: Tuple[int, int, int] = TEXT_COLOR):
        if size is not None:
            self.size = size
        else:
            self.size = BASE_CELL_IN_BLOCK_SIZE
        if isinstance(img, str):
            self.img = pygame.image.load(img) if any(img) else None
        else:
            self.img = img
        if isinstance(self.img, pygame.Surface):
            self.img = pygame.transform.smoothscale(self.img, self.size)
        self.text = text
        self.action = action
        self.rect = pygame.Rect(0, 0, *self.size)
        self.font = font
        self.text_color = text_color

    def do_action(self):
        self.action()

    def update_rect(self, block_list_rect: pygame.Rect,
                    koof: int, block_list_local_var: int, orientation: int):
        if orientation == 0:
            self.rect = pygame.Rect(block_list_rect.centerx -
                                    self.size[0] // 2,
                                    block_list_rect.y + block_list_local_var +
                                    (SPACE_BLOCKS_IN_BLOCK_LIST +
                                     self.size[1]) * koof,
                                    *self.size)
        else:
            self.rect = pygame.Rect(block_list_rect.x + block_list_local_var +
                                    (self.size[0] +
                                     SPACE_BLOCKS_IN_BLOCK_LIST) * koof,
                                    block_list_rect.centery -
                                    self.size[1] // 2,
                                    *self.size)

    def render(self, screen: pygame.Surface, block_list_rect: pygame.Rect,
               koof: int, block_list_local_var: int, orientation: int) -> None:
        """orientation - 0 = vertical, 1 = horizontal"""
        self.update_rect(
            block_list_rect, koof, block_list_local_var, orientation)

        if orientation == 0:
            if self.rect.bottom < block_list_rect.top or \
                    self.rect.top > block_list_rect.bottom:
                return
        else:
            if self.rect.right < block_list_rect.left or \
                    self.rect.left > block_list_rect.right:
                return

        cropping = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        surf = pygame.Surface(self.rect.size)
        if self.img is None:
            if isinstance(self.text, str) and '\n' in self.text:
                widgets = []
                for line in self.text.split('\n'):
                    widgets.append(
                        self.font.render(line, True, self.text_color).copy())
            else:
                widgets = [self.font.render(
                    self.text if isinstance(self.text, str) else
                    self.text(), True, self.text_color)]
            rect = self.rect.copy()
            y_indent = 0
            for widget in widgets:
                font_rect = widget.get_rect()
                if len(widgets) > 1:
                    font_rect.center = (rect.w // 2, font_rect.h)
                else:
                    font_rect.center = (rect.w // 2, rect.h // 2)
                font_rect.y += y_indent
                surf.blit(widget, font_rect)
                y_indent += font_rect.h
            pygame.draw.rect(
                surf, LIST_CELLS_COLOR, (0, 0, rect.w, rect.h),
                width=BLOCKS_WIDTH)
        else:
            surf = self.img

        if orientation == 0:
            if self.rect.y < block_list_rect.y:
                cropping.y = -(self.rect.y - block_list_rect.y)
                cropping.h = self.rect.h - cropping.y
            elif self.rect.bottom > block_list_rect.bottom:
                cropping.h = (self.rect.h -
                              (self.rect.bottom - block_list_rect.bottom))
            screen.blit(surf, (self.rect.x, self.rect.y + cropping.y),
                        cropping)
        else:
            if self.rect.x < block_list_rect.x:
                cropping.x = -(self.rect.x - block_list_rect.x)
                cropping.w = self.rect.w - cropping.x
            elif self.rect.right > block_list_rect.right:
                cropping.w = (self.rect.w -
                              (self.rect.right - block_list_rect.right))
            screen.blit(surf, (self.rect.x + cropping.x, self.rect), cropping)

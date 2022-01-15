import pygame
from typing import Callable, Union, Tuple
from source_code.constants import BLOCKS_WIDTH, BLOCKS_NAME_COLOR, \
    BLOCKS_COLOR, SPACE_BLOCKS_IN_BLOCK_LIST, BASE_CELL_IN_BLOCK_SIZE


class CellInList:
    """Ячейка в списке"""
    def __init__(self, text: Union[str, Callable[[], str]],
                 action: Callable = lambda: None, size: Tuple[int, int] = None,
                 font: pygame.font.Font = pygame.font.Font(None, 20),
                 img: Union[pygame.Surface, str] = None):
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

    def do_action(self):
        self.action()

    def render(self, screen: pygame.Surface, block_list_rect: pygame.Rect,
               koof: int, block_list_local_var: int, orientation: int) -> None:
        """orientation - 0 = vertical, 1 = horizontal"""
        cropping = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        surf = pygame.Surface(self.rect.size)
        if self.img is None:
            widget = self.font.render(
                self.text if isinstance(self.text, str) else
                self.text(), True, BLOCKS_NAME_COLOR)
            font_rect = widget.get_rect()
            font_rect.center = (self.rect.w // 2, self.rect.h // 2)
            surf.blit(widget, font_rect)
            pygame.draw.rect(
                surf, BLOCKS_COLOR, (0, 0, self.rect.w, self.rect.h),
                width=BLOCKS_WIDTH)
        else:
            surf = self.img
        if orientation == 0:
            self.rect = pygame.Rect(block_list_rect.centerx -
                                    self.size[0] // 2,
                                    block_list_rect.y + block_list_local_var +
                                    (SPACE_BLOCKS_IN_BLOCK_LIST +
                                     self.size[1]) * koof,
                                    *self.size)
            if self.rect.y < -self.size[1]:
                return
            if self.rect.y < block_list_rect.y:
                cropping.y = -(self.rect.y - block_list_rect.y)
                cropping.h = self.rect.h - cropping.y
            elif self.rect.bottom > block_list_rect.bottom:
                cropping.h = (self.rect.h -
                              (self.rect.bottom - block_list_rect.bottom))
            screen.blit(surf, (self.rect.x, self.rect.y + cropping.y),
                        cropping)
        else:
            self.rect = pygame.Rect(block_list_rect.x + block_list_local_var +
                                    (self.size[0] +
                                     SPACE_BLOCKS_IN_BLOCK_LIST) * koof,
                                    block_list_rect.centery -
                                    self.size[1] // 2,
                                    *self.size)
            if self.rect.x < -self.size[0]:
                return
            if self.rect.x < block_list_rect.x:
                cropping.x = -(self.rect.x - block_list_rect.x)
                cropping.w = self.rect.w - cropping.x
            elif self.rect.right > block_list_rect.right:
                cropping.w = (self.rect.w -
                              (self.rect.right - block_list_rect.right))
            screen.blit(surf, (self.rect.x + cropping.x, self.rect), cropping)

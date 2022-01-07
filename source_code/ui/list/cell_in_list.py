from typing import Callable, Union, Tuple

import pygame
from source_code.block_scheme.blocks.base_block import BaseBlock
from source_code.constants import BLOCKS_WIDTH, BLOCKS_NAME_COLOR, \
    BLOCK_MIN_SIZE, BLOCKS_COLOR, SPACE_BLOCKS_IN_BLOCK_LIST, BACKGROUND_COLOR, \
    BASE_CELL_IN_BLOCK_SIZE


class CellInList:
    def __init__(self, text: Union[str, Callable[[], str]],
                 action: Callable, size: Tuple[int, int] = None,
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

    def do_action(self):
        self.action()

    def render(self, screen: pygame.Surface, block_list_rect: pygame.Rect,
               koof: int, block_list_local_var: int, orientation: int) -> None:
        """orientation - 0 = vertical, 1 = horizontal"""
        if orientation == 0:
            self.rect = pygame.Rect(block_list_rect.centerx -
                                    self.size[0] // 2,
                                    block_list_rect.y + block_list_local_var +
                                    (SPACE_BLOCKS_IN_BLOCK_LIST +
                                     self.size[1]) * koof,
                                    *self.size)
            if self.rect.y < -self.size[1]:
                return
            surf = pygame.Surface(self.rect.size)
            pygame.draw.rect(
                surf, BLOCKS_COLOR, (0, 0, self.rect.w, self.rect.h),
                width=BLOCKS_WIDTH)

            if self.img is None:
                font = pygame.font.Font(None, 20)
                widget = font.render(self.text if isinstance(self.text, str)
                                     else self.text(), True, BLOCKS_NAME_COLOR)
                font_rect = widget.get_rect()
                font_rect.center = (self.rect.w // 2, self.rect.h // 2)
                surf.blit(widget, font_rect)
                if self.rect.y < block_list_rect.y:
                    second_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
                    second_rect.height = -(self.rect.y - block_list_rect.y)
                    pygame.draw.rect(surf, (0, 0, 0, 0), second_rect)
                if self.rect.y + self.rect.h > block_list_rect.y + \
                        block_list_rect.h:
                    dif = (self.rect.y + self.rect.h) - \
                          (block_list_rect.y + block_list_rect.h)
                    second_rect = pygame.Rect(0, self.rect.h - dif,
                                              self.rect.w, self.rect.h)
                    second_rect.height = dif
                    pygame.draw.rect(surf, (0, 0, 0, 0), second_rect)
                screen.blit(surf, self.rect)
            else:
                screen.blit(self.img, self.rect)
        else:
            self.rect = pygame.Rect(block_list_rect.x + block_list_local_var +
                                    (self.size[0] +
                                     SPACE_BLOCKS_IN_BLOCK_LIST) * koof,
                                    block_list_rect.centery -
                                    self.size[1] // 2,
                                    *self.size)
            if self.rect.x < -self.size[0]:
                return
            surf = pygame.Surface(self.rect.size)
            pygame.draw.rect(
                surf, BLOCKS_COLOR, (0, 0, self.rect.w, self.rect.h),
                width=BLOCKS_WIDTH)

            if self.img is None:
                font = pygame.font.Font(None, 20)
                widget = font.render(self.text if isinstance(self.text, str) else
                                     self.text(), True, BLOCKS_NAME_COLOR)
                font_rect = widget.get_rect()
                font_rect.center = (self.rect.w // 2, self.rect.h // 2)
                surf.blit(widget, font_rect)
                if self.rect.x < block_list_rect.x:
                    second_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
                    second_rect.width = -(self.rect.x - block_list_rect.x)
                    pygame.draw.rect(surf, (0, 0, 0, 0), second_rect)
                if self.rect.x + self.rect.w > \
                        block_list_rect.x + block_list_rect.w:
                    dif = (self.rect.x + self.rect.w) - \
                          (block_list_rect.x + block_list_rect.w)
                    second_rect = pygame.Rect(self.rect.w - dif, 0,
                                              self.rect.w, self.rect.h)
                    second_rect.width = dif
                    pygame.draw.rect(surf, (0, 0, 0, 0), second_rect)
                screen.blit(surf, self.rect)
            else:
                screen.blit(self.img, self.rect)

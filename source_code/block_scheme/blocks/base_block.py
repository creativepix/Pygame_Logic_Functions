from typing import List
import pygame
from source_code.block_scheme.blocks.builder_base_block import BuilderBaseBlock
from source_code.block_scheme.connections.base_connection import BaseConnection
from source_code.constants import BLOCKS_COLOR, BLOCKS_NAME_COLOR, \
    BLOCKS_INDENT_FOR_RESIZING, BLOCKS_WIDTH, BLOCK_MIN_SIZE
from source_code.windows.base_game_window import BaseGameWindow


class BaseBlock(BuilderBaseBlock):
    def __init__(self, base_game_window: BaseGameWindow,
                 name: str, rect: pygame.rect.Rect,
                 inputs: List[BaseConnection],
                 outputs: List[BaseConnection], img_path: str = None):
        super().__init__(base_game_window, name, rect, inputs, outputs,
                         img_path)

    def zoom(self, koof: int) -> None:
        last_center = self.rect.center
        self.resize(koof * 2, koof * 2)
        self.rect.center = last_center
        self.last_pos = self.rect.x, self.rect.y

    def move(self, x_dif: int, y_dif: int) -> None:
        self.rect = self.rect.move(x_dif, y_dif)

    def is_selected(self) -> bool:
        return self.rect.collidepoint(*pygame.mouse.get_pos())

    def resize(self, w_dif: int, h_dif: int) -> None:
        if self.rect.w + w_dif >= BLOCK_MIN_SIZE[0] or w_dif >= 0:
            self.rect.w = max(BLOCK_MIN_SIZE[0], self.rect.w + w_dif)
        if self.rect.h >= BLOCK_MIN_SIZE[1] or h_dif >= 0:
            self.rect.h = max(BLOCK_MIN_SIZE[1], self.rect.h + h_dif)

    def render(self, screen: pygame.Surface) -> None:
        if self.img is None:
            pygame.draw.rect(screen, BLOCKS_COLOR, self.rect,
                             width=BLOCKS_WIDTH)

            font = pygame.font.Font(None, 20)
            widget = font.render(self.name, True, BLOCKS_NAME_COLOR)
            font_rect = widget.get_rect()
            font_rect.center = self.rect.center
            screen.blit(widget, font_rect)
        else:

            img = pygame.transform.scale(self.img, self.rect.size)
            screen.blit(img, self.rect.topleft)

            top_left = pygame.Rect(*self.rect.topleft, 10, 10)
            pygame.draw.rect(screen, BLOCKS_COLOR, top_left)
            top_right = pygame.Rect(self.rect.topright[0] - 10,
                                    self.rect.topright[1], 10, 10)
            pygame.draw.rect(screen, BLOCKS_COLOR, top_right)
            bottom_left = pygame.Rect(self.rect.bottomleft[0],
                                      self.rect.bottomleft[1] - 10, 10, 10)
            pygame.draw.rect(screen, BLOCKS_COLOR, bottom_left)
            bottom_right = pygame.Rect(self.rect.bottomright[0] - 10,
                                       self.rect.bottomright[1] - 10, 10, 10)
            pygame.draw.rect(screen, BLOCKS_COLOR, bottom_right)

        for connection in self.inputs + self.outputs:
            connection.render(screen)

    def mouse_down(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        for connection in self.inputs + self.outputs:
            connection.mouse_down()

        if self.connection_editing is None and self.is_selected():
            res_ind = BLOCKS_INDENT_FOR_RESIZING
            usl1 = self.rect.top <= mouse_pos[1] <= self.rect.top + res_ind
            usl2 = (self.rect.bottom >= mouse_pos[1] >= self.rect.bottom -
                    res_ind)
            usl3 = self.rect.left <= mouse_pos[0] <= self.rect.left + res_ind
            usl4 = self.rect.right <= mouse_pos[0] >= self.rect.right - res_ind
            if usl1 or usl2 or usl3 or usl4:
                self.is_resizing = True
            else:
                self.is_dragging = True
            self.last_mouse_pos = mouse_pos

    def mouse_motion(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        if self.connection_editing is not None:
            return

        action = None
        if self.is_dragging:
            action = self.move
        elif self.is_resizing:
            action = self.resize
        if self.is_dragging or self.is_resizing:
            # использую замысловатые методы вместо pygame.mouse.get_rel(),
            # потому что этот метод при первом значении выдаёт всё неправильное
            action(mouse_pos[0] - self.last_mouse_pos[0],
                   mouse_pos[1] - self.last_mouse_pos[1])
            self.last_mouse_pos = mouse_pos

    def mouse_up(self) -> None:
        for connection in self.inputs + self.outputs:
            connection.mouse_up()

        if self.connection_editing is not None:
            return

        self.is_resizing = False
        self.is_dragging = False
        self.last_mouse_pos = None

        for collide_rect in self.base_game_window.all_blocks:
            if self.rect is not collide_rect.rect and \
                    self.rect.colliderect(collide_rect.rect):
                self.rect.x = self.last_pos[0]
                self.rect.y = self.last_pos[1]
                return
        self.last_pos = self.rect.x, self.rect.y

    def delete(self) -> None:
        for connection in self.inputs + self.outputs:
            for attached_connection in connection.attached_connections:
                connection.detach(attached_connection)
        del self.base_game_window.all_blocks[
            self.base_game_window.all_blocks.index(self)]

    def copy(self):
        return self.__copy__()

    def __str__(self):
        return self.__repr__()

    def __repr__(self, header: str = 'BaseBlock'):
        ans = f'{header}({self.name},{self.rect}'
        for connection in self.inputs + self.outputs:
            ans += f',{connection}'
        return ans + ')'

    def __copy__(self):
        new_block = BaseBlock(self.base_game_window, self.name, self.rect,
                              [input_.copy() for input_ in self.inputs],
                              [output_.copy() for output_ in self.outputs])
        for connection in new_block.inputs + new_block.outputs:
            connection.parent_block = new_block
        return new_block

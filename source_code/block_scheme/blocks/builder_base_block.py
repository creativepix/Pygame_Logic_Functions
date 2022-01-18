import math
import pygame
from abc import abstractmethod
from source_code.py_base import PyObjectBase
from source_code.constants import BLOCK_MIN_SIZE
from source_code.middlewares.load_image import load_image


class BuilderBaseBlock(PyObjectBase, pygame.sprite.Sprite):
    def __init__(self, base_game_window, name, rect, signal_action, inputs,
                 outputs, img):
        super().__init__()
        self.base_game_window = base_game_window
        self.name = name
        self.rect = rect
        self.signal_action = signal_action
        self.inputs = inputs
        self.outputs = outputs
        if isinstance(img, str):
            if any(img):
                self.img = load_image(img)
            else:
                self.img = None
        else:
            self.img = img

        self.connection_editing = None
        self.is_dragging = False
        self.is_resizing = False
        self.last_mouse_pos = None
        self.last_rect = self.rect.copy()
        self.size_koof = int(math.log(self.rect.w // BLOCK_MIN_SIZE[0], 2))

    @abstractmethod
    def zoom(self, koof: int) -> None:
        pass

    @abstractmethod
    def move(self, x_dif: int, y_dif: int) -> None:
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        pass

    @abstractmethod
    def resize(self, w_dif: int, h_dif: int) -> None:
        pass

    @abstractmethod
    def is_selected(self) -> bool:
        """Наведена ли мышка на блок"""
        pass

    @abstractmethod
    def delete(self) -> None:
        pass

    @abstractmethod
    def update_output_signals(self):
        """Обновляет все выходные сигналы у блока"""
        pass


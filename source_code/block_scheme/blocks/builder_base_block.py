from abc import abstractmethod
from typing import List
import pygame
from source_code.py_base import PyObjectBase
from source_code.windows.base_game_window import BaseGameWindow


class BuilderBaseBlock(PyObjectBase):
    def __init__(self, base_game_window, name, rect, signal_action,
                 inputs, outputs, img):
        self.base_game_window = base_game_window
        self.name = name
        self.rect = rect
        self.signal_action = signal_action
        self.inputs = inputs
        self.outputs = outputs
        if isinstance(img, str):
            if any(img):
                self.img = pygame.image.load(img)
            else:
                self.img = None
        else:
            self.img = img
        if isinstance(self.img, pygame.Surface):
            self.img = pygame.transform.smoothscale(self.img, self.rect.size)

        self.connection_editing = None
        self.is_dragging = False
        self.is_resizing = False
        self.last_mouse_pos = None
        self.last_rect = self.rect.copy()

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
        pass

    @abstractmethod
    def delete(self) -> None:
        pass

    @abstractmethod
    def update_output_signals(self):
        pass


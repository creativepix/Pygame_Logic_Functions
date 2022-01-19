import pygame
import sqlite3
from abc import abstractmethod


class BuilderBaseGameWindow:
    def __init__(self):
        self.all_blocks = []
        self.all_btns = []
        self.all_inp_fields = []
        self.message_window = None
        self.id_connections = {None: None}
        self.choose_block_list = None

    @abstractmethod
    def update_id_connections(self) -> None:
        pass

    @abstractmethod
    def tick(self, screen: pygame.Surface) -> None:
        pass

    @abstractmethod
    def load(self, structure_line: str,
             cursor: sqlite3.Cursor = None) -> None:
        pass

    @abstractmethod
    def mouse_down(self, mouse_button) -> None:
        pass

    @abstractmethod
    def mouse_motion(self) -> None:
        pass

    @abstractmethod
    def mouse_up(self) -> None:
        pass

    @abstractmethod
    def mouse_wheel(self, koof) -> None:
        pass

    @abstractmethod
    def double_mouse_click(self) -> None:
        pass

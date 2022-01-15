import pygame
from abc import abstractmethod
from source_code.py_base import PyObjectBase


# Декоратор для определённых методов, при котором метод запусукается
# только в том случае, если message-окно неактивно
def disable_if_message(func):
    def cmd(*args):
        if args[0].message_window is None:
            func(*args)
    return cmd


# Декоратор, использующийся для mouse_down методов, при котором метод
# запусукается только в том случае, если диалоговое окно неактивно.
# Здесь также добавляется условие: если тот метод не выполняется, то
# mouse_down запускается у message-окна
def mouse_down_check_message(func):
    def cmd(*args):
        if args[0].message_window is None:
            func(*args)
        else:
            if args[1] == 1:
                args[0].message_window.mouse_down()
    return cmd


class BaseWindow(PyObjectBase):
    def __init__(self):
        self.all_btns = []
        self.all_inp_fields = []
        self.all_blocks = []
        self.message_window = None

    def file_drop(self, file_path: str) -> None:
        self.message_window.file_drop(file_path)

    @abstractmethod
    def tick(self, screen: pygame.Surface) -> None:
        pass

    @disable_if_message
    def key_down(self, key: int) -> None:
        for inp_field in self.all_inp_fields:
            inp_field.key_down(key)

    @disable_if_message
    def text_input(self, text: str):
        for inp_field in self.all_inp_fields:
            inp_field.text_input(text)

    @mouse_down_check_message
    def mouse_down(self, mouse_button: int) -> None:
        if mouse_button == 1:
            for btn in self.all_btns:
                btn.mouse_down()

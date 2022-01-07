import pygame


# Класс для всего на экране
class PyObjectBase(object):
    def text_input(self, *args) -> None:
        pass

    def key_down(self, *args) -> None:
        pass

    def mouse_up(self, *args) -> None:
        pass

    def mouse_motion(self, *args) -> None:
        pass

    def mouse_down(self, *args) -> None:
        pass

    def mouse_wheel(self, *args) -> None:
        pass

    def double_mouse_click(self, *args) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass

import pygame

from source_code.constants import BLOCKS_WIDTH
from source_code.py_base import PyObjectBase


class TextFrame(PyObjectBase):
    # Экспериментальный класс многострочного текста
    # Для всяких там описаний уровней
    # TO-DO: протестировать!
    # Ибо писано на коленке
    def __init__(self, text: str, font: pygame.font.Font, rect: pygame.Rect):
        self.rect, self.font = rect, font
        self.lines = self.to_lines(text)
        self.scrolling_pos = 0

    def mouse_wheel(self, koof):
        self.scrolling_pos += koof

    def to_lines(self, text):
        words = text.split()
        line = ''
        lines = []
        for word in words:
            new_line = ' '.join((line, word))
            if self.font.size(new_line)[0] >= self.rect.width:
                lines.append(line)
                line = word
            else:
                line = new_line
        lines.append(line)
        return lines

    def render(self, screen: pygame.Surface) -> None:
        # Цвет поставлен от балды, прошу не обращать внимания
        pygame.draw.rect(screen, (0, 255, 0), self.rect, width=BLOCKS_WIDTH)
        widget = self.font.render('\n'.join(self.lines[
                                            self.scrolling_pos: self.scrolling_pos + self.rect.width // self.font.get_linesize()]),
                                  True, (0, 255, 0))
        font_rect = widget.get_rect()
        font_rect.midtop = self.rect.midtop
        screen.blit(widget, font_rect)

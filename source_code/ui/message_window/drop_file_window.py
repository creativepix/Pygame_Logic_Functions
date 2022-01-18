import pygame
from typing import Callable, List
from source_code.ui.message_window.message_window import MessageWindow


class DropFileWindow(MessageWindow):
    """UI: Окно, в которое вкидывается файл"""
    def __init__(self, text1: str, text2: str, rect: pygame.Rect,
                 available_tags: List[str],
                 dropped_action: Callable[[str], None]):
        """text1 - текст до дропа файла
        text2 - текст после дропа файла"""
        self.text1 = text1
        self.text2 = text2
        self.dropped_action = dropped_action
        self.available_tags = available_tags
        super().__init__(self.text1, rect)

    def file_drop(self, file_path: str) -> None:
        if any([file_path.endswith(available_tag)
                for available_tag in self.available_tags]):
            self.dropped_action(file_path)
            self.text = self.text2

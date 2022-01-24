import pygame
from typing import Callable, List
from pygame_gui.windows import UIFileDialog

from source_code import global_vars
from source_code.ui.message_window.message_window import MessageWindow


class DropFileWindow(MessageWindow):
    """UI: Окно, в которое вкидывается файл"""
    def __init__(self, text1: str, text2: str, rect: pygame.Rect,
                 available_tags: List[str],
                 dropped_action: Callable[[str], None]):
        """text1 - текст до выбора файла
        text2 - текст после выбора файла"""
        self.text1 = text1
        self.text2 = text2
        self.dropped_action = dropped_action
        self.available_tags = available_tags
        self.file_dialog = UIFileDialog(
            pygame.Rect(160, 50, 440, 500),
            global_vars.UI_MANAGER,
            window_title='Load Image...',
            initial_file_path='',
            allow_existing_files_only=True)
        super().__init__(self.text1, rect)

    def file_drop(self, file_path: str) -> None:
        if any([file_path.endswith(available_tag)
                for available_tag in self.available_tags]):
            self.dropped_action(file_path)
            self.text = self.text2
            global_vars.ACTIVE_WINDOW.show_message(self.text2)

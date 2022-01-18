import pygame
from source_code.constants import TRAINING_ARROW_IMG_PATH
from source_code.middlewares.load_image import load_image


class TrainingArrow(pygame.sprite.Sprite):
    """UI: Стрелка-указатель во время обучения"""
    def __init__(self, training_stage: int = None):
        super().__init__()

        self.frames = []
        self.cur_frame = 0
        self.koof = 5
        rows, columns = 3, 20

        sheet = load_image(TRAINING_ARROW_IMG_PATH, colorkey=0)
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        self.rotating = 0
        self.cut_sheet(sheet, columns, rows)
        self.image = self.frames[self.cur_frame]
        self.training_stage = training_stage

    def cut_sheet(self, sheet, columns, rows):
        for j in range(rows):
            for i in range(columns):
                for _ in range(self.koof):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def render(self, screen: pygame.Surface):
        if self.training_stage is not None:
            image = pygame.transform.rotate(self.image, self.rotating)
            image = pygame.transform.smoothscale(image, self.rect.size)
            screen.blit(image, self.rect)
            self.update()

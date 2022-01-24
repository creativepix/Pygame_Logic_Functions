import pygame
from source_code import global_vars


def get_current_horizontal_ration(var: int) -> int:
    return var * global_vars.ACTIVE_SCREEN.get_rect().w // 1200


def get_current_vertical_ration(var: int) -> int:
    return var * global_vars.ACTIVE_SCREEN.get_rect().h // 700


def get_current_rect_w_h_ration(rect: pygame.Rect) -> pygame.Rect:
    rect = pygame.Rect(rect.x, rect.y,
                       get_current_horizontal_ration(rect.w),
                       get_current_vertical_ration(rect.h))
    return rect


def get_current_rect_ration(rect: pygame.Rect) -> pygame.Rect:
    rect = pygame.Rect(get_current_horizontal_ration(rect.x),
                       get_current_vertical_ration(rect.y),
                       get_current_horizontal_ration(rect.w),
                       get_current_vertical_ration(rect.h))
    return rect

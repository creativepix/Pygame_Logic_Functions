import pygame
from source_code import global_vars
from source_code.windows.main_menu_window import MainMenuWindow
from source_code.constants import BACKGROUND_COLOR, START_MENU_SIZE, FPS


def start():
    pygame.init()
    pygame.display.set_caption('Logic_Functions')
    screen = pygame.display.set_mode(START_MENU_SIZE,
                                     pygame.RESIZABLE)
    # Surface активного окна
    global_vars.ACTIVE_SCREEN = screen
    # Активное окно
    global_vars.ACTIVE_WINDOW = MainMenuWindow()

    timer_db_click = 0
    is_db_downed = False

    clock = pygame.time.Clock()
    while global_vars.RUNNING:
        screen.fill(BACKGROUND_COLOR)
        # Перерисовка окна
        global_vars.ACTIVE_WINDOW.tick(global_vars.ACTIVE_SCREEN)
        if not global_vars.RUNNING:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global_vars.RUNNING = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Активному окну - событие
                global_vars.ACTIVE_WINDOW.mouse_down(event.button)
                # Фазы двойного клика
                if event.button == 1:
                    if timer_db_click == 0:
                        timer_db_click = 0.001
                    elif timer_db_click < 0.5:
                        is_db_downed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    global_vars.ACTIVE_WINDOW.mouse_up()
                    # Событие двойного клика
                    if is_db_downed and timer_db_click < 0.5:
                        global_vars.ACTIVE_WINDOW.double_mouse_click()
                        timer_db_click = 0
                    is_db_downed = False
            elif event.type == pygame.MOUSEMOTION:
                global_vars.ACTIVE_WINDOW.mouse_motion()
            elif event.type == pygame.MOUSEWHEEL:
                global_vars.ACTIVE_WINDOW.mouse_wheel(event.y)
            elif event.type == pygame.KEYDOWN:
                global_vars.ACTIVE_WINDOW.key_down(event.key)
            elif event.type == pygame.TEXTINPUT:
                global_vars.ACTIVE_WINDOW.text_input(event.text)
            elif event.type == pygame.DROPFILE:
                global_vars.ACTIVE_WINDOW.file_drop(event.file)
        if not global_vars.RUNNING:
            break

        dt = clock.tick(FPS) / 1000

        # Таймер для двойного клика
        if timer_db_click != 0:
            timer_db_click += dt
            if timer_db_click >= 0.5:
                timer_db_click = 0
                is_db_downed = False

        pygame.display.flip()
    pygame.quit()

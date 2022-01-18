import pygame

FPS = 120
START_MENU_SIZE = 1200, 750
BACKGROUND_COLOR = (0, 0, 0)
# Buttons
SAVE_BTN_RECT = pygame.Rect(10, 50, 150, 35)
SAVE_PIC_BTN_RECT = pygame.Rect(10, 90, 150, 35)
CHECK_SOLUTION_BTN_RECT = pygame.Rect(10, 90, 150, 35)
BACK_BTN_RECT = pygame.Rect(10, 10, 150, 35)
DESCRIPTION_BTN_RECT = pygame.Rect(10, 700, 150, 35)
# Message window
MESSAGE_WINDOW_TEXT_COLOR = pygame.Color("black")
MESSAGE_WINDOW_TEXT_LINES_INDENT = 35
MESSAGE_WINDOW_TEXT_MAX_SYMBOLS = 40
MESSAGE_WINDOW_ALPHA = 75
# Menu window
TEXT_COLOR = (50, 170, 50)
MAIN_MENU_SCORE_RECT = (10, 10, 100, 100)
# Presandbox window
PRESANDBOX_TEXT_WIDTH = 10
# Preplay window
PREPLAY_LEVEL_HEIGHT = 50
PREPLAY_MAX_SYMBOLS_DESCRIPTION = 100
# Training
TRAINING_INSTRUCTIONS = \
    ['Игра создана на основе двоичной логике. Для прохождения уровней вам пре'
     'дстоит строить блок-схемы. Чтобы продолжить нажимайте левую кнопку мыши',
     'Это уровень "Полная противоположность" для обучения механикам игры',
     'От вас требуется сделать так, чтобы все входные сигналы приобрели '
     'противоположные значения',
     'В каждом уровне есть определённые входные блоки (input)',
     'А также выходные (output)',
     'На экране справа расположен список блоков (каждая картинка блока '
     'соответствует его предназначению), которые можно переместить '
     'методом drag-drop (таким же образом можно перемещать блоки). '
     'Попрубуй сделать это с блоком not',
     'В приложении есть и другая функция - функция зума. Чтобы протестировать '
     'её медленно покрути колёсико мыши',
     'В каждом блоке есть входные и выходные сигналы, которые можно соединять '
     'у разных блоков. Соедини выходной сигнал блока input с входным сигналом '
     'блока not',
     'А теперь выходной сигнал блока not с входным сигналом блока output',
     'Каждое соединение имеет цвет: серый - ложь, зелёный - истина',
     'Сигналы input блоков ты можешь поменять, кликнув на блок два раза. '
     'Попытайся сделать это',
     'Примечание: выходные сигналы можно соединять с неограниченным '
     'множестовом входных сигналов, но любой входной сигнал может быть '
     'соединён только с одним выходным',
     'Ещё ты можешь удалить какой-либо блок, нажав на него правой кнопкой '
     'мыши. Проделай это с блоком not',
     'Теперь построй полноценную  рабочую блок-схему так, чтобы '
     'выходные сигналы у блоков input приобретали обратное значение у входных '
     'сигналов блоков output',
     'Сейчас ты можешь проверить свою схему, нажав кнопку "Check"',
     'Справа расположена таблица результатов, где первый столбец - тестовые '
     'значения, второй - значения, которые должные быть, третий - '
     'значок итога (+ или -) и ваш вывод',
     'В правом нижнем крае представлены ваши очки: очки за последнее '
     'решение и очки за самое лучше решение',
     'Вы прошли обучение!']
TRAINING_STARTING_DRAWING_STAGE = 3
TRAINING_ARROW_IMG_PATH = 'source_code/block_scheme/data/training/' \
                          'training_arrow.png'
TRAINING_ARROW_SIZE = (50, 50)
TRAINING_UPPER_TEXT_RECT = pygame.Rect(250, 10, 100, 25)
TRAINING_UPPER_TEXT_SIZE = 25
TRAINING_UPPER_TEXT_MAX_SYMBOLS = 75
TRAINING_TEXT_LINES_INDENT = 25
TRAINING_TEXT_COLOR = (255, 255, 255)
# Score/Results
RESULT_TITLES_INDENT = 15
RESULTS_FONT_SIZE = 15
RESULTS_MAX_SYMBOLS = 8
RESULTS_WIDTH = 60
SCORE_FONT_SIZE = 25
SCORE_GAME_RECT = pygame.Rect(10, 620, 150, 50)
BEST_GAME_SCORE_RECT = pygame.Rect(10, 650, 100, 50)
# Play window
INPUTS_RESULT_TABLE_RECT = pygame.Rect(
    10, 140 + RESULT_TITLES_INDENT, 50, 450)
NEEDED_OUTPUTS_RESULT_TABLE_RECT = pygame.Rect(
    70, 140 + RESULT_TITLES_INDENT, 50, 450)
OUTPUTS_RESULT_TABLE_RECT = pygame.Rect(
    130, 140 + RESULT_TITLES_INDENT, 50, 450)
# Blocks
BASE_BLOCK_IMAGES_PATH = 'source_code/block_scheme/data/block_imgs/base_blocks'
MAX_LEN_BLOCK_NAME = 7
BLOCK_MIN_SIZE = (30, 30)
BLOCK_MAX_SIZE = (240, 240)
BLOCK_TEXT_MIN_SIZE = 10
BLOCK_TEXT_MAX_SIZE = 80
BLOCKS_COLOR = (170, 170, 170)
BLOCKS_WIDTH = 2
BLOCK_CONNECTION_INPUT_COLOR = (170, 170, 170)
BLOCK_CONNECTION_OUTPUT_COLOR = (170, 170, 170)
BLOCK_CONNECTION_FALSE_COLOR = (170, 170, 170)
BLOCK_CONNECTION_TRUE_COLOR = (50, 170, 50)
BLOCKS_NAME_COLOR = pygame.Color("seagreen")
BLOCKS_INDENT_FOR_RESIZING = 4
STARTING_LEFTTOP_BLOCKS_WITHOUT_STRUCTURE = (300, 300)
# BlockConnections
CONNECTION_LOCAL_RADIUS_PERCENTAGE = 8
# BlockList
SPACE_BLOCKS_IN_BLOCK_LIST = 10
BLOCK_SIZE_IN_BLOCK_LIST = (60, 60)
BLOCK_LIST_WIDTH = BLOCK_SIZE_IN_BLOCK_LIST[0] + 15
# PyList
BASE_CELL_IN_BLOCK_SIZE = BLOCK_SIZE_IN_BLOCK_LIST
# Ui
BUTTON_RECT_COLOR = (170, 170, 170)
TABLE_X_SYMBOL_SIZE = (20, BASE_CELL_IN_BLOCK_SIZE[1])
LIST_CELLS_COLOR = (170, 170, 170)

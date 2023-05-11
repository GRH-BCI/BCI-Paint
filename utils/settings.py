import pygame

pygame.init()
pygame.font.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 255, 0)
ORANGE = (255, 150, 0)
GREEN = (0, 0, 255)
PURPLE = (255, 0, 255)

FPS = 60

DEFAULT_WIDTH, DEFAULT_HEIGHT = 800, 700

# Specifies the number of rows and columns if using a grid
ROWS = COLS = 50

TOOLBAR_HEIGHT = DEFAULT_WIDTH - DEFAULT_HEIGHT

PIXEL_SIZE = DEFAULT_WIDTH // COLS

BG_COLOUR = WHITE

# Indicates whether the grid lines should be drawn or not
DRAW_GRID_LINES = False

def get_font(size):
    return pygame.font.Font(pygame.font.get_default_font(), size)
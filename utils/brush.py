from .settings import *
from enum import Enum
import math
 
class BrushSize(Enum):
    """
    A class used to associate a brush size with a numeric value

    Varients:
    ----------
    SMALL
    MEDIUM
    LARGE
    """
    SMALL = 10
    MEDIUM = 20
    LARGE = 30

class Brush:
    """
    A class used to represent the users brush on a canvas

    Attributes:
    ----------
    x: int
        The x coordinate of the center of the brush
    y: int
        The y coordinate of the center corner of the brush
    raduis: int
        The size of the brush
    colour: tuple (r, g, b)
        The colour of the paint on the brush
    vel: int
        How many pixels the brush moves when a key is pressed

    Methods:
    ----------
    draw(win)
        Draws the brush on the canvas

    handle_movement(keys_pressed)
        Changes the position of the brush based on the keys pressed 
    """

    def __init__(self, x, y, radius, colour) -> None:
        """
        Parameters:
        ----------
        x: int
            The x coordinate of the center of the brush
        y: int
            The y coordinate of the center corner of the brush
        raduis: int
            The size of the brush
        colour: tuple (r: int, g,: int b: int)
            The colour of the paint on the brush
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = pygame.Color(colour)
        self.vel = 5


    def draw(self, win):
        """
        Draws the brush on the canvas

        Parameters:
        ----------
        win: Surface
            The window to draw the brush on
        """
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)


    def handle_movement(self, win, keys_pressed, theta):
        """
        Moves the position of the brush on the canvas

        Parameters:
        ----------
        win: Surface
            The window to move the brush on
        keys_pressed: Sequence[Bool]
            The state of the keyboard keys
        theta: int
            The direction to move the brush if using a single input key (0 is up)
        """
        # Allows the brush to be move with the 4 arrow keys
        if keys_pressed[pygame.K_LEFT] and self.x - self.vel >= TOOLBAR_HEIGHT + self.radius:
            self.x -= self.vel
        if keys_pressed[pygame.K_RIGHT] and self.x + self.vel < win.get_width():
            self.x += self.vel
        if keys_pressed[pygame.K_UP] and self.y - self.vel > 0:
            self.y -= self.vel
        if keys_pressed[pygame.K_DOWN]  and self.y + self.vel < win.get_height():
            self.y += self.vel

        # Allows the brush to be moved with a single input (the w key) using the angle of the line in the direction
        # animation when the key was pressed
        if keys_pressed[pygame.K_w]:
            if TOOLBAR_HEIGHT + self.radius <= self.x + math.sin(2*math.pi*theta/360) * self.vel <= win.get_width():
                self.x += math.sin(2*math.pi*theta/360) * self.vel
            
            if 0 <= self.y - math.cos(2*math.pi*theta/360) * self.vel <= win.get_height():
                self.y -= math.cos(2*math.pi*theta/360) * self.vel

            pygame.event.post(pygame.event.Event(PAUSE_ROTATION))
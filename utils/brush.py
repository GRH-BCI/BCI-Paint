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
        self.x_vel = 0
        self.y_vel = 0


    def draw(self, win):
        """
        Draws the brush on the canvas

        Parameters:
        ----------
        win: Surface
            The window to draw the brush on
        """
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)


    def handle_movement(self, win, keys_pressed, theta, mode, move):
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
        if mode == "Game":
            # Allows the brush to be moved with a single input (the w key) using the angle of the line in the direction
            # animation when the key was pressed
            if keys_pressed[pygame.K_w]:
                if TOOLBAR_HEIGHT + self.radius <= self.x + math.sin(2*math.pi*theta/360) * self.vel <= win.get_width():
                    self.x_vel = math.sin(2*math.pi*theta/360) * self.vel
                
                if 0 <= self.y - math.cos(2*math.pi*theta/360) * self.vel <= win.get_height():
                    self.y_vel = math.cos(2*math.pi*theta/360) * self.vel


                pygame.event.post(pygame.event.Event(PAUSE_ROTATION))

            if move:
                self.x += self.x_vel
                self.y -= self.y_vel

                # If the brush goes over the left or right bound draw it at the edge of the bound
                if self.x - self.radius <= TOOLBAR_HEIGHT:
                    self.x  = TOOLBAR_HEIGHT + self.radius
                
                elif self.x + self.radius >= win.get_width():
                    self.x = win.get_width() - self.radius

                # If the brush hits the left or right bound, reflect it and slow the speed
                if self.x - self.radius <= TOOLBAR_HEIGHT or self.x + self.radius >= win.get_width():
                    self.x_vel = -(self.x_vel*0.95)
                    self.y_vel = self.y_vel*0.95

                # If the brush goes over the top or bottom bound draw it at the edge of the bound
                if self.y - self.radius <= 0:
                    self.y = self.radius
                    
                elif self.y + self.radius >= win.get_height():
                    self.y = win.get_height() - self.radius
                    
                # If the brush hits the top or bottom bound, reflect it and slow the speed
                if self.y - self.radius <= 0 or self.y + self.radius >= win.get_height():
                    self.y_vel = -(self.y_vel*0.95)
                    self.x_vel = self.x_vel*0.95

        
        elif mode == "Casual":
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
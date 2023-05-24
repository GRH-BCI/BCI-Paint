from .settings import *
import pygame

class ColorPicker:
    """
    A class used to represent a colour picker with hue, saturation, and lightness elements

    Attributes:
    ----------
    x: int
        The x coordinate of the top left corner of the colour picker
    y: int
        The y coordinate of the top left corner of the colour picker
    width: int
        The width of the colour picker
    height: int
        The height of the colour picker
    bg: Surface
        The surface where the hue, saturation, and lightness gradients are drawn
    hue: int
        The hue component of the colour (range: 0-360)
    sat: int
        The saturation component of the colour (range: 0-100)
    light: int
        The lightness component of the colour (range: 0-100)
    hue_bound: Rect
        The boundary of the hue gradient
    sat_bound: Rect
        The boundary of the saturation gradient
    light_bound: Rect
        The boundary of the lightness gradient
    hue_pos: int
        The x coordinate of the mouse for the last instance a hue was selected
    sat_pos: int
        The x coordinate of the mouse for the last instance a saturation was selected
    light_pos: int
        The x coordinate of the mouse for the last instance a lightness was selected

    Methods:
    ----------
    update()
        Update the user selection for hue, saturation, and lightness
    draw(win)
        Draws the colour picker on the window
    """

    def __init__(self, x, y):
        """
        Parameters:
        ----------
        x: int
            The x coordinate of the top left corner of the colour picker
        y: int
            The y coordinate of the top left corner of the colour picker
        """
        self.x = x
        self.y = y
        self.width = 400
        self.height = 100
        self.bg = pygame.Surface((self.width, self.height))
        self.hue = 0
        self.sat = 0
        self.light = 0
        self.hue_bound = pygame.Rect(x + 20, y + 10, 360, 20)
        self.sat_bound = pygame.Rect(x + 20, y + 40, 100*(360//100), 20)
        self.light_bound = pygame.Rect(x + 20, y + 70, 100*(360//100), 20)
        self.hue_pos = self.hue_bound.x
        self.sat_pos = self.sat_bound.x
        self.light_pos = self.light_bound.x

        self.bg.fill((255, 255, 255))

        # Draw hue gradient
        for i in range(360):
            colour = pygame.Color(BLACK)
            colour.hsla = (i, 100, 50, 100)
            pygame.draw.rect(self.bg, colour, (i + 20, 10, 1, 20))

        # Draw saturation gradient
        for i in range(100):
            colour = pygame.Color(BLACK)
            colour.hsla = (0, i, 50, 100)
            pygame.draw.rect(self.bg, colour, (i*(360//100) + 20, 40, 360//100, 20))

        # Draw lightness gradient
        for i in range(100):
            colour = pygame.Color(BLACK)
            colour.hsla = (0, 100, i, 100)
            pygame.draw.rect(self.bg, colour, (i*(360//100) + 20, 70, 360//100, 20))
    
    def update(self):
        """
        Updates the user's selection for hue, saturation, and lightness

        Parameters:
        ----------
        None
        """
        mouse_pressed = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()

        if mouse_pressed[0] and self.hue_bound.left <= x <= self.hue_bound.right and self.hue_bound.top <= y <= self.hue_bound.bottom:
            self.hue_pos = x
            self.hue = self.hue_pos - self.hue_bound.x
            pygame.event.post(pygame.event.Event(COLOUR_CHANGE))

        elif mouse_pressed[0] and self.sat_bound.left <= x <= self.sat_bound.right and self.sat_bound.top <= y <= self.sat_bound.bottom:
            self.sat_pos = x
            self.sat = round((self.sat_pos - self.sat_bound.x)/(360//100))
            pygame.event.post(pygame.event.Event(COLOUR_CHANGE))

        elif mouse_pressed[0] and self.light_bound.left <= x <= self.light_bound.right and self.light_bound.top <= y <= self.light_bound.bottom:
            self.light_pos = x
            self.light = round((self.light_pos - self.light_bound.x)/(360//100))
            pygame.event.post(pygame.event.Event(COLOUR_CHANGE))


    def draw(self, win):
        """
        Draws the colour picker on the window

        Parameters:
        ----------
        win: Surface
            The window to draw the colour picker on
        """
        # Draw the gradients
        win.blit(self.bg, pygame.Rect(self.x, self.y, self.width, self.height))
        colour = pygame.Color(BLACK)
        radius = 15

        # Draw the hue selector circle
        center = (self.hue_pos, self.y + 20)
        colour.hsla = (self.hue, 100, 50, 100)
        pygame.draw.circle(win, colour, center, radius)

        # Draw the saturation selector circle
        center = (self.sat_pos, self.y + 50)
        colour.hsla = (self.hue, self.sat, 50, 100)
        pygame.draw.circle(win, colour, center, radius)

        # Draw the lightness selector circle
        center = (self.light_pos, self.y + 80)
        colour.hsla = (self.hue, 100, self.light, 100)
        pygame.draw.circle(win, colour, center, radius)

        # Draw the overall colour square
        colour.hsla = (self.hue, self.sat, self.light, 100)
        pygame.draw.rect(win, colour, (self.sat_bound.right + 20, self.y + 40, 50, 50))
from .settings import *
import math
import pygame

class Button:
    """
    A class used to represent a clickable button

    Attributes:
    ----------
    x: int
        The x coordinate of the top left corner of the button
    y: int
        The y coordinate of the top left corner of the button
    width: int
        The width of the button
    height: int
        The height of the button
    colour: tuple (r, g, b)
        The colour of the button
    text: str, optional
        The text to display on the button
    text_colour: tuple (r, g, b), optional
        The colour of the text on the button. (Default is black)
    selected: bool
        Indicates whether the button is selected or not

    Methods:
    ----------
    draw(win)
        Draws the button on the canvas

    clicked(pos)
        Determines if the button was clicked based on the given position 
    """

    def __init__(self, x, y, width, height, colour, selected=False, text=None, text_colour=BLACK) -> None:
        """
        Parameters:
        ----------
        x: int
            The x coordinate of the top left corner of the button
        y: int
            The y coordinate of the top left corner of the button
        width: int
            The width of the button
        height: int
            The height of the button
        colour: tuple (r: int, g,: int b: int)
            The colour of the button
        selected: bool
            Indicates whether the button is selected or not
        text: str, optional
            The text to display on the button
        text_colour: tuple (r: int, g,: int b: int), optional
            The colour of the text on the button. (Default is black)
        """

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = pygame.Color(colour)
        self.text = text
        self.text_colour = text_colour
        self.selected = selected


    def draw(self, win):
        """
        Draws the button on the canvas

        Parameters:
        ----------
        win: Surface
            The window to draw the button on
        """

        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

        if self.selected:
            border_colour = BLACK
        elif self.colour == WHITE:
            border_colour = GREY
        else:
            border_colour = WHITE
        
        pygame.draw.rect(win, border_colour, (self.x, self.y, self.width, self.height), 2)

        if self.text:
            button_font = get_font(16)
            text_surface = button_font.render(self.text, 1, self.text_colour)
            win.blit(text_surface, (self.x + self.width/2 - text_surface.get_width()/2,
                                    self.y + self.height/2 - text_surface.get_height()/2))


    def clicked(self, pos):
        """
        Determines if the button was clicked based on the given position

        Parameters:
        ----------
        pos: tuple (x: int, y: int)
            The position of the mouse when a click event occured

        Returns:
        bool:
            True indicates the button was clicked and false indicates the button was not clicked
        """

        x, y = pos

        if not (x >= self.x and x <= self.x + self.width):
            return False
        if not (y >= self.y and y <= self.y + self.height):
            return False
        
        self.selected = True
        
        return True
    
class RoundButton:
    """
    A class used to represent a circular clickable button

    Attributes:
    ----------
    x: int
        The x coordinate of the center of the button
    y: int
        The y coordinate of the center of the button
    radius: int
        The radius of the button
    colour: tuple (r, g, b)
        The colour of the button
    text: str, optional
        The text to display on the button
    text_colour: tuple (r, g, b), optional
        The colour of the text on the button. (Default is black)
    selected: bool
        Indicates whether the button is selected or not

    Methods:
    ----------
    draw(win)
        Draws the button on the canvas

    clicked(pos)
        Determines if the button was clicked based on the given position 
    """

    def __init__(self, x, y, radius, colour, selected=False, text=None, text_colour=BLACK) -> None:
        """
        Parameters:
        ----------
        x: int
            The x coordinate of the center of the button
        y: int
            The y coordinate of the center of the button
        radius: int
            The radius of the button
        colour: tuple (r, g, b)
            The colour of the button
        selected: bool
            Indicates whether the button is selected or not
        text: str, optional
            The text to display on the button
        text_colour: tuple (r, g, b), optional
            The colour of the text on the button. (Default is black)
        """

        self.x = x
        self.y = y
        self.radius = radius
        self.colour = pygame.Color(colour)
        self.text = text
        self.text_colour = text_colour
        self.selected = selected


    def draw(self, win):
        """
        Draws the button on the canvas

        Parameters:
        ----------
        win: Surface
            The window to draw the button on
        """

        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)

        if self.selected:
            border_colour = BLACK
        else:
            border_colour = WHITE
        
        pygame.draw.circle(win, border_colour, (self.x, self.y), self.radius, 2)

        if self.text:
            button_font = get_font(16)
            text_surface = button_font.render(self.text, 1, self.text_colour)
            win.blit(text_surface, (self.x - text_surface.get_width()/2,
                                    self.y - text_surface.get_height()/2))


    def clicked(self, pos):
        """
        Determines if the button was clicked based on the given position

        Parameters:
        ----------
        pos: tuple (x: int, y: int)
            The position of the mouse when a click event occured

        Returns:
        bool:
            True indicates the button was clicked and false indicates the button was not clicked
        """

        x, y = pos

        x_sqr = (x - self.x)**2
        y_sqr = (y - self.y)**2

        if not (math.sqrt(x_sqr + y_sqr) < self.radius):
            return False
        
        self.selected = True
        
        return True
    

class SliderButton:
    """
    A class used to represent a slider button

    Attributes:
    ----------
    x: int
        The x coordinate of the top left of the slider button
    y: int
        The y coordinate of the top left of the slider button
    high: int
        The upper bound for the value of the slider
    low: int
        The lower bound for the value of the slider
    circle_x:
        The x position of the circle on the slider
    circle_r:
        The radius of the circle on the slider
    value:
        The value of the slider (between high and low)
    inner_bound:
        The rectangle which the slider moves over
    outer_bound:
        The rectangle which encapsulates the slider (circle) and the inner rectangle

    Methods:
    ----------
    draw(win)
        Draws the slider on the canvas

    update()
        Checks if the slider was changed and updates the value 
    """

    def __init__(self, x, y, w, h, high, low, start):
        """
        Parameters:
        ----------
        x: int
            The x coordinate of the top left of the slider button
        y: int
            The y coordinate of the top left of the slider button
        w: int
            The width of the slider
        h:
            The height of the slider
        high: int
            The upper bound for the value of the slider
        low: int
            The lower bound for the value of the slider
        start: int
            The value for the slider to start at
        """
        self.x = x
        self.y = y
        self.high = high
        self.low = low
        self.circle_x = x + start / (high - low) * w
        self.circle_r = h/2 + 10
        self.value = start
        self.inner_bound = pygame.Rect(x, y, w, h)
        self.outer_bound = pygame.Rect(x - self.circle_r, y - self.circle_r, w + 2* self.circle_r, h + 2* self.circle_r)
    
    def draw(self, win):
        """
        Draws the slider on the surface

        Parameters:
        ----------
        win:
            The surface to draw the slider on
        """
        pygame.draw.rect(win, (255, 255, 255), self.outer_bound)
        pygame.draw.rect(win, (0, 0, 0), self.inner_bound)
        pygame.draw.circle(win, (200, 200, 200), (self.circle_x, (self.inner_bound.h / 2 + self.inner_bound.y)), self.circle_r)

    def update(self):
        """
        Checks if the slider has been changed and updates the value of the slider

        Parameters:
        None
        """
        mouse_pressed = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()

        if mouse_pressed[0] and self.inner_bound.left <= x <= self.inner_bound.right and self.inner_bound.top <= y <= self.inner_bound.bottom:
            self.circle_x = x
            self.value = float(float(x - self.inner_bound.x) / float(self.inner_bound.w) * (self.high - self.low) + self.low)
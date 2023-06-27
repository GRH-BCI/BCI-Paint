from .settings import *
import math

class Clock:

    def __init__(self, x, y, r) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.left = x - r
        self.right = x + r
        self.top = y - r
        self.bottom = y + r

    def update(self):
        self.left = self.x - self.r
        self.right = self.x + self.r
        self.top = self.y - self.r
        self.bottom = self.y + self.r

    def draw(self, win, colour, theta):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.r) # center of the clock
        pygame.draw.circle(win, BLACK, (self.x, self.y), self.r, 15) # Border of the clock
        pygame.draw.circle(win, colour, (self.x, self.y), self.r - 15 , 5) # Coloured inside border of the clock

        pygame.draw.line(win, BLACK, (self.x, self.y), self.calc_rotation(self.r - 30, theta, self.x, self.y), 10)

    def calc_rotation(self, r, theta, x_center, y_center):
        """
        Calculates the x and y position for the end of a line at a given angle

        Parameters:
        ----------
        r: int
            The radial length of the line
        theta: int
            The angle of the line in degrees (0 represents up)
        x_center: int
            The x coordinate of the point which one end of the line is fixed and the other endpoint rotates around
        y_center: int
            The y coordinate of the point which one end of the line is fixed and the other endpoint rotates around
        """
        y = math.cos(2*math.pi*theta/360)*r
        x = math.sin(2*math.pi*theta/360)*r
        return x + x_center, -(y - y_center)
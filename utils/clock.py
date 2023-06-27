from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

class Clock:
    """
    Represents a clock animation used to determine the direction of the brush
    """
    
    def __init__(self, x, y, r, outer_thickness=16, inner_thickness=8) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.outer_thickness = outer_thickness
        self.inner_thickness = inner_thickness
        self.outer_border = QRect(x, y, r, r)
        self.inner_border = QRect(x + outer_thickness//2 + inner_thickness//2 - 1, y + outer_thickness//2 + inner_thickness//2 - 1, r - outer_thickness - inner_thickness + 2, r - outer_thickness - inner_thickness + 2)
        self.arrow = QLineF(x + r//2, y + r//2, x + r//2, y + r//2 + 75)

    def draw(self, qpainter, theta, color):
        """
        Draws the clock on the window
        """

        qpainter.setPen(QPen(Qt.black, self.outer_thickness, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        # Draw the outer border
        qpainter.drawEllipse(self.outer_border)

        # Draw the arrow
        x, y = self.calc_rotation(self.r//2 - 25, theta, self.outer_border.center().x(), self.outer_border.center().y())
        self.arrow.setP2(QPointF(x, y))
        qpainter.drawLine(self.arrow)

        qpainter.setPen(QPen(color, self.inner_thickness, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        # Draw the inner border
        qpainter.drawEllipse(self.inner_border)

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
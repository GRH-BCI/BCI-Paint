from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import math
from .settings import LineStyle, BrushStyle

def drawStroke(win):
    """
    Draws the brush stroke on the canvas

    Paramenters:
    ----------
    win: Window
        The main window
    """

    # If the spray paint option is chosen it overrides the line style
    if win.brushStyle == BrushStyle.SPRAYPAINT:
        # Set the pen of the painter
        win.painter.setPen(QPen(win.brushColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        # Draw the spray
        for n in range(100):
            xo = random.gauss(0, win.brush.width())
            yo = random.gauss(0, win.brush.width())
            win.painter.drawPoint(int(win.x + xo), int(win.y + yo))

    elif win.brushStyle == BrushStyle.GRAFFITI:
        # Set the pen of the painter
        win.painter.setPen(QPen(win.brushColor, win.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        
        # Draw line from the last point of cursor to the current point
        win.painter.drawLine(win.lastPoint, QPointF(win.x, win.y))

        # Draw the spray
        win.painter.setPen(QPen(win.brushColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        for n in range(500):
            xo = random.gauss(0, win.brush.width())
            yo = random.gauss(0, win.brush.width())
            win.painter.drawPoint(int(win.x + xo), int(win.y + yo))

        # Draw the drip
        win.painter.setPen(QPen(win.brushColor, win.brushSize//4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        drip = random.random()
        if drip > 0.40 and math.sqrt(yo**2 + xo**2) < win.brush.size().width():
            win.painter.drawLine(QPointF(int(win.x + xo), int(win.y + yo)), QPointF(int(win.x + xo), int(win.y + yo + 100*random.random())))
    
    elif win.brushStyle == BrushStyle.SPLATTER:
        # Set the pen of the painter
        win.painter.setPen(QPen(win.brushColor, win.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        
        # Draw line from the last point of cursor to the current point
        win.painter.drawLine(win.lastPoint, QPointF(win.x, win.y))

        for n in range(20):
            xo = random.gauss(0, win.brush.width()*2)
            yo = random.gauss(0, win.brush.width()*2)
            win.painter.drawPoint(int(win.x + xo), int(win.y + yo))

    elif win.brushStyle == BrushStyle.ABSTRACT:
        # Draw the random points
        for n in range(10*win.brushSize):
            xo = random.gauss(0, win.brush.width()*2)
            yo = random.gauss(0, win.brush.width()*2)

            splatterSize = 1/math.sqrt(xo**2 + yo**2)*5
            win.painter.setPen(QPen(win.brushColor, splatterSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            win.painter.drawPoint(int(win.x + xo), int(win.y + yo))

    elif win.lineStyle == LineStyle.DOTTED:
        # Set the pen of the painter
        win.painter.setPen(QPen(win.brushColor, win.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        
        # Draw a point around the current brush position
        win.painter.drawPoint(QPointF(win.x, win.y))

    else:
        # Set the pen of the painter
        win.painter.setPen(QPen(win.brushColor, win.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        
        # Draw line from the last point of cursor to the current point
        win.painter.drawLine(win.lastPoint, QPointF(win.x, win.y))


def handleBrushMovement(win, event, deltaX, deltaY):
    """
    Handles the movement of the brush accordingly with the key pressed

    Paramenters:
    ----------
    win: Window
        The main window
    deltaX: int
        The change in the x direction of the brush
    """

    # Allow the brush to move with the arrow keys or the w key and the clock animation
    if event.key() == Qt.Key_Up:
        if handleVerticalMovement(win, win.brushSpeed):
            win.brushSpeed = -win.brushSpeed
    
    elif event.key() == Qt.Key_Down:
        if handleVerticalMovement(win, -win.brushSpeed):
            win.brushSpeed = -win.brushSpeed
    
    elif event.key() == Qt.Key_Left:
        if handleHorizontalMovement(win, -win.brushSpeed):
            win.brushSpeed = -win.brushSpeed
    
    elif event.key() == Qt.Key_Right:
        if handleHorizontalMovement(win, win.brushSpeed):
            win.brushSpeed = -win.brushSpeed
    
    elif event.key() == win.BCIKey:
        if handleVerticalMovement(win, deltaY):
            deltaY = -deltaY
        
        if handleHorizontalMovement(win, deltaX):
            deltaX = -deltaX

    return deltaX, deltaY

def handleVerticalMovement(win, deltaY):
    """
    Checks for a collision with the top and bottom of the screen and accordingly handles the verical movement of the brush

    Paramenters:
    ----------
    win: Window
        The main window
    deltaY: int
        The change in the y direction of the brush
    """
    
    # Check if the brush will go beyond the toolbar at the top of the window
    if win.y - deltaY < win.brush.height():
        win.y = win.brush.height()
        return True
    # Check if the brush will go beyond the the bottom of the window
    elif win.y + win.brush.height() - deltaY > win.imageTools.size().height():
        win.y = win.imageTools.size().height() - win.brush.height()
        return True
    else:
        win.y -= deltaY
        return False


def handleHorizontalMovement(win, deltaX):
    """
    Checks for a collision with the left and right of the screen and accordingly handles the horizontal movement of the brush
    """

    # Check if the brush will go beyond the right side of the window
    if win.x + win.brush.width() + deltaX > win.imageTools.size().width():
        win.x = win.imageTools.size().width() - win.brush.width()
        return True
    # Check if the brush will go beyond the toolbar on the left
    elif win.x + deltaX < 0 + win.brush.width():
        win.x = 0 + win.brush.width()
        return True
    else:
        win.x += deltaX
        return False
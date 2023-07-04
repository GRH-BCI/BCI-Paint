from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
import sys
import math
import os
import random
from utils import *
 
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        # Setting the title
        self.setWindowTitle("BCI Paint")

        # Setting the window icon
        self.setWindowIcon(QIcon(os.path.join("Assets", "paint-palette.png")))
 
        # Setting geometry to main window
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowState(Qt.WindowMaximized)
 
        # Creating an image object for the canvas
        screenSize = self.size()
        canvasSize = QSize(screenSize.width() - 400, screenSize.height() - 30)
        self.image = QImage(canvasSize, QImage.Format_RGB32)
 
        # Fill the canvas with white
        self.image.fill(Qt.white)

        # Create an image to draw the tools overtop of the painting but not included in the painting
        self.imageTools = QImage(canvasSize, QImage.Format_ARGB32)
        self.imageTools.fill(QColor(255, 255, 255, 0))

        # Initialize the angle for arrow and the rate of change of the angle
        self.theta = 0
        self.step = 1

        # Set the timer for the angle of the clock arm
        self.angleTimer = QTimer(self, interval=100)
        self.angleTimer.timeout.connect(self.updateAngle)
        self.angleTimer.start()

        # Initialize the rainbow colour to off and start the rainbow timer
        self.rainbow = False

        self.rainbowTimer = QTimer(self, interval=10)
        self.rainbowTimer.timeout.connect(self.updateColor)
        self.rainbowTimer.start()

        # Set the timer for the blink of the brush
        self.blink = True

        self.blinkTimer = QTimer(self, interval=1000)
        self.blinkTimer.timeout.connect(self.blinkBrush)
        self.blinkTimer.start()

        # Initialize the mode to freestyle
        self.mode = Mode.FREESTYLE

        self.feedback = False
 
        # Initial brush size
        self.brushSize = 12
        # Initial brush speed
        self.brushSpeed = self.brushSize
        # Initail brush color
        self.brushColor = QColor(0, 0, 0)
        # Initial transparancy value
        self.alpha = 255
        # Initial line style
        self.lineStyle = LineStyle.SOLID
        # Initialize the brush style
        self.brushStyle = BrushStyle.MARKER

        # Creating the brush
        self.brush = QRectF(0, 0, self.brushSize/2, self.brushSize/2)

        # Initializing the position of the brush
        self.x = self.image.size().width() // 2
        self.y = self.image.size().height() // 2

        # Creating the clock animation
        self.clock =  Clock(25, 50, 350)
 
        # QPoint object to tract the point
        self.lastPoint = QPointF()

        # Painter that draws the brush lines on the canvas
        self.painter = QPainter(self.image)

        # Creating the menu bar
        createMenu(self)
        

    def keyPressEvent(self, event):
        # If the painter is interrupted, restart the painter
        if self.painter.isActive():
            self.painter.end()
        
        # Creating painter object
        self.painter = QPainter(self.image)
            
        # Set the pen of the painter
        self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        if self.mode == Mode.FREESTYLE:
            self.brushSpeed = abs(self.brushSpeed)
            
            # Change the last point
            self.lastPoint = QPointF(self.x, self.y)

            # Allow the brush to move with the arrow keys or the w key and the clock animation
            if event.key() == Qt.Key_Up:
                # Check if the brush will go beyond the toolbar at the top of the window
                if self.y - self.brushSpeed < self.brush.height():
                    self.y = self.brush.height()
                else:
                    self.y -= self.brushSpeed
            
            elif event.key() == Qt.Key_Down:
                # Check if the brush will go beyond the bottom of the window
                if self.y + self.brush.height() + self.brushSpeed > self.imageTools.size().height():
                    self.y = self.imageTools.size().height() - self.brush.height()
                else:
                    self.y += self.brushSpeed
            
            elif event.key() == Qt.Key_Left:
                # Check if the brush will go beyond the toolbar on the left
                if self.x - self.brushSpeed < 0 + self.brush.width():
                    self.x = 0 + self.brush.width()
                else:
                    self.x -= self.brushSpeed
            
            elif event.key() == Qt.Key_Right:
                # Check if the brush will go beyond the right side of the window
                if self.x + self.brush.width() + self.brushSpeed > self.imageTools.size().width():
                    self.x = self.imageTools.size().width() - self.brush.width()//2
                else:
                    self.x += self.brushSpeed
            
            elif event.key() == Qt.Key_W:
                # calculate the change in the x and y direction based on the angle
                deltaX = math.sin(2*math.pi*self.theta/360)*self.brushSpeed
                deltaY = math.cos(2*math.pi*self.theta/360)*self.brushSpeed
                
                # Check if the brush will go beyond the right side of the window
                if self.x + self.brush.width() + deltaX > self.imageTools.size().width():
                    self.x = self.imageTools.size().width() - self.brush.width()
                # Check if the brush will go beyond the toolbar on the left
                elif self.x + deltaX < 0 + self.brush.width():
                    self.x = 0 + self.brush.width()
                else:
                    self.x += deltaX

                # Check if the brush will go beyond the toolbar at the top of the window
                if self.y - deltaY < self.brush.height():
                    self.y = self.brush.height()
                # Check if the brush will go beyond the the bottom of the window
                elif self.y + self.brush.height() - deltaY > self.imageTools.size().height():
                    self.y = self.imageTools.size().height() - self.brush.height()
                else:
                    self.y -= deltaY
            
            # If the spray paint option is chosen it overrides the line style
            if self.brushStyle == BrushStyle.SPRAYPAINT:
                # Set the pen of the painter
                self.painter.setPen(QPen(self.brushColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

                # Draw the spray
                for n in range(100):
                    xo = random.gauss(0, self.brush.width())
                    yo = random.gauss(0, self.brush.width())
                    self.painter.drawPoint(int(self.x + xo), int(self.y + yo))

            elif self.brushStyle == BrushStyle.GRAFFITI:
                # Set the pen of the painter
                self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                
                # Draw line from the last point of cursor to the current point
                self.painter.drawLine(self.lastPoint, QPointF(self.x, self.y))

                # Draw the spray
                self.painter.setPen(QPen(self.brushColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

                for n in range(500):
                    xo = random.gauss(0, self.brush.width())
                    yo = random.gauss(0, self.brush.width())
                    self.painter.drawPoint(int(self.x + xo), int(self.y + yo))

                # Draw the drip
                self.painter.setPen(QPen(self.brushColor, self.brushSize//4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

                drip = random.random()
                if drip > 0.40 and math.sqrt(yo**2 + xo**2) < self.brush.size().width():
                    self.painter.drawLine(QPointF(int(self.x + xo), int(self.y + yo)), QPointF(int(self.x + xo), int(self.y + yo + 100*random.random())))
            
            elif self.brushStyle == BrushStyle.SPLATTER:
                # Set the pen of the painter
                self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                
                # Draw line from the last point of cursor to the current point
                self.painter.drawLine(self.lastPoint, QPointF(self.x, self.y))

                for n in range(20):
                    xo = random.gauss(0, self.brush.width()*2)
                    yo = random.gauss(0, self.brush.width()*2)
                    self.painter.drawPoint(int(self.x + xo), int(self.y + yo))

            elif self.brushStyle == BrushStyle.ABSTRACT:
                # Draw the random points
                for n in range(10*self.brushSize):
                    xo = random.gauss(0, self.brush.width()*2)
                    yo = random.gauss(0, self.brush.width()*2)

                    splatterSize = 1/math.sqrt(xo**2 + yo**2)*5
                    self.painter.setPen(QPen(self.brushColor, splatterSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.painter.drawPoint(int(self.x + xo), int(self.y + yo))

            elif self.lineStyle == LineStyle.DOTTED:
                # Set the pen of the painter
                self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                
                # Draw a point around the current brush position
                self.painter.drawPoint(QPointF(self.x, self.y))

            else:
                # Set the pen of the painter
                self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                
                # Draw line from the last point of cursor to the current point
                self.painter.drawLine(self.lastPoint, QPointF(self.x, self.y))
            
            self.update()

        elif self.mode == Mode.GAME:
            # Calculate the change in the x and y direction based on the angle
            deltaX = math.sin(2*math.pi*self.theta/360)*self.brushSpeed
            deltaY = math.cos(2*math.pi*self.theta/360)*self.brushSpeed

            self.brushSpeed = abs(self.brushSpeed)

            for i in range(0, 300):
                if self.painter.isActive() == False:
                    break

                # Slow the brush down over time
                if i > 150:
                    deltaY = deltaY*0.99
                    deltaX = deltaX*0.99
    
                # Change the last point
                self.lastPoint = QPointF(self.x, self.y)

                # Allow the brush to move with the arrow keys or the w key and the clock animation
                if event.key() == Qt.Key_Up:
                    # Check if the brush will go beyond the toolbar at the top of the window
                    if self.y - self.brushSpeed < self.brush.height():
                        self.y = self.brush.height()
                        self.brushSpeed = -self.brushSpeed
                    # Check if the brush will go beyond the bottom of the window
                    elif self.y + self.brush.height() - self.brushSpeed > self.imageTools.size().height():
                        self.y = self.imageTools.size().height() - self.brush.height()
                        self.brushSpeed = -self.brushSpeed
                    else:
                        self.y -= self.brushSpeed
                
                elif event.key() == Qt.Key_Down:
                    # Check if the brush will go beyond the bottom of the window
                    if self.y + self.brush.height() + self.brushSpeed > self.imageTools.size().height():
                        self.y = self.imageTools.size().height() - self.brush.height()
                        self.brushSpeed = -self.brushSpeed
                    # Check if the brush will go beyond the toolbar at the top of the window
                    elif self.y + self.brushSpeed < self.brush.height():
                        self.y = self.brush.height()
                        self.brushSpeed = -self.brushSpeed
                    else:
                        self.y += self.brushSpeed
                
                elif event.key() == Qt.Key_Left:
                    # Check if the brush will go beyond the toolbar on the left
                    if self.x - self.brushSpeed < 0 + self.brush.width():
                        self.x = 0 + self.brush.width()
                        self.brushSpeed = -self.brushSpeed
                    # Check if the brush will go beyond the right side of the window
                    elif self.x + self.brush.width() - self.brushSpeed > self.imageTools.size().width():
                        self.x = self.imageTools.size().width() - self.brush.width()
                        self.brushSpeed = -self.brushSpeed
                    else:
                        self.x -= self.brushSpeed
                
                elif event.key() == Qt.Key_Right:
                    # Check if the brush will go beyond the right side of the window
                    if self.x + self.brush.width() + self.brushSpeed > self.imageTools.size().width():
                        self.x = self.imageTools.size().width() - self.brush.width()
                        self.brushSpeed = -self.brushSpeed
                    # Check if the brush will go beyond the toolbar on the left
                    elif self.x + self.brushSpeed < 0 + self.brush.width():
                        self.x = 0 + self.brush.width()
                        self.brushSpeed = -self.brushSpeed
                    else:
                        self.x += self.brushSpeed
                
                elif event.key() == Qt.Key_W:
                    # Check if the brush will go beyond the right side of the window
                    if self.x + self.brush.width() + deltaX > self.imageTools.size().width():
                        self.x = self.imageTools.size().width() - self.brush.width()
                        deltaX = -deltaX
                    # Check if the brush will go beyond the toolbar on the left
                    elif self.x + deltaX < 0 + self.brush.width():
                        self.x = 0 + self.brush.width()
                        deltaX = -deltaX
                    else:
                        self.x += deltaX

                    # Check if the brush will go beyond the toolbar at the top of the window
                    if self.y - deltaY < self.brush.height():
                        self.y = self.brush.height()
                        deltaY = -deltaY
                    # Check if the brush will go beyond the the bottom of the window
                    elif self.y + self.brush.height() - deltaY > self.imageTools.size().height():
                        self.y = self.imageTools.size().height() - self.brush.height()
                        deltaY = -deltaY
                    else:
                        self.y -= deltaY

                # If the spray paint option is chosen it overrides the line style
                if self.brushStyle == BrushStyle.SPRAYPAINT:
                    # Set the pen of the painter
                    self.painter.setPen(QPen(self.brushColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

                    # Draw the spray
                    for n in range(100):
                        xo = random.gauss(0, self.brush.width())
                        yo = random.gauss(0, self.brush.width())
                        self.painter.drawPoint(int(self.x + xo), int(self.y + yo))

                elif self.brushStyle == BrushStyle.GRAFFITI:
                    # Set the pen of the painter
                    self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    
                    # Draw line from the last point of cursor to the current point
                    self.painter.drawLine(self.lastPoint, QPointF(self.x, self.y))

                    # Draw the spray
                    self.painter.setPen(QPen(self.brushColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

                    for n in range(500):
                        xo = random.gauss(0, self.brush.width())
                        yo = random.gauss(0, self.brush.width())
                        self.painter.drawPoint(int(self.x + xo), int(self.y + yo))

                    # Draw the drip
                    self.painter.setPen(QPen(self.brushColor, self.brushSize//4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

                    drip = random.random()
                    if drip > 0.40 and math.sqrt(yo**2 + xo**2) < self.brush.size().width():
                        self.painter.drawLine(QPointF(int(self.x + xo), int(self.y + yo)), QPointF(int(self.x + xo), int(self.y + yo + 100*random.random())))

                elif self.brushStyle == BrushStyle.SPLATTER:
                    # Set the pen of the painter
                    self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    
                    # Draw line from the last point of cursor to the current point
                    self.painter.drawLine(self.lastPoint, QPointF(self.x, self.y))

                    for n in range(20):
                        xo = random.gauss(0, self.brush.width()*2)
                        yo = random.gauss(0, self.brush.width()*2)
                        self.painter.drawPoint(int(self.x + xo), int(self.y + yo))

                elif self.brushStyle == BrushStyle.ABSTRACT:
                    # Draw the random points
                    for n in range(10*self.brushSize):
                        xo = random.gauss(0, self.brush.width()*2)
                        yo = random.gauss(0, self.brush.width()*2)

                        splatterSize = 1/math.sqrt(xo**2 + yo**2)*5
                        self.painter.setPen(QPen(self.brushColor, splatterSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                        self.painter.drawPoint(int(self.x + xo), int(self.y + yo))


                elif self.lineStyle == LineStyle.DOTTED:
                    # Set the pen of the painter
                    self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    
                    # Draw a point around the current brush position
                    self.painter.drawPoint(QPointF(self.x, self.y))

                else:
                    # Set the pen of the painter
                    self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                            
                    # Draw line from the last point of cursor to the current point
                    self.painter.drawLine(self.lastPoint, QPointF(self.x, self.y))
                    
                self.update()

                # Add a pause so the animation is visible
                QTest.qWait(15)

        if self.painter.isActive():
            self.painter.end()
 

    def paintEvent(self, event):
        # create a canvas
        canvasPainter = QPainter(self)
         
        # Draw the canvas on the window
        rect = self.rect()
        canvasRect = QRect(rect.x() + 400, rect.y() + 30, rect.width() - 400, rect.height() - 30) # 30px is the height of the menu bar, 400px is the size of the toolbar on the left
        canvasPainter.drawImage(canvasRect, self.image, self.image.rect())

        # Draw the direction animation
        self.clock.draw(canvasPainter, self.theta, self.brushColor)

        canvasPainter.drawImage(canvasRect, self.imageTools, self.image.rect())

        canvasPainter.end()

        # Create the canvas to draw the tools on. This is overlayed on top of the painting
        toolPainter = QPainter(self.imageTools)

        self.imageTools.fill(QColor(255, 255, 255, 0))

        toolPainter.setPen(QPen(Qt.black, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        # Draw the animation around the brush
        x2 = math.sin(2*math.pi*self.theta/360)*self.brushSize*2
        y2 = math.cos(2*math.pi*self.theta/360)*self.brushSize*2
        toolPainter.drawLine(QLineF(self.x + x2, self.y - y2, self.x + 2*x2, self.y - 2*y2))

        # Draw the brush 
        if self.blink:
            toolPainter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            brush = QBrush()
            brush.setColor(QColor(self.brushColor))
            brush.setStyle(Qt.SolidPattern)
            toolPainter.setBrush(brush)
            self.brush.moveCenter(QPointF(self.x, self.y))
            toolPainter.drawEllipse(self.brush)

 
    # Handle the save canvas action
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                          "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        if filePath == "":
            return
        self.image.save(filePath)
 
    # Handle the clear canvas action
    def clear(self):
        self.image.fill(Qt.white)
        self.update()
 
    # Handle the brush size actions
    def Pixel_12(self):
        self.brushSize = 12
        self.brush.setWidth(self.brushSize/2)
        self.brush.setHeight(self.brushSize/2)
        self.adjustSpeed()
        self.disableSelection(self.bSizeMenu, "12px")
 
    def Pixel_16(self):
        self.brushSize = 16
        self.brush.setWidth(self.brushSize/2)
        self.brush.setHeight(self.brushSize/2)
        self.adjustSpeed()
        self.disableSelection(self.bSizeMenu, "16px")
 
    def Pixel_20(self):
        self.brushSize = 20
        self.brush.setWidth(self.brushSize/2)
        self.brush.setHeight(self.brushSize/2)
        self.adjustSpeed()
        self.disableSelection(self.bSizeMenu, "20px")
 
    def Pixel_24(self):
        self.brushSize = 24
        self.brush.setWidth(self.brushSize/2)
        self.brush.setHeight(self.brushSize/2)
        self.adjustSpeed()
        self.disableSelection(self.bSizeMenu, "24px")

    def adjustSpeed(self):
        for action in self.bSpeedMenu.actions():
            if not action.isEnabled() and action.text() == "Slow":
                self.bSlow()
            elif not action.isEnabled() and action.text() == "Medium":
                self.bMedium()
            elif not action.isEnabled() and action.text() == "Fast":
                self.bMedium()
 
    # Handle the brush colour actions
    def blackColor(self):
        self.brushColor = QColor(0, 0, 0, self.alpha)
        self.rainbow = False
        self.disableSelection(self.bColorMenu, "Black")
 
    def whiteColor(self):
        self.brushColor = QColor(255, 255, 255, self.alpha)
        self.rainbow = False
        self.disableSelection(self.bColorMenu, "White")

    def redColor(self):
        self.brushColor = QColor(255, 0, 0, self.alpha)
        self.rainbow = False
        self.disableSelection(self.bColorMenu, "Red")

    def orangeColor(self):
        self.brushColor = QColor(255, 127, 0, self.alpha)
        self.rainbow = False
        self.disableSelection(self.bColorMenu, "Orange")

    def yellowColor(self):
        self.brushColor = QColor(255, 255, 0, self.alpha)
        self.rainbow = False
        self.disableSelection(self.bColorMenu, "Yellow")
 
    def greenColor(self):
        self.brushColor = QColor(0, 255, 0, self.alpha)
        self.rainbow = False
        self.disableSelection(self.bColorMenu, "Green")

    def blueColor(self):
        self.brushColor = QColor(0, 0, 255, self.alpha)
        self.rainbow = False
        self.disableSelection(self.bColorMenu, "Blue")

    def purpleColor(self):
        self.brushColor = QColor(127, 0, 255, self.alpha)
        self.rainbow = False
        self.disableSelection(self.bColorMenu, "Purple")

    def pinkColor(self):
        self.brushColor = QColor(255, 0, 127, self.alpha)
        self.rainbow = False
        self.disableSelection(self.bColorMenu, "Pink")

    def rainbowColor(self):
        self.brushColor = QColor(255, 0, 0, self.alpha)
        self.rainbow = True
        self.disableSelection(self.bColorMenu, "Rainbow")

    def updateColor(self):
        if self.rainbow:
            self.brushColor.setHsl((self.brushColor.hue() + 1) % 360, self.brushColor.saturation(), self.brushColor.lightness())
            self.brushColor.setAlpha(self.alpha)

    def customColor(self):
        self.brushColor = QColorDialog.getColor()
        self.rainbow = False

        # Set the icon of the custom color to the selected color
        color = QPixmap(50, 50)
        color.fill(self.brushColor)

        for action in self.bColorMenu.actions():
            if action.text() == "Custom":
                action.setIcon(QIcon(color))

        self.disableSelection(self.bColorMenu, "")

    # Handle the brush style actions
    def marker(self):
        self.alpha = 255
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
        self.brushStyle = BrushStyle.MARKER
        self.disableSelection(self.bStyleMenu, "Marker")
    
    def watercolor(self):
        self.alpha = 50
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
        self.brushStyle = BrushStyle.WATERCOLOR
        self.disableSelection(self.bStyleMenu, "Watercolor")

    def sprayPaint(self):
        self.brushStyle = BrushStyle.SPRAYPAINT
        self.disableSelection(self.bStyleMenu, "Spray Paint")

    def graffiti(self):
        self.brushStyle = BrushStyle.GRAFFITI
        self.disableSelection(self.bStyleMenu, "Graffiti")

    def splatter(self):
        self.brushStyle = BrushStyle.SPLATTER
        self.disableSelection(self.bStyleMenu, "Splatter")

    def abstract(self):
        self.brushStyle = BrushStyle.ABSTRACT
        self.disableSelection(self.bStyleMenu, "Abstract")

    # Handle the brush speed actions
    def bSlow(self):
        self.brushSpeed = 1*(self.brushSize/2)
        self.disableSelection(self.bSpeedMenu, "Slow")

    def bMedium(self):
        self.brushSpeed = 2*(self.brushSize/2)
        self.disableSelection(self.bSpeedMenu, "Medium")

    def bFast(self):
        self.brushSpeed = 5*(self.brushSize/2)
        self.disableSelection(self.bSpeedMenu, "Fast")

    # Handle the line style actions
    def solid(self):
        self.lineStyle = LineStyle.SOLID
        self.disableSelection(self.lStyleMenu, "Solid")

    def dotted(self):
        self.lineStyle = LineStyle.DOTTED
        self.disableSelection(self.lStyleMenu, "Dotted")

    # Handle the mode actions
    def freestyle(self):
        self.mode = Mode.FREESTYLE
        self.disableSelection(self.modeMenu, "Freestyle")

    def game(self):
        self.mode = Mode.GAME
        self.disableSelection(self.modeMenu, "Game")

    # Handle the clock speed actions
    def stopClock(self):
        self.step = 0
        self.disableSelection(self.clockSpeedMenu, "Stop")

    def cSlow(self):
        self.step = 0.5
        self.disableSelection(self.clockSpeedMenu, "Slow")

    def cMedium(self):
        self.step = 1
        self.disableSelection(self.clockSpeedMenu, "Medium")

    def cFast(self):
        self.step = 2
        self.disableSelection(self.clockSpeedMenu, "Fast")

    # Handle the feedback actions
    def feedbackOn(self):
        self.feedback = True
        self.disableSelection(self.feedbackMenu, "On")

    def feedbackOff(self):
        self.feedback = False
        self.disableSelection(self.feedbackMenu, "Off")

    # Updates the angle of the clock arm
    def updateAngle(self):
        self.theta = (self.theta + self.step) % 360
        self.update()

    def blinkBrush(self):
        if self.blink == True:
            self.blink = False
        else:
            self.blink = True

    def disableSelection(self, menu, actionName):
        for action in menu.actions():
            action.setDisabled(False)

            if action.text() == actionName:
                action.setDisabled(True)
 
 
 
# create pyqt5 app
App = QApplication(sys.argv)
 
# create the instance of our Window
window = Window()
 
# showing the window
window.show()
 
# start the app
sys.exit(App.exec())
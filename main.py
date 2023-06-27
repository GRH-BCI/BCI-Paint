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
        screen_size = self.size()
        canvas_size = QSize(screen_size.width() - 400, screen_size.height() -30)
        self.image = QImage(canvas_size, QImage.Format_RGB32)
 
        # Fill the canvas with white
        self.image.fill(Qt.white)

        # Create an image to draw the tools overtop of the painting but not included in the painting
        self.image_tools = QImage(canvas_size, QImage.Format_ARGB32)
        self.image_tools.fill(QColor(255, 255, 255, 0))

        # Initialize the angle for arrow and the rate of change of the angle
        self.theta = 0
        self.step = 1

        # Set the timer for the angle of the clock arm
        self.angle_timer = QTimer(self, interval=100)
        self.angle_timer.timeout.connect(self.update_angle)
        self.angle_timer.start()

        # Initialize the rainbow colour to off and start the rainbow timer
        self.rainbow = False

        self.rainbow_timer = QTimer(self, interval=10)
        self.rainbow_timer.timeout.connect(self.update_color)
        self.rainbow_timer.start()

        # Set the timer for the blink of the brush
        self.blink = True

        self.blink_timer = QTimer(self, interval=1000)
        self.blink_timer.timeout.connect(self.blink_brush)
        self.blink_timer.start()

        # Initialize the mode to freestyle
        self.mode = Mode.FREESTYLE

        self.feedback = False
 
        # Initial brush size
        self.brushSize = 12
        # Initail brush color
        self.brushColor = QColor(0, 0, 0)
        # Initial transparancy value
        self.alpha = 255
        # Initial line style
        self.lineStyle = Qt.SolidLine
        # Initialize the spray paint settings
        self.spray = False

        # Creating the brush
        self.brush = QRectF(0, 0, self.brushSize/2, self.brushSize/2)
        self.brush_speed = self.brushSize/2

        # Initializing the position of the brush
        self.x = self.size().width() // 2
        self.y = self.size().height() // 2

        # Creating the clock animation
        self.clock =  Clock(25, 50, 350)
 
        # QPoint object to tract the point
        self.lastPoint = QPointF()

        # Painter that draws the brush lines on the canvas
        self.painter = QPainter(self.image)

        # Creating the menu bar
        create_menu(self)
        

    def keyPressEvent(self, event):
        # If the painter is interrupted, restart the painter
        if self.painter.isActive():
            self.painter.end()
        
        # Creating painter object
        self.painter = QPainter(self.image)
            
        # Set the pen of the painter
        self.painter.setPen(QPen(self.brushColor, self.brushSize, self.lineStyle, Qt.RoundCap, Qt.RoundJoin))

        if self.mode == Mode.FREESTYLE:
            self.brush_speed = abs(self.brush_speed)
            
            # Change the last point
            self.lastPoint = QPointF(self.x, self.y)

            # Allow the brush to move with the arrow keys or the w key and the clock animation
            if event.key() == Qt.Key_Up:
                # Check if the brush will go beyond the toolbar at the top of the window
                if self.y - self.brush_speed < self.brush.height():
                    self.y = self.brush.height()
                else:
                    self.y -= self.brush_speed
            
            elif event.key() == Qt.Key_Down:
                # Check if the brush will go beyond the bottom of the window
                if self.y + self.brush.height() + self.brush_speed > self.image_tools.size().height():
                    self.y = self.image_tools.size().height() - self.brush.height()
                else:
                    self.y += self.brush_speed
            
            elif event.key() == Qt.Key_Left:
                # Check if the brush will go beyond the toolbar on the left
                if self.x - self.brush_speed < 0 + self.brush.width():
                    self.x = 0 + self.brush.width()
                else:
                    self.x -= self.brush_speed
            
            elif event.key() == Qt.Key_Right:
                # Check if the brush will go beyond the right side of the window
                if self.x + self.brush.width() + self.brush_speed > self.image_tools.size().width():
                    self.x = self.image_tools.size().width() - self.brush.width()//2
                else:
                    self.x += self.brush_speed
            
            elif event.key() == Qt.Key_W:
                # calculate the change in the x and y direction based on the angle
                delta_x = math.sin(2*math.pi*self.theta/360)*self.brush_speed
                delta_y = math.cos(2*math.pi*self.theta/360)*self.brush_speed
                
                # Check if the brush will go beyond the right side of the window
                if self.x + self.brush.width() + delta_x > self.image_tools.size().width():
                    self.x = self.image_tools.size().width() - self.brush.width()
                # Check if the brush will go beyond the toolbar on the left
                elif self.x + delta_x < 0 + self.brush.width():
                    self.x = 0 + self.brush.width()
                else:
                    self.x += delta_x

                # Check if the brush will go beyond the toolbar at the top of the window
                if self.y - delta_y < self.brush.height():
                    self.y = self.brush.height()
                # Check if the brush will go beyond the the bottom of the window
                elif self.y + self.brush.height() - delta_y > self.image_tools.size().height():
                    self.y = self.image_tools.size().height() - self.brush.height()
                else:
                    self.y -= delta_y
                
            if self.spray:
                # set the pen of the painter
                self.painter.setPen(QPen(self.brushColor, 1, self.lineStyle, Qt.RoundCap, Qt.RoundJoin))

                # Draw the spray
                for n in range(100):
                    xo = random.gauss(0, self.brush.width())
                    yo = random.gauss(0, self.brush.width())
                    self.painter.drawPoint(int(self.x + xo), int(self.y + yo))
            else:
                # set the pen of the painter
                self.painter.setPen(QPen(self.brushColor, self.brushSize, self.lineStyle, Qt.RoundCap, Qt.RoundJoin))
                
                # draw line from the last point of cursor to the current point
                self.painter.drawLine(self.lastPoint, QPointF(self.x, self.y))
            
            self.update()

        elif self.mode == Mode.GAME:
            # Calculate the change in the x and y direction based on the angle
            delta_x = math.sin(2*math.pi*self.theta/360)*self.brush_speed
            delta_y = math.cos(2*math.pi*self.theta/360)*self.brush_speed

            self.brush_speed = abs(self.brush_speed)

            for i in range(0, 300):
                if self.painter.isActive() == False:
                    break

                # Slow the brush down over time
                if i > 150:
                    delta_y = delta_y*0.99
                    delta_x = delta_x*0.99
    
                # Change the last point
                self.lastPoint = QPointF(self.x, self.y)

                # Allow the brush to move with the arrow keys or the w key and the clock animation
                if event.key() == Qt.Key_Up:
                    # Check if the brush will go beyond the toolbar at the top of the window
                    if self.y - self.brush_speed < self.brush.height():
                        self.y = self.brush.height()
                        self.brush_speed = -self.brush_speed
                    # Check if the brush will go beyond the bottom of the window
                    elif self.y + self.brush.height() - self.brush_speed > self.image_tools.size().height():
                        self.y = self.image_tools.size().height() - self.brush.height()
                        self.brush_speed = -self.brush_speed
                    else:
                        self.y -= self.brush_speed
                
                elif event.key() == Qt.Key_Down:
                    # Check if the brush will go beyond the bottom of the window
                    if self.y + self.brush.height() + self.brush_speed > self.image_tools.size().height():
                        self.y = self.image_tools.size().height() - self.brush.height()
                        self.brush_speed = -self.brush_speed
                    # Check if the brush will go beyond the toolbar at the top of the window
                    elif self.y + self.brush_speed < self.brush.height():
                        self.y = self.brush.height()
                        self.brush_speed = -self.brush_speed
                    else:
                        self.y += self.brush_speed
                
                elif event.key() == Qt.Key_Left:
                    # Check if the brush will go beyond the toolbar on the left
                    if self.x - self.brush_speed < 0 + self.brush.width():
                        self.x = 0 + self.brush.width()
                        self.brush_speed = -self.brush_speed
                    # Check if the brush will go beyond the right side of the window
                    elif self.x + self.brush.width() - self.brush_speed > self.image_tools.size().width():
                        self.x = self.image_tools.size().width() - self.brush.width()
                        self.brush_speed = -self.brush_speed
                    else:
                        self.x -= self.brush_speed
                
                elif event.key() == Qt.Key_Right:
                    # Check if the brush will go beyond the right side of the window
                    if self.x + self.brush.width() + self.brush_speed > self.image_tools.size().width():
                        self.x = self.image_tools.size().width() - self.brush.width()
                        self.brush_speed = -self.brush_speed
                    # Check if the brush will go beyond the toolbar on the left
                    elif self.x + self.brush_speed < 0 + self.brush.width():
                        self.x = 0 + self.brush.width()
                        self.brush_speed = -self.brush_speed
                    else:
                        self.x += self.brush_speed
                
                elif event.key() == Qt.Key_W:
                    # Check if the brush will go beyond the right side of the window
                    if self.x + self.brush.width() + delta_x > self.image_tools.size().width():
                        self.x = self.image_tools.size().width() - self.brush.width()
                        delta_x = -delta_x
                    # Check if the brush will go beyond the toolbar on the left
                    elif self.x + delta_x < 0 + self.brush.width():
                        self.x = 0 + self.brush.width()
                        delta_x = -delta_x
                    else:
                        self.x += delta_x

                    # Check if the brush will go beyond the toolbar at the top of the window
                    if self.y - delta_y < self.brush.height():
                        self.y = self.brush.height()
                        delta_y = -delta_y
                    # Check if the brush will go beyond the the bottom of the window
                    elif self.y + self.brush.height() - delta_y > self.image_tools.size().height():
                        self.y = self.image_tools.size().height() - self.brush.height()
                        delta_y = -delta_y
                    else:
                        self.y -= delta_y

                if self.spray:
                    # Set the pen of the painter
                    self.painter.setPen(QPen(self.brushColor, 1, self.lineStyle, Qt.RoundCap, Qt.RoundJoin))

                    # Draw the spray
                    for n in range(100):
                        xo = random.gauss(0, self.brush.width())
                        yo = random.gauss(0, self.brush.width())
                        self.painter.drawPoint(int(self.x + xo), int(self.y + yo))
                else:
                    # Set the pen of the painter
                    self.painter.setPen(QPen(self.brushColor, self.brushSize, self.lineStyle, Qt.RoundCap, Qt.RoundJoin))
                            
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
        new_rect = QRect(rect.x() + 400, rect.y() + 30, rect.width() - 400, rect.height() - 30) # 30px is the height of the menu bar, 400px is the size of the toolbar on the left
        canvasPainter.drawImage(new_rect, self.image, self.image.rect())

        # Draw the direction animation
        self.clock.draw(canvasPainter, self.theta, self.brushColor)

        canvasPainter.drawImage(new_rect, self.image_tools, self.image.rect())

        canvasPainter.end()

        # Create the canvas to draw the tools on. This is overlayed on top of the painting
        toolPainter = QPainter(self.image_tools)

        self.image_tools.fill(QColor(255, 255, 255, 0))

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
 
    def Pixel_16(self):
        self.brushSize = 16
        self.brush.setWidth(self.brushSize/2)
        self.brush.setHeight(self.brushSize/2)
 
    def Pixel_20(self):
        self.brushSize = 20
        self.brush.setWidth(self.brushSize/2)
        self.brush.setHeight(self.brushSize/2)
 
    def Pixel_24(self):
        self.brushSize = 24
        self.brush.setWidth(self.brushSize/2)
        self.brush.setHeight(self.brushSize/2)
 
    # Handle the brush colour actions
    def blackColor(self):
        self.brushColor = QColor(0, 0, 0, self.alpha)
        self.rainbow = False
 
    def whiteColor(self):
        self.brushColor = QColor(255, 255, 255, self.alpha)
        self.rainbow = False

    def redColor(self):
        self.brushColor = QColor(255, 0, 0, self.alpha)
        self.rainbow = False

    def orangeColor(self):
        self.brushColor = QColor(255, 127, 0, self.alpha)
        self.rainbow = False

    def yellowColor(self):
        self.brushColor = QColor(255, 255, 0, self.alpha)
        self.rainbow = False
 
    def greenColor(self):
        self.brushColor = QColor(0, 255, 0, self.alpha)
        self.rainbow = False

    def blueColor(self):
        self.brushColor = QColor(0, 0, 255, self.alpha)
        self.rainbow = False

    def purpleColor(self):
        self.brushColor = QColor(127, 0, 255, self.alpha)
        self.rainbow = False

    def pinkColor(self):
        self.brushColor = QColor(255, 0, 127, self.alpha)
        self.rainbow = False

    def rainbowColor(self):
        self.brushColor = QColor(255, 0, 0, self.alpha)
        self.rainbow = True

    def update_color(self):
        if self.rainbow:
            self.brushColor.setHsl((self.brushColor.hue() + 1) % 360, self.brushColor.saturation(), self.brushColor.lightness())
            self.brushColor.setAlpha(self.alpha)

    def customColor(self):
        self.brushColor = QColorDialog.getColor()
        self.rainbow = False

    # Handle the brush style actions
    def watercolor(self):
        self.alpha = 50
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
        self.spray = False

    def marker(self):
        self.alpha = 255
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
        self.spray = False

    def spray_paint(self):
        self.spray = True

    # Handle the brush speed actions
    def b_slow(self):
        self.brush_speed = 1*(self.brushSize/2)

    def b_medium(self):
        self.brush_speed = 2*(self.brushSize/2)

    def b_fast(self):
        self.brush_speed = 5*(self.brushSize/2)

    # Handle the linestyle actions
    def solid(self):
        self.lineStyle = Qt.SolidLine

    def dotted(self):
        self.lineStyle = Qt.DotLine

    # Handle the mode actions
    def freestyle(self):
        self.mode = Mode.FREESTYLE

    def game(self):
        self.mode = Mode.GAME

    # Handle the clock speed actions
    def stop_clock(self):
        self.step = 0

    def c_slow(self):
        self.step = 0.5

    def c_medium(self):
        self.step = 1

    def c_fast(self):
        self.step = 2

    # Handle the feedback actions
    def feedback_on(self):
        self.feedback = True

    def feedback_off(self):
        self.feedback = False

    # Updates the angle of the clock arm
    def update_angle(self):
        self.theta = (self.theta + self.step) % 360
        self.update()

    def blink_brush(self):
        if self.blink == True:
            self.blink = False
        else:
            self.blink = True
 
 
 
# create pyqt5 app
App = QApplication(sys.argv)
 
# create the instance of our Window
window = Window()
 
# showing the window
window.show()
 
# start the app
sys.exit(App.exec())
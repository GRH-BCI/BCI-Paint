from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
import sys
import math
import os
import ctypes
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
        self.backgroundColor = Qt.white
        self.image.fill(self.backgroundColor)

        # Create an image to draw the tools overtop of the painting but not included in the painting
        self.imageTools = QImage(canvasSize, QImage.Format_ARGB32)
        self.imageTools.fill(QColor(255, 255, 255, 0))
        self.toolColor = Qt.black

        # Initialize the angle for arrow and the rate of change of the angle
        self.theta = 0
        self.step = 1

        # Set the timer for the angle of the clock arm
        self.angleTimer = QTimer(self, interval=100)
        self.angleTimer.timeout.connect(self.updateAngle)
        self.angleTimer.start()

        # Initialize the type of color
        self.specialtyColor = SpecialtyColor.REGULAR

        # Indicates whether a texture image has been created with the color or if it is new
        self.newColor = True

        self.rainbowTimer = QTimer(self, interval=10)
        self.rainbowTimer.timeout.connect(self.updateColor)
        self.rainbowTimer.start()

        # Initialize the texture of the brush
        self.texture = Texture.NULL

        # Set the timer for the blink of the brush
        self.blink = True

        self.blinkTimer = QTimer(self, interval=1000)
        self.blinkTimer.timeout.connect(self.blinkBrush)
        self.blinkTimer.start()

        # Set the timer for allow key presses
        self.allowKey = True
        # Counts the number of key presses currently being handled
        self.keyCount = 0

        self.allowKeyTimer = QTimer(self, interval=1)
        self.allowKeyTimer.timeout.connect(self.allowKeyPress)
        self.allowKeyTimer.start()

        # Initialize the BCI key used
        self.BCIKey = Qt.Key_W

        # Initialize the mode to freestyle
        self.mode = Mode.FREESTYLE

        # Set up the sticker placements (rows, columns, and coordinates allow for future flexibilty)
        self.StickerIndices = ["number-1.png", "number-2.png", "number-3.png", "number-4", "number-5.png", "number-6.png", "number-7.png", "number-8.png", "number-9.png"]
        self.stickerCoordinates = []
        self.stickerRows = 3
        self.stickerColumns = 3
        self.currentStickerIndex = 0

        self.stickerTimer = QTimer(self, interval=3000)
        self.stickerTimer.timeout.connect(self.incrementStickerIndex)
        self.stickerTimer.start()

        # Initialize feedback mode using the power level to off
        self.feedback = False
 
        # Initial brush size
        self.brushSize = 20
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
 
        # QPoint object to track the point
        self.lastPoint = QPointF()

        # Painter that draws the brush lines on the canvas
        self.painter = QPainter(self.image)

        # Creating the menu bar
        createMenu(self)
        

    def keyPressEvent(self, event):
        # Allows 50 key presses to be handled at one time. If the keyPressEvent is interrupted by another keyPressEvent,
        # the current state is saved on the stack. Max 50 states can be saved at a time before they have to be resovled
        # to prevent a stack overflow error.
        if self.allowKey and self.keyCount < 50:
            self.keyCount += 1
            self.allowKey = False
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

                # Calculate the change in the x and y direction based on the angle
                deltaX = math.sin(2*math.pi*self.theta/360)*self.brushSpeed
                deltaY = math.cos(2*math.pi*self.theta/360)*self.brushSpeed

                handleBrushMovement(self, event, deltaX, deltaY)

                drawStroke(self)
                
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

                    deltaX, deltaY = handleBrushMovement(self, event, deltaX, deltaY)

                    drawStroke(self)
                    
                    self.update()

                    # Add a pause so the animation is visible
                    QTest.qWait(15)
            elif self.mode == Mode.STICKER:
                self.stickerTimer.stop()

                # Get the image from the user
                filename=None

                if not filename:
                    filename, _ = QFileDialog.getOpenFileName(self, 'Select Sticker' , QDir.currentPath(), 'Images (*.png *.jpg)')
                if not filename:
                    self.stickerTimer.start()
                    return
                
                pixmap = QPixmap(filename)

                # Scale the picture to the size of the grid cell if it is larger
                if (pixmap.height() > self.image.height() // self.stickerRows):
                    pixmap = pixmap.scaledToHeight(self.image.height() // self.stickerRows)
                if (pixmap.width() > self.image.width() // self.stickerColumns):
                    pixmap = pixmap.scaledToWidth(self.image.width() // self.stickerColumns)

                # Set the coordinates of the picture to be centered in the grid cell
                x = self.stickerCoordinates[self.currentStickerIndex][0] - pixmap.width() // 2
                y = self.stickerCoordinates[self.currentStickerIndex][1] - pixmap.height() // 2

                self.painter.drawPixmap(x, y, pixmap)

                # Reset the timer
                self.stickerTimer.start()

            # When the key press action finishes subtract 1 from the total currently active key presses being handled
            self.keyCount -= 1

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

        toolPainter.setPen(QPen(self.toolColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        if self.mode == Mode.STICKER:
            # Cacluate positions to draw stickers based on the number of rows and columns
            self.stickerCoordinates = []
            for i in range(0, self.stickerRows):
                for j in range(0, self.stickerColumns):
                    x = (self.image.width() // self.stickerColumns) * j + (self.image.width() // self.stickerColumns) // 2
                    y = (self.image.height() // self.stickerRows) * i + (self.image.height() // self.stickerRows) // 2
                    self.stickerCoordinates.append([x, y])

            index = 0
            for number in self.StickerIndices:
                pixmap = QPixmap(os.path.join("Assets", number))

                # Set the size of the number icon according to whether it is highlighted or not
                if (index == self.currentStickerIndex):
                    pixels = 128
                else:
                    pixels = 64
                pixmap = pixmap.scaledToHeight(pixels)

                toolPainter.drawPixmap(self.stickerCoordinates[index][0] - pixmap.width() // 2, self.stickerCoordinates[index][1] - pixmap.height() // 2, pixmap)

                index += 1
        else:
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
        self.image.fill(self.backgroundColor)
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
        self.specialtyColor = SpecialtyColor.REGULAR
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Black")
 
    def whiteColor(self):
        self.brushColor = QColor(255, 255, 255, self.alpha)
        self.specialtyColor = SpecialtyColor.REGULAR
        self.newColor = True
        self.disableSelection(self.bColorMenu, "White")

    def redColor(self):
        self.brushColor = QColor(255, 0, 0, self.alpha)
        self.specialtyColor = SpecialtyColor.REGULAR
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Red")

    def orangeColor(self):
        self.brushColor = QColor(255, 127, 0, self.alpha)
        self.specialtyColor = SpecialtyColor.REGULAR
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Orange")

    def yellowColor(self):
        self.brushColor = QColor(255, 255, 0, self.alpha)
        self.specialtyColor = SpecialtyColor.REGULAR
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Yellow")
 
    def greenColor(self):
        self.brushColor = QColor(0, 255, 0, self.alpha)
        self.specialtyColor = SpecialtyColor.REGULAR
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Green")

    def blueColor(self):
        self.brushColor = QColor(0, 0, 255, self.alpha)
        self.specialtyColor = SpecialtyColor.REGULAR
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Blue")

    def purpleColor(self):
        self.brushColor = QColor(127, 0, 255, self.alpha)
        self.specialtyColor = SpecialtyColor.REGULAR
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Purple")

    def pinkColor(self):
        self.brushColor = QColor(255, 0, 127, self.alpha)
        self.specialtyColor = SpecialtyColor.REGULAR
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Pink")

    def goldColor(self):
        self.specialtyColor = SpecialtyColor.GOLD
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Gold")

    def silverColor(self):
        self.specialtyColor = SpecialtyColor.SILVER
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Silver")

    def rainbowColor(self):
        self.brushColor = QColor(255, 0, 0, self.alpha)
        self.specialtyColor = SpecialtyColor.RAINBOW
        self.newColor = True
        self.disableSelection(self.bColorMenu, "Rainbow")

    def updateColor(self):
        if self.specialtyColor == SpecialtyColor.RAINBOW:
            self.brushColor.setHsl((self.brushColor.hue() + 1) % 360, self.brushColor.saturation(), self.brushColor.lightness())
            self.brushColor.setAlpha(self.alpha)
            self.newColor = True

    def customColor(self):
        color = QColorDialog.getColor(initial=self.brushColor)

        if color.isValid():
            self.brushColor = QColor(color.red(), color.green(), color.blue(), self.alpha)
            self.specialtyColor = SpecialtyColor.REGULAR
            self.newColor = True

            # Set the icon of the custom color to the selected color
            colorIcon = QPixmap(50, 50)
            colorIcon.fill(color)

            for action in self.bColorMenu.actions():
                if action.text() == "Custom":
                    action.setIcon(QIcon(colorIcon))

            self.disableSelection(self.bColorMenu, "")

    
    # Handle the texture type actions
    def noTexture(self):
        self.texture = Texture.NULL
        self.disableSelection(self.bTextureMenu, "None")

    def metallicTexture(self):
        self.texture = Texture.METALLIC
        self.disableSelection(self.bTextureMenu, "Metallic")


    # Handle the paint type actions
    def acrylic(self):
        self.alpha = 255
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
        self.disableSelection(self.bPaintTypeMenu, "Acrylic")

    def watercolor(self):
        self.alpha = 50
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
        self.disableSelection(self.bPaintTypeMenu, "Watercolor")

    # Handle the brush style actions
    def marker(self):
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
        self.brushStyle = BrushStyle.MARKER
        self.disableSelection(self.bStyleMenu, "Marker")

    def sprayPaint(self):
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
        self.brushStyle = BrushStyle.SPRAYPAINT
        self.disableSelection(self.bStyleMenu, "Spray Paint")

    def graffiti(self):
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
        self.brushStyle = BrushStyle.GRAFFITI
        self.disableSelection(self.bStyleMenu, "Graffiti")

    def splatter(self):
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
        self.brushStyle = BrushStyle.SPLATTER
        self.disableSelection(self.bStyleMenu, "Splatter")

    def abstract(self):
        self.brushColor = QColor(self.brushColor.red(), self.brushColor.green(), self.brushColor.blue(), self.alpha)
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

    # Handle the background actions
    def whiteBackground(self):
        self.backgroundColor = Qt.white
        self.image.fill(self.backgroundColor)
        self.toolColor = Qt.black
        self.disableSelection(self.backgroundMenu, "White")

    def blackBackground(self):
        self.backgroundColor = Qt.black
        self.image.fill(self.backgroundColor)
        self.toolColor = Qt.white
        self.disableSelection(self.backgroundMenu, "Black")

    def customBackground(self):
        color = QColorDialog.getColor(initial=Qt.white)

        if color.isValid():
            self.backgroundColor = QColor(color.red(), color.green(), color.blue(), self.alpha)
            self.image.fill(self.backgroundColor)

            if (color.lightness() < 128):
                self.toolColor = Qt.white
            else:
                self.toolColor = Qt.black

            # Set the icon of the custom color to the selected color
            colorIcon = QPixmap(50, 50)
            colorIcon.fill(color)

            for action in self.backgroundMenu.actions():
                if action.text() == "Custom":
                    action.setIcon(QIcon(colorIcon))

            self.disableSelection(self.backgroundMenu, "")

    # Handle the mode actions
    def freestyle(self):
        self.mode = Mode.FREESTYLE
        self.allowKeyTimer.setInterval(1)
        self.disableSelection(self.modeMenu, "Freestyle")

    def game(self):
        self.mode = Mode.GAME
        self.allowKeyTimer.setInterval(1000) # Allow 1 key press every second
        self.disableSelection(self.modeMenu, "Game")

    def sticker(self):
        self.mode = Mode.STICKER
        self.allowKeyTimer.setInterval(1000)
        self.currentStickerIndex = 0
        self.stickerTimer.start()
        self.disableSelection(self.modeMenu, "Sticker")

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

    def cHyperspeed(self):
        self.step = 10
        self.disableSelection(self.clockSpeedMenu, "Hyperspeed")

    # Handle the BCI key actions
    def setBCIKeyW(self):
        self.BCIKey = Qt.Key_W
        self.disableSelection(self.BCIKeyMenu, "W")

    def setBCIKeyA(self):
        self.BCIKey = Qt.Key_A
        self.disableSelection(self.BCIKeyMenu, "A")

    def setBCIKeyS(self):
        self.BCIKey = Qt.Key_S
        self.disableSelection(self.BCIKeyMenu, "S")

    def setBCIKeyD(self):
        self.BCIKey = Qt.Key_D
        self.disableSelection(self.BCIKeyMenu, "D")

    # Handle the feedback actions
    # def feedbackOn(self):
    #     self.feedback = True
    #     self.disableSelection(self.feedbackMenu, "On")

    # def feedbackOff(self):
    #     self.feedback = False
    #     self.disableSelection(self.feedbackMenu, "Off")

    # Updates the angle of the clock arm
    def updateAngle(self):
        self.theta = (self.theta + self.step) % 360
        self.update()

    def blinkBrush(self):
        if self.blink == True:
            self.blink = False
        else:
            self.blink = True

    def allowKeyPress(self):
        self.allowKey = True

    def incrementStickerIndex(self):
        self.currentStickerIndex = (self.currentStickerIndex + 1) % len(self.StickerIndices)

    # Disables the currently selected option in a menu
    def disableSelection(self, menu, actionName):
        for action in menu.actions():
            action.setDisabled(False)

            if action.text() == actionName:
                action.setDisabled(True)
 

# Set the icon in the task bar to match the window icon
myappid = 'GRH_BCI_Paint' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
 
# Create pyqt5 app
App = QApplication(sys.argv)

# Set a style to the app
myStyle = largeIconProxyStyle('Motif')
App.setStyle(myStyle)
 
# Create the instance of our Window
window = Window()
 
# Showing the window
window.show()
 
# start the app
sys.exit(App.exec())
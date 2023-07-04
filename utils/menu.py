from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

def createMenu(win):
    # Creating the menu bar
    mainMenu = win.menuBar()
    mainMenu.setMinimumHeight(30)
    font = mainMenu.font()
    font.setPointSize(10)
    mainMenu.setFont(font)

    # Adding a file menu for the save and clear actions
    win.fileMenu = mainMenu.addMenu("File")

    # Adding a brush menu to the main menu bar
    win.brushMenu = mainMenu.addMenu("Brush")

    # Adding brush size submenu to the brush menu
    win.bSizeMenu = win.brushMenu.addMenu("Brush Size")

    # Adding brush color submenu to the brush menu
    win.bColorMenu = win.brushMenu.addMenu("Brush Color")

    # Adding a brush style to main menu
    win.bStyleMenu = win.brushMenu.addMenu("Brush Style")

    # Adding a brush speed to main menu
    win.bSpeedMenu = win.brushMenu.addMenu("Brush Speed")

    # Adding a line style to main menu
    win.lStyleMenu = win.brushMenu.addMenu("Line Style")

    # Adding a mode selection to main menu
    win.modeMenu = mainMenu.addMenu("Mode")

    # Adding a clock speed selection to main menu
    win.clockSpeedMenu = mainMenu.addMenu("Clock Speed")

    # Adding feedback option to main menu
    win.feedbackMenu = mainMenu.addMenu("Feedback")

    # Creating the save action
    saveAction = QAction(QIcon(os.path.join("Assets", "save.png")), "Save", win)
    saveAction.setShortcut("Ctrl + S")
    win.fileMenu.addAction(saveAction)
    saveAction.triggered.connect(win.save)

    # Creating the clear action
    clearAction = QAction(QIcon(os.path.join("Assets", "delete.png")), "Clear", win)
    win.fileMenu.addAction(clearAction)
    clearAction.triggered.connect(win.clear)


    # Creating options for brush sizes
    pix_12 = QAction("12px", win)
    win.bSizeMenu.addAction(pix_12)
    pix_12.triggered.connect(win.Pixel_12)
    pix_12.setDisabled(True)

    pix_16 = QAction("16px", win)
    win.bSizeMenu.addAction(pix_16)
    pix_16.triggered.connect(win.Pixel_16)

    pix_20 = QAction("20px", win)
    win.bSizeMenu.addAction(pix_20)
    pix_20.triggered.connect(win.Pixel_20)

    pix_24 = QAction("24px", win)
    win.bSizeMenu.addAction(pix_24)
    pix_24.triggered.connect(win.Pixel_24)


    # Creating options for brush colors
    black = QAction(QIcon(os.path.join("Assets", "Black.png")), "Black", win)
    win.bColorMenu.addAction(black)
    black.triggered.connect(win.blackColor)
    black.setDisabled(True)

    white = QAction(QIcon(os.path.join("Assets", "White.png")), "White", win)
    win.bColorMenu.addAction(white)
    white.triggered.connect(win.whiteColor)

    red = QAction(QIcon(os.path.join("Assets", "Red.png")), "Red", win)
    win.bColorMenu.addAction(red)
    red.triggered.connect(win.redColor)

    orange = QAction(QIcon(os.path.join("Assets", "Orange.png")), "Orange", win)
    win.bColorMenu.addAction(orange)
    orange.triggered.connect(win.orangeColor)

    yellow = QAction(QIcon(os.path.join("Assets", "Yellow.png")), "Yellow", win)
    win.bColorMenu.addAction(yellow)
    yellow.triggered.connect(win.yellowColor)

    green = QAction(QIcon(os.path.join("Assets", "Green.png")), "Green", win)
    win.bColorMenu.addAction(green)
    green.triggered.connect(win.greenColor)

    blue = QAction(QIcon(os.path.join("Assets", "Blue.png")), "Blue", win)
    win.bColorMenu.addAction(blue)
    blue.triggered.connect(win.blueColor)

    purple = QAction(QIcon(os.path.join("Assets", "Purple.png")), "Purple", win)
    win.bColorMenu.addAction(purple)
    purple.triggered.connect(win.purpleColor)

    pink = QAction(QIcon(os.path.join("Assets", "Pink.png")), "Pink", win)
    win.bColorMenu.addAction(pink)
    pink.triggered.connect(win.pinkColor)

    rainbow = QAction(QIcon(os.path.join("Assets", "Rainbow.png")), "Rainbow", win)
    win.bColorMenu.addAction(rainbow)
    rainbow.triggered.connect(win.rainbowColor)

    custom = QAction("Custom", win)
    win.bColorMenu.addAction(custom)
    custom.triggered.connect(win.customColor)


    # Creating options for brush styles
    marker = QAction(QIcon(os.path.join("Assets", "marker.png")), "Marker", win)
    win.bStyleMenu.addAction(marker)
    marker.triggered.connect(win.marker)
    marker.setDisabled(True)

    watercolor = QAction(QIcon(os.path.join("Assets", "watercolor.png")), "Watercolor", win)
    win.bStyleMenu.addAction(watercolor)
    watercolor.triggered.connect(win.watercolor)

    sprayPaint = QAction(QIcon(os.path.join("Assets", "spray-paint.png")), "Spray Paint", win)
    win.bStyleMenu.addAction(sprayPaint)
    sprayPaint.triggered.connect(win.sprayPaint)

    graffiti = QAction("Graffiti", win)
    win.bStyleMenu.addAction(graffiti)
    graffiti.triggered.connect(win.graffiti)

    splatter = QAction("Splatter", win)
    win.bStyleMenu.addAction(splatter)
    splatter.triggered.connect(win.splatter)

    abstract = QAction("Abstract", win)
    win.bStyleMenu.addAction(abstract)
    abstract.triggered.connect(win.abstract)


    # Creating options for brush speeds
    bSlow = QAction("Slow", win)
    win.bSpeedMenu.addAction(bSlow)
    bSlow.triggered.connect(win.bSlow)

    bMedium = QAction("Medium", win)
    win.bSpeedMenu.addAction(bMedium)
    bMedium.triggered.connect(win.bMedium)
    bMedium.setDisabled(True)

    bFast = QAction("Fast", win)
    win.bSpeedMenu.addAction(bFast)
    bFast.triggered.connect(win.bFast)


    # Creating options for line styles
    solid = QAction("Solid", win)
    win.lStyleMenu.addAction(solid)
    solid.triggered.connect(win.solid)
    solid.setDisabled(True)

    dotted = QAction("Dotted", win)
    win.lStyleMenu.addAction(dotted)
    dotted.triggered.connect(win.dotted)


    # Creating options game modes
    freestyle = QAction("Freestyle", win)
    win.modeMenu.addAction(freestyle)
    freestyle.triggered.connect(win.freestyle)
    freestyle.setDisabled(True)

    game = QAction("Game", win)
    win.modeMenu.addAction(game)
    game.triggered.connect(win.game)


    # Creating options for clock speeds
    stopClock = QAction("Stop", win)
    win.clockSpeedMenu.addAction(stopClock)
    stopClock.triggered.connect(win.stopClock)

    cSlow = QAction("Slow", win)
    win.clockSpeedMenu.addAction(cSlow)
    cSlow.triggered.connect(win.cSlow)

    cMedium = QAction("Medium", win)
    win.clockSpeedMenu.addAction(cMedium)
    cMedium.triggered.connect(win.cMedium)
    cMedium.setDisabled(True)

    cFast = QAction("Fast", win)
    win.clockSpeedMenu.addAction(cFast)
    cFast.triggered.connect(win.cFast)

    # Creating options for feedback
    feedbackOn = QAction("On", win)
    win.feedbackMenu.addAction(feedbackOn)
    feedbackOn.triggered.connect(win.feedbackOn)

    feedbackOff = QAction("Off", win)
    win.feedbackMenu.addAction(feedbackOff)
    feedbackOff.triggered.connect(win.feedbackOff)
    feedbackOff.setDisabled(True)
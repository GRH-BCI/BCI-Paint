from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

def create_menu(win):
    # Creating the menu bar
    mainMenu = win.menuBar()
    mainMenu.setMinimumHeight(30)
    font = mainMenu.font()
    font.setPointSize(10)
    mainMenu.setFont(font)

    # Adding a file menu for the save and clear actions
    fileMenu = mainMenu.addMenu("File")

    # Adding brush size to main menu
    b_size = mainMenu.addMenu("Brush Size")

    # Adding brush color to main menu
    b_color = mainMenu.addMenu("Brush Color")

    # Adding a brush style to main menu
    b_style = mainMenu.addMenu("Brush Style")

    # Adding a brush speed to main menu
    b_speed = mainMenu.addMenu("Brush Speed")

    # Adding a line style to main menu
    l_style = mainMenu.addMenu("Line Style")

    # Adding a mode selection to main menu
    mode = mainMenu.addMenu("Mode")

    # Adding a clock speed selection to main menu
    clock_speed = mainMenu.addMenu("Clock Speed")

    # Adding feedback option to main menu
    feedback = mainMenu.addMenu("Feedback")

    # Creating the save action
    saveAction = QAction(QIcon(os.path.join("Assets", "save.png")), "Save", win)
    saveAction.setShortcut("Ctrl + S")
    fileMenu.addAction(saveAction)
    saveAction.triggered.connect(win.save)

    # Creating the clear action
    clearAction = QAction(QIcon(os.path.join("Assets", "delete.png")), "Clear", win)
    fileMenu.addAction(clearAction)
    clearAction.triggered.connect(win.clear)


    # Creating options for brush sizes
    pix_12 = QAction("12px", win)
    b_size.addAction(pix_12)
    pix_12.triggered.connect(win.Pixel_12)

    pix_16 = QAction("16px", win)
    b_size.addAction(pix_16)
    pix_16.triggered.connect(win.Pixel_16)

    pix_20 = QAction("20px", win)
    b_size.addAction(pix_20)
    pix_20.triggered.connect(win.Pixel_20)

    pix_24 = QAction("24px", win)
    b_size.addAction(pix_24)
    pix_24.triggered.connect(win.Pixel_24)


    # Creating options for brush colors
    black = QAction(QIcon(os.path.join("Assets", "Black.png")), "Black", win)
    b_color.addAction(black)
    black.triggered.connect(win.blackColor)

    white = QAction(QIcon(os.path.join("Assets", "White.png")), "White", win)
    b_color.addAction(white)
    white.triggered.connect(win.whiteColor)

    red = QAction(QIcon(os.path.join("Assets", "Red.png")), "Red", win)
    b_color.addAction(red)
    red.triggered.connect(win.redColor)

    orange = QAction(QIcon(os.path.join("Assets", "Orange.png")), "Orange", win)
    b_color.addAction(orange)
    orange.triggered.connect(win.orangeColor)

    yellow = QAction(QIcon(os.path.join("Assets", "Yellow.png")), "Yellow", win)
    b_color.addAction(yellow)
    yellow.triggered.connect(win.yellowColor)

    green = QAction(QIcon(os.path.join("Assets", "Green.png")), "Green", win)
    b_color.addAction(green)
    green.triggered.connect(win.greenColor)

    blue = QAction(QIcon(os.path.join("Assets", "Blue.png")), "Blue", win)
    b_color.addAction(blue)
    blue.triggered.connect(win.blueColor)

    purple = QAction(QIcon(os.path.join("Assets", "Purple.png")), "Purple", win)
    b_color.addAction(purple)
    purple.triggered.connect(win.purpleColor)

    pink = QAction(QIcon(os.path.join("Assets", "Pink.png")), "Pink", win)
    b_color.addAction(pink)
    pink.triggered.connect(win.pinkColor)

    rainbow = QAction(QIcon(os.path.join("Assets", "Rainbow.png")), "Rainbow", win)
    b_color.addAction(rainbow)
    rainbow.triggered.connect(win.rainbowColor)

    custom = QAction("Custom", win)
    b_color.addAction(custom)
    custom.triggered.connect(win.customColor)


    # Creating options for brush styles
    watercolor = QAction(QIcon(os.path.join("Assets", "watercolor.png")), "Watercolor", win)
    b_style.addAction(watercolor)
    watercolor.triggered.connect(win.watercolor)

    marker = QAction(QIcon(os.path.join("Assets", "marker.png")), "Marker", win)
    b_style.addAction(marker)
    marker.triggered.connect(win.marker)

    spray_paint = QAction(QIcon(os.path.join("Assets", "spray-paint.png")), "Spray Paint", win)
    b_style.addAction(spray_paint)
    spray_paint.triggered.connect(win.spray_paint)


    # Creating options for brush speeds
    b_slow = QAction("Slow", win)
    b_speed.addAction(b_slow)
    b_slow.triggered.connect(win.b_slow)

    b_medium = QAction("Medium", win)
    b_speed.addAction(b_medium)
    b_medium.triggered.connect(win.b_medium)

    b_fast = QAction("Fast", win)
    b_speed.addAction(b_fast)
    b_fast.triggered.connect(win.b_fast)


    # Creating options for line styles
    solid = QAction("Solid", win)
    l_style.addAction(solid)
    solid.triggered.connect(win.solid)

    dotted = QAction("Dotted", win)
    l_style.addAction(dotted)
    dotted.triggered.connect(win.dotted)


    # Creating options game modes
    freestyle = QAction("Freestyle", win)
    mode.addAction(freestyle)
    freestyle.triggered.connect(win.freestyle)

    game = QAction("Game", win)
    mode.addAction(game)
    game.triggered.connect(win.game)


    # Creating options for clock speeds
    stop_clock = QAction("Stop", win)
    clock_speed.addAction(stop_clock)
    stop_clock.triggered.connect(win.stop_clock)

    c_slow = QAction("Slow", win)
    clock_speed.addAction(c_slow)
    c_slow.triggered.connect(win.c_slow)

    c_medium = QAction("Medium", win)
    clock_speed.addAction(c_medium)
    c_medium.triggered.connect(win.c_medium)

    c_fast = QAction("Fast", win)
    clock_speed.addAction(c_fast)
    c_fast.triggered.connect(win.c_fast)

    # Creating options for feedback
    feedback_on = QAction("On", win)
    feedback.addAction(feedback_on)
    feedback_on.triggered.connect(win.feedback_on)

    feedback_off = QAction("Off", win)
    feedback.addAction(feedback_off)
    feedback_off.triggered.connect(win.feedback_off)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

def createMenu(win):
    # Creating the menu bar
    mainMenu = win.menuBar()
    font = mainMenu.font()
    font.setPointSize(14)
    mainMenu.setFont(font)

    # Adding a file menu for the save and clear actions
    win.fileMenu = mainMenu.addMenu("\U0001F4C1 File")
    win.fileMenu.setFont(font)

    # Adding a brush menu to the main menu bar
    win.brushMenu = mainMenu.addMenu("\U0001F58C Brush")
    win.brushMenu.setFont(font)

    # Adding brush size submenu to the brush menu
    win.bSizeMenu = win.brushMenu.addMenu(QIcon(os.path.join("Assets", "brush-sizes.png")), "Brush Size")
    win.bSizeMenu.setFont(font)

    # Adding brush color submenu to the brush menu
    win.bColorMenu = win.brushMenu.addMenu(QIcon(os.path.join("Assets", "colour.png")), "Brush Color")
    win.bColorMenu.setFont(font)

    # Adding brush texture submenu to the brush menu
    win.bTextureMenu = win.brushMenu.addMenu(QIcon(os.path.join("Assets", "material.png")),  "Texture")
    win.bTextureMenu.setFont(font)

    # Adding paint type submenu to the brush menu
    win.bPaintTypeMenu = win.brushMenu.addMenu(QIcon(os.path.join("Assets", "paint-bucket.png")), "Paint Type")
    win.bPaintTypeMenu.setFont(font)

    # Adding a brush style submenu to the brush menu
    win.bStyleMenu = win.brushMenu.addMenu(QIcon(os.path.join("Assets", "paint-tools.png")), "Brush Style")
    win.bStyleMenu.setFont(font)

    # Adding a brush speed submenu to the brush menu
    win.bSpeedMenu = win.brushMenu.addMenu(QIcon(os.path.join("Assets", "brush-speed.png")), "Brush Speed")
    win.bSpeedMenu.setFont(font)

    # Adding a line style submenu to the brush menu
    win.lStyleMenu = win.brushMenu.addMenu(QIcon(os.path.join("Assets", "line-style.png")), "Line Style")
    win.lStyleMenu.setFont(font)

    # Adding a mode selection to main menu
    win.modeMenu = mainMenu.addMenu("\U0001F3AE Mode")
    win.modeMenu.setFont(font)

    # Adding a clock speed selection to main menu
    win.clockSpeedMenu = mainMenu.addMenu("\U0001F55B Clock Speed")
    win.clockSpeedMenu.setFont(font)

    # Adding BCI key selection to main menu
    win.BCIKeyMenu = mainMenu.addMenu("\U00002328 BCI Key")
    win.BCIKeyMenu.setFont(font)

    # Adding feedback option to main menu
    # win.feedbackMenu = mainMenu.addMenu("Feedback")
    # win.feedbackMenu.setFont(font)

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
    pix_12 = QAction(QIcon(os.path.join("Assets", "12px.png")), "12px", win)
    win.bSizeMenu.addAction(pix_12)
    pix_12.triggered.connect(win.Pixel_12)

    pix_16 = QAction(QIcon(os.path.join("Assets", "16px.png")), "16px", win)
    win.bSizeMenu.addAction(pix_16)
    pix_16.triggered.connect(win.Pixel_16)

    pix_20 = QAction(QIcon(os.path.join("Assets", "20px.png")), "20px", win)
    win.bSizeMenu.addAction(pix_20)
    pix_20.triggered.connect(win.Pixel_20)
    pix_20.setDisabled(True)

    pix_24 = QAction(QIcon(os.path.join("Assets", "24px.png")), "24px", win)
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

    gold = QAction(QIcon(os.path.join("Assets", "Gold.jpg")), "Gold", win)
    win.bColorMenu.addAction(gold)
    gold.triggered.connect(win.goldColor)

    silver = QAction(QIcon(os.path.join("Assets", "Silver.jpg")), "Silver", win)
    win.bColorMenu.addAction(silver)
    silver.triggered.connect(win.silverColor)

    rainbow = QAction(QIcon(os.path.join("Assets", "Rainbow.png")), "Rainbow", win)
    win.bColorMenu.addAction(rainbow)
    rainbow.triggered.connect(win.rainbowColor)

    custom = QAction("Custom", win)
    win.bColorMenu.addAction(custom)
    custom.triggered.connect(win.customColor)

    # Creating options for texture types
    none = QAction(QIcon(os.path.join("Assets", "no-entry.png")), "None", win)
    win.bTextureMenu.addAction(none)
    none.triggered.connect(win.noTexture)
    none.setDisabled(True)

    metallic = QAction(QIcon(os.path.join("Assets", "shines.png")), "Metallic", win)
    win.bTextureMenu.addAction(metallic)
    metallic.triggered.connect(win.metallicTexture)

    # Creating options for paint types
    acrylic = QAction(QIcon(os.path.join("Assets", "paint-tube.png")), "Acrylic", win)
    win.bPaintTypeMenu.addAction(acrylic)
    acrylic.triggered.connect(win.acrylic)
    acrylic.setDisabled(True)

    watercolor = QAction(QIcon(os.path.join("Assets", "water-pot.png")), "Watercolor", win)
    win.bPaintTypeMenu.addAction(watercolor)
    watercolor.triggered.connect(win.watercolor)


    # Creating options for brush styles
    marker = QAction(QIcon(os.path.join("Assets", "marker.png")), "Marker", win)
    win.bStyleMenu.addAction(marker)
    marker.triggered.connect(win.marker)
    marker.setDisabled(True)

    sprayPaint = QAction(QIcon(os.path.join("Assets", "spray-paint.png")), "Spray Paint", win)
    win.bStyleMenu.addAction(sprayPaint)
    sprayPaint.triggered.connect(win.sprayPaint)

    graffiti = QAction(QIcon(os.path.join("Assets", "graffiti.png")), "Graffiti", win)
    win.bStyleMenu.addAction(graffiti)
    graffiti.triggered.connect(win.graffiti)

    splatter = QAction(QIcon(os.path.join("Assets", "splatter.png")), "Splatter", win)
    win.bStyleMenu.addAction(splatter)
    splatter.triggered.connect(win.splatter)

    abstract = QAction(QIcon(os.path.join("Assets", "abstract-shape.png")), "Abstract", win)
    win.bStyleMenu.addAction(abstract)
    abstract.triggered.connect(win.abstract)


    # Creating options for brush speeds
    bSlow = QAction(QIcon(os.path.join("Assets", "speedometer-slow.png")), "Slow", win)
    win.bSpeedMenu.addAction(bSlow)
    bSlow.triggered.connect(win.bSlow)

    bMedium = QAction(QIcon(os.path.join("Assets", "speedometer-medium.png")), "Medium", win)
    win.bSpeedMenu.addAction(bMedium)
    bMedium.triggered.connect(win.bMedium)
    bMedium.setDisabled(True)

    bFast = QAction(QIcon(os.path.join("Assets", "speedometer-fast.png")), "Fast", win)
    win.bSpeedMenu.addAction(bFast)
    bFast.triggered.connect(win.bFast)


    # Creating options for line styles
    solid = QAction(QIcon(os.path.join("Assets", "solid.png")), "Solid", win)
    win.lStyleMenu.addAction(solid)
    solid.triggered.connect(win.solid)
    solid.setDisabled(True)

    dotted = QAction(QIcon(os.path.join("Assets", "dotted.png")), "Dotted", win)
    win.lStyleMenu.addAction(dotted)
    dotted.triggered.connect(win.dotted)


    # Creating options game modes
    freestyle = QAction(QIcon(os.path.join("Assets", "freestyle.png")), "Freestyle", win)
    win.modeMenu.addAction(freestyle)
    freestyle.triggered.connect(win.freestyle)
    freestyle.setDisabled(True)

    game = QAction(QIcon(os.path.join("Assets", "game.png")), "Game", win)
    win.modeMenu.addAction(game)
    game.triggered.connect(win.game)

    sticker = QAction(QIcon(os.path.join("Assets", "sticker.png")), "Sticker", win)
    win.modeMenu.addAction(sticker)
    sticker.triggered.connect(win.sticker)


    # Creating options for clock speeds
    stopClock = QAction(QIcon(os.path.join("Assets", "stop.png")), "Stop", win)
    win.clockSpeedMenu.addAction(stopClock)
    stopClock.triggered.connect(win.stopClock)

    cSlow = QAction(QIcon(os.path.join("Assets", "speedometer-slow.png")), "Slow", win)
    win.clockSpeedMenu.addAction(cSlow)
    cSlow.triggered.connect(win.cSlow)

    cMedium = QAction(QIcon(os.path.join("Assets", "speedometer-medium.png")), "Medium", win)
    win.clockSpeedMenu.addAction(cMedium)
    cMedium.triggered.connect(win.cMedium)
    cMedium.setDisabled(True)

    cFast = QAction(QIcon(os.path.join("Assets", "speedometer-fast.png")), "Fast", win)
    win.clockSpeedMenu.addAction(cFast)
    cFast.triggered.connect(win.cFast)

    cHyperspeed = QAction(QIcon(os.path.join("Assets", "hyperspeed.png")), "Hyperspeed", win)
    win.clockSpeedMenu.addAction(cHyperspeed)
    cHyperspeed.triggered.connect(win.cHyperspeed)

    # Creating options for the BCI key
    wKey = QAction("W", win)
    win.BCIKeyMenu.addAction(wKey)
    wKey.triggered.connect(win.setBCIKeyW)
    wKey.setDisabled(True)

    aKey = QAction("A", win)
    win.BCIKeyMenu.addAction(aKey)
    aKey.triggered.connect(win.setBCIKeyA)

    sKey = QAction("S", win)
    win.BCIKeyMenu.addAction(sKey)
    sKey.triggered.connect(win.setBCIKeyS)

    dKey = QAction("D", win)
    win.BCIKeyMenu.addAction(dKey)
    dKey.triggered.connect(win.setBCIKeyD)

    # Creating options for feedback
    # feedbackOn = QAction("On", win)
    # win.feedbackMenu.addAction(feedbackOn)
    # feedbackOn.triggered.connect(win.feedbackOn)

    # feedbackOff = QAction("Off", win)
    # win.feedbackMenu.addAction(feedbackOff)
    # feedbackOff.triggered.connect(win.feedbackOff)
    # feedbackOff.setDisabled(True)
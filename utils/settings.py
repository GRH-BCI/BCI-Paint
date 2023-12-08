from enum import Enum
from PyQt5.QtWidgets import QProxyStyle, QStyle

class Mode(Enum):
    """
    A class used to represent different modes of a program

    Varients:
    ----------
    FREESTYLE
    GAME
    """
    FREESTYLE = "freestyle"
    GAME = "game"


class LineStyle(Enum):
    """
    A class used to represent different line styles

    Varients:
    ----------
    SOLID
    DOTTED
    """
    SOLID = "solid"
    DOTTED = "dotted"

class BrushStyle(Enum):
    """
    A class used to represent different brush styles

    Varients:
    ----------
    MARKER
    SPRAYPAINT
    GRAFFITI
    SPLATTER
    ABSTRACT
    """

    MARKER = "marker"
    SPRAYPAINT = "spray paint"
    GRAFFITI = "graffiti"
    SPLATTER = "splatter"
    ABSTRACT = "abstract"

class Texture(Enum):
    """
    A class used to represent different textures

    Varients:
    ----------
    GOLD
    SILVER
    NULL
    """

    GOLD = "gold"
    SILVER = "silver"
    NULL = "none"

# Create a style class to make the menu bar icons larger
class largeIconProxyStyle(QProxyStyle):
    def pixelMetric(self, QStylePixelMetric, option=None, widget=None):

        if QStylePixelMetric == QStyle.PM_SmallIconSize:
            return 30
        else:
            return QProxyStyle.pixelMetric(self, QStylePixelMetric, option, widget)
from enum import Enum

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
    WATERCOLOR
    SPRAYPAINT
    GRAFFITI
    SPLATTER
    ABSTRACT
    """
    MARKER = "marker"
    WATERCOLOR = "watercolor"
    SPRAYPAINT = "spray paint"
    GRAFFITI = "graffiti"
    SPLATTER = "splatter"
    ABSTRACT = "abstract"
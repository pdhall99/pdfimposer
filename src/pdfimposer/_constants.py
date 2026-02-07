PAGE_FORMATS = {
    "A3": (842, 1192),
    "A4": (595, 842),
    "A5": (420, 595),
    "Tabloid": (792, 1224),
    "Letter": (612, 792),
    "Legal": (612, 1008),
}


class PageOrientation:
    """The page orientation constants."""

    PORTRAIT = False
    """The portrait orientation"""
    LANDSCAPE = True
    """The landscape orientation"""


class TwoSidedFlip:
    """Which paper edge will the flip occur on when printing?"""

    SHORT_EDGE = "short-edge flip"
    """Pages will be flipped on the short edge"""
    LONG_EDGE = "long-edge flip"
    """Pages will be flipped on the long edge"""

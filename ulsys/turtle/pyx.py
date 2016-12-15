"""
ulsys PyX turtle file. Defines a turtle that outputs PyX commands. Use with PyX
to render to SVG.
"""

from .turtle import BaseTurtle

try:
    from pyx import *

    class PyXTurtle(BaseTurtle):
        def __init__(self):
            super().__init__()
            self.paths = []
            self.states = []
            self.paths.append(path.moveto(0, 0))
            self.circles = []

        def forward(self, scale=1.0):
            super().forward(scale)
            self.paths.append(path.lineto(self.pos.x, self.pos.y))

        def rotate(self, rad):
            super().rotate(rad)

        def push(self):
            self.states.append((self.pos, self.angle))

        def linewidth(self, width):
            path.moveto(0,0) #IMPLEMENT

        def pop(self):
            pos, angle = self.states.pop()
            self.pos = pos
            self.angle = angle
            self.paths.append(path.moveto(pos.x, pos.y))

        def circle(self, r):
            self.circles.append(path.circle(self.pos.x, self.pos.y, r))
    
    __all__ = [
        "PyXTurtle"
    ]

except ImportError:
    pass

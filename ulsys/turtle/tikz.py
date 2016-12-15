"""
ulsys tikz turtle file. Defines a turtle that outputs tikz code for LaTeX.
"""

__all__ = [
    "TikzTurtle"
]

from .turtle import BaseTurtle
from .geom import *

class TikzPath:
    def __init__(self, start=None):
        self._v = ([] if start is None else [start])
        self._attribs = {}
        self._cycle = False
    
    def to(self, v):
        self._v.append(v)
    
    def lineWidth(self, width):
        self._attribs["line_width"] = width
    
    def color(self, col):
        self._attribs["color"] = col
    
    def setCycle(self):
        self._cycle = True
    
    def __str__(self):
        if not self._v:
            return ""
        args = ",".join([k + "=" + v for k, v in self._attribs.items()])
        cmd = "\\draw[" + args + "]"
        return cmd + "--".join(["({:.1f},{:.1f})".format(v.x, v.y) for v in self._v]) + ";"

class TikzPicture:
    def __init__(self, scale=None):
        self._scale = scale
        self._objs = []
    
    def add(self, obj):
        self._objs.append(obj)
    
    def _tikzCommands(self, prettyPrint=False):
        separator = " " # At minimum, a space is needed for tikz.
        if prettyPrint:
            separator = "\n\t"
        return separator.join(map(str, self._objs))

    def toTexCode(self, prettyPrint=False):
        attrs = ""
        if self._scale:
            attrs += "scale=" + str(self._scale)
        # Start outputting the code.
        code  = "\\begin{tikzpicture}[" + attrs + "]"
        code += self._tikzCommands(prettyPrint=prettyPrint)
        code += "\\end{tikzpicture}"
        return code

class TikzTurtle(BaseTurtle):
    def __init__(self, pos=vec2(0, 0), angle=math.pi/2):
        super().__init__(pos=pos, angle=angle)
        self._stack = []
        self._picture = TikzPicture()
        self._path = None
    
    def forward(self, scale=1.0):
        if self._path is None:
            self._path = TikzPath(self.pos)
        super().forward(scale)
        self._path.to(self.pos)
    
    def rotate(self, rad):
        super().rotate(rad)
    
    def push(self):
        self._stack.append((self._path, self.pos, self.angle))
        self._path = None
    
    def pop(self):
        if not self._path is None: 
            self._picture.add(self._path)
        path, pos, angle = self._stack.pop()
        self._path = path
        self.pos = pos
        self.angle = angle
    
    def color(self, color):
        if self._path is None:
            self._path = TikzPath(self.pos)
        self._path.color(color)
    
    @property
    def tikzPicture(self):
        return self._picture

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# The MIT License (MIT)
# 
# Copyright (c) 2016 Simon Otter
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
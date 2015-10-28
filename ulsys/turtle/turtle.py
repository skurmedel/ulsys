"""
ulsys turtle file. This package is different from the turtle packaged with 
CPython.

License follows
-------------------------------------------------------------------------------
The MIT License (MIT)

Copyright (c) 2015 Simon Otter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__all__ = [
    "mapActions",
    "BaseTurtle",
    "TurtleAction",
    "PyXTurtle"
]

import math
from abc import ABC, abstractmethod

class _vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, b):
        return _vec2(self.x + b.x, self.y + b.y)
    
    def __mul__(self, a):
        return _vec2(self.x * float(a), self.y * float(a))
        
def mapActions(symbols, actions, turtle):
    """Takes a sequence of symbols and maps them to actions.
    
    symbols is a sequence.
    actions is a dictionary mapping symbol->action
    turtle is an implementation of the turtle interface.
    
    Non mapped symbols are ignored (they do not generate an error!)
    
    An action is a function object f: turtle -> None.
    """
    for s in symbols:
        # Todo: Maybe warn if not in actions?
        if s in actions:
            f = actions[s]
            f(turtle)
    return turtle

class BaseTurtle(ABC):
    """An abstract turtle interface. This represents the bare minimum interface
    for a turtle object.
    
    Note that a turtle doesn't actually have to inherit from this class to work,
    but it has to provide roughly the same interface.
    """
    def __init__(self, pos=_vec2(0, 0), angle=math.pi/2):
        self.pos = pos
        self.angle = angle
    
    def direction(self):
        """Returns the direction as a unit vector."""
        return _vec2(math.cos(self.angle), math.sin(self.angle))
        
    @abstractmethod
    def forward(self, scale=1.0):
        self.pos += self.direction() * scale
    
    @abstractmethod
    def rotate(self, rad):
        self.angle += rad
    
    @abstractmethod
    def push(self):
        pass
    
    @abstractmethod
    def pop(self):
        pass

class TurtleAction:
    def __init__(self, method_name, args=[]):
        self._method_name = method_name
        self._args = args
    
    def __call__(self, turtle):
        f = getattr(turtle, self._method_name)
        f(*self._args)
    
    @classmethod
    def forward(cls):
        return TurtleAction("forward")
    
    @classmethod
    def rotate(cls, radians):
        return TurtleAction("rotate", [radians])
    
    @classmethod
    def push(cls):
        return TurtleAction("push")
    
    @classmethod
    def pop(cls):
        return TurtleAction("pop")
        
    @classmethod
    def combine(cls, a, b):
        def do_combined_action(turtle):
            a(turtle)
            b(turtle)
        return do_combined_action

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
            
except ImportError:
    pass
"""
ulsys main file.

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

import math

class _vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, b):
        return _vec2(self.x + b.x, self.y + b.y)

def evaluateSystem(axiom, rules, n):
    """Evaluates a regular bog-standard L-System.
    
    axiom is a sequence of symbols.
    rules is a dictionary mapping s->sequence
    n is an integer specifying the number of iterations
    
    What data constitutes as a symbol is not really important, but it should
    support equality and hashing.
    
    Example for the simple Pythagoras tree fractal:
        
        >>> evaluateSystem("0", {"1":list("11"),"0":list("1[0]0")}, 2)
        ['1', '1', '[', '1', '[', '0', ']', '0', ']', '1', '[', '0', ']', '0']
    """    
    if n < 1:
        return axiom
    result = []
    for x in axiom:
        if x in rules:
            result += rules[x]
        else:
            result.append(x)
    return evaluateSystem(result, rules, n-1)

def turtleMapper(symbols, actions, turtle):
    """Takes a sequence of symbols and maps them to actions.
    
    symbols is a sequence.
    actions is a dictionary mapping symbol->action
    turtle is an implementation of the turtle interface.
    
    Non mapped symbols are ignored (they do not generate an error!)
    
    An action is a function f: turtle -> None.
    """
    for s in symbols:
        # Todo: Maybe warn if not in actions?
        if s in actions:
            f = actions[s]
            f(turtle)
    return turtle

def turtleAction(method_name, args=[]):
    def do_action(turtle):
        f = getattr(turtle, method_name)
        f(*args)
    return do_action

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


def linewidthAction(width):
    return turtleAction("linewidth", [width])

def pythagorasTree(n, axiom="0"):
    symbols = evaluateSystem(axiom, {"1":list("11"),"0":list("1[0]0")}, n)
    return symbols

pythagorasTree.turtleActions = {
    "0": TurtleAction.forward(),
    "1": TurtleAction.forward(),
    "[": TurtleAction.combine(TurtleAction.push(), TurtleAction.rotate(-math.pi/4.0)),
    "]": TurtleAction.combine(TurtleAction.pop(), TurtleAction.rotate(math.pi/4.0))
}

def fractalPlant(n, axiom="X"):
    symbols = evaluateSystem(axiom, {"X":list("C0FF+[C1+F]+[C3-F]"), "F":list("C0FF-[C1-F+F]+[C2+F-F]")}, n)
    return symbols

fractalPlant.turtleActions = {
        "F":TurtleAction.forward(),
        "-":TurtleAction.rotate(-math.pi / 9),
        "+":TurtleAction.rotate( math.pi / 9),
        "[":TurtleAction.push(),
        "]":TurtleAction.pop()
    }

def kochFlake(n, axiom="F++F++F"):
    symbols = evaluateSystem(axiom, {"F":list("F-F++F-F")}, n)
    return symbols

kochFlake.turtleActions = {
        "F":TurtleAction.forward(),
        "-":TurtleAction.rotate(-math.pi / 2.5),
        "+":TurtleAction.rotate( math.pi / 2.5),
        "[":TurtleAction.push(),
        "]":TurtleAction.pop()
    }

def triKochFlake(n, axiom="F++F++F"):
    symbols = evaluateSystem(axiom, {"F":list("F-X++X-F"), "X":list("[-F++F++F]")}, n)
    return symbols
    
triKochFlake.turtleActions = kochFlake.turtleActions

# TODO: MOVE INTO PACKAGE!
from pyx import *
import math

class pyxTurtleState:
    def __init__(self):
        self.pos = _vec2(0,0)
        self.angle = math.pi / 2.0
        self.paths = []
        self.states = []
        self.paths.append(path.moveto(0, 0))
    
    def dir(self):
        return _vec2(math.cos(self.angle), math.sin(self.angle))
    
    def forward(self):
        self.pos += self.dir()
        self.paths.append(path.lineto(self.pos.x, self.pos.y))
    
    def rotate(self, rad):
        self.angle += rad
    
    def push(self):
        self.states.append((self.pos, self.angle))
    
    def linewidth(self, width):
        path.moveto(0,0) #IMPLEMENT

    
    def pop(self):
        pos, angle = self.states.pop()
        self.pos = pos
        self.angle = angle
        self.paths.append(path.moveto(pos.x, pos.y))

for i in range(1, 6):
    endState = turtleMapper(pythagorasTree(i), pythagorasTree.turtleActions, pyxTurtleState())
    #endState = turtleMapper(kochFlake(i), kochFlake.turtleActions, pyxTurtleState())
    c = canvas.canvas()
    c.stroke(path.path(*endState.paths), [style.linewidth(0.25)])
    c.writeSVGfile("tree{}.svg".format(i))


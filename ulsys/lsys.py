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

__all__ = [
    "TurtleAction", 
    "pythagorasTree", 
    "kochFlake", 
    "triKochFlake",
    "fractalPlant",
    "FunctionalSymbol"
]

class FunctionalSymbol:
    """Represents a symbol which is also a function. This gives the user a way
    to associate an action with an L-System symbol. Can be used as an alternative
    way to run a Turtle from an L-System.
    """
    def __init__(self, name, f):
        """Wraps f as a symbol with the specified name.
        
        The name is used for equality testing.
        
        f must be a callable:

            >>> FunctionalSymbol("S", 123)
            Traceback (most recent call last):
                File "<stdin>", line 1, in <module>
            TypeError: f is not a callable
        
        """
        if not callable(f):
            raise TypeError("f is not a callable")
        self._name = name
        self._f = f
    
    def __call__(self, *args, **kwargs):
        self._f(*args, functionalSymbolName=self._name, **kwargs)
    
    def __eq__(self, b):
        return self._name == b
    
    def __str__(self):
        return self._name
    
    def __hash__(self):
        return self._name.__hash__()
        
    @classmethod
    def call_all_with_results(cls, symbols, *args, **kwargs):
        """Tries to invoke all symbols as function, ignoring those 
        not callable.
        
        Returns a generator function that returns each consecutive input.
        """
        for s in symbols:
            if callable(s):
                yield s(*args, **kwargs)
    
    @classmethod
    def call_all(cls, symbols, *args, **kwargs):
        """Same as call_all_with_results but evaluates generator and 
        discards output.
        
        Will loop forever if symbols is not finite.
        """
        gen = cls.call_all(symbols, *args, **kwargs)
        list(gen)

if __name__ != "__main__":
    # SOME COMMON L-SYSTEMS, FOR TESTING, EXAMPLES ETC.
    from .turtle import TurtleAction
    from .standard import evaluateSystem, production
    
    def pythagorasTree(n, axiom="0"):
        symbols = evaluateSystem("0", production("1->11", "0->1[0]0"), n)
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
        symbols = evaluateSystem(axiom, production("F->F-F++F-F"), n)
        return symbols
    
    kochFlake.turtleActions = {
            "F":TurtleAction.forward(),
            "-":TurtleAction.rotate(-math.pi / 3),
            "+":TurtleAction.rotate( math.pi / 3),
            "[":TurtleAction.push(),
            "]":TurtleAction.pop()
        }
    
    def triKochFlake(n, axiom="F++F++F"):
        symbols = evaluateSystem(axiom, {"F":list("F-X++X-F"), "X":list("[-F++F++F]")}, n)
        return symbols
        
    triKochFlake.turtleActions = kochFlake.turtleActions

if __name__ == "__main__":
    import doctest
    doctest.testmod()
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
    "evaluateSystem", 
    "TurtleAction", 
    "pythagorasTree", 
    "kochFlake", 
    "triKochFlake",
    "fractalPlant",
    "FunctionalSymbol",
    "production"
]

def production(*args):
    """Creates a production rule or list of rules from the input.
    
    Supports two kinds of input:
    
        A parsed string of form "S->ABC" where S is a single character, and
        ABC is a string of characters. S is the input symbol, ABC is the output
        symbols.
        Neither S nor ABC can be any of the characters "-", ">" for obvious 
        reasons.
    
        A tuple of type (S, Seq, ...) where S is the symbol of some hashable 
        type and seq is an finite iterable representing the output symbols.
        
        Naturally if you don't want to use characters/strings to represent 
        symbols then you'll typically need to use the second form.

    You can pass multiple inputs to generate multiple production rules, 
    in that case the result is a list of rules, not a single rule.
    
    If you pass multiple inputs the symbol must differ since a simple
    L-System only supports one production rule per symbol.
    
    Example:
    
        >>> production("F->Ab[]") 
        ('F', ['A', 'b', '[', ']'])
        
        >>> production("F->Ab[]", ("P", "bAz"), (1, (0,1)))
        [('F', ['A', 'b', '[', ']']), ('P', ['b', 'A', 'z']), (1, [0, 1])]
    """
    if len(args) < 1:
        raise ValueError("missing arguments")
    res = []
    for a in args:
        if issubclass(str, type(a)):
            parts = a.split(sep="->", maxsplit=1)
            if len(parts) < 2:
                raise ValueError("couldn't parse invalid string \"{}\"".format(a))
            res.append((parts[0], list(parts[1])))
        elif issubclass(tuple, type(a)):
            s, to, *vals = a
            res.append((s, list(to)))
        else:
            raise TypeError("sorry don't know what to do with " + str(type(a)))
    if len(res) == 1:
        return res[0]
    return res

def evaluateSystem(axiom, rules, n):
    """Evaluates a regular bog-standard L-System.
    
    axiom is a sequence of symbols.
    rules is either:
        a dictionary type S->Symbols, like {1: [1, 2, 3]}
        a list of tuples as the ones produced by the function production()
        a single tuple as the ones produced by the function production()
    n is an integer specifying the number of iterations
    
    What data constitutes as a symbol is not really important, but it should
    support equality and hashing.
    
    Example for the simple Pythagoras tree fractal:
        
        >>> evaluateSystem("0", {"1":list("11"),"0":list("1[0]0")}, 2)
        ['1', '1', '[', '1', '[', '0', ']', '0', ']', '1', '[', '0', ']', '0']

    A cleaner version using production():
        
        >>> evaluateSystem("0", production("1->11", "0->1[0]0"), 2)
        ['1', '1', '[', '1', '[', '0', ']', '0', ']', '1', '[', '0', ']', '0']
    """
    if issubclass(type(rules), list):
        rules = dict(rules)
    if issubclass(type(rules), tuple):
        rules = [rules]
    if n < 1:
        return axiom
    result = []
    for x in axiom:
        if x in rules:
            result += rules[x]
        else:
            result.append(x)
    return evaluateSystem(result, rules, n-1)

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
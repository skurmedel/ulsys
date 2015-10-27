"""
ulsys stochastic L-System module.

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

import re

_prodre = re.compile("^([^->])(\s[0-9]+(\.[0-9]*)?)?\s*->([^->]*)$")

def production(*args):
    """Creates a production rule or list of production rules from input.
    
    Like it's sister function in the standard module this function supports
    several kinds of input.
    
    The different kinds of input are:
    
        A string of format "S R -> Abc", where S is the symbol, R is a 
        real valued probability constant and Abc is the output symbols.
        R is optional, if R is omitted then the probability constant is assumed
        to be 1.0.
        
        A tuple (S, R, Abc, ...) where the tokens means the same as in the prior
        scenario. Abc should be an iterable type. R must be anything supported
        by float().
    
    If more than one input is given, the result is a list of rules.
    
    Example of parsed input:    
    
    >>> production("F 0.3->F++F++F", "F 0.7->F+F+F", "A->B")
    [('F', 0.3, ['F', '+', '+', 'F', '+', '+', 'F']), ('F', 0.7, ['F', '+', 'F', '+', 'F']), ('A', 1.0, ['B'])]
    
    Exceptions are raised if the input is not supported:    
    
    >>> production(1234)
    Traceback (most recent call last):
    TypeError: don't know what to do with type <class 'int'>
    
    >>> production("F 234 invalid blabla")
    Traceback (most recent call last):
    ValueError: could not parse input: 'F 234 invalid blabla'
    """
    if len(args) < 1:
        raise ValueError("missing arguments")
    res = []
    for a in args:
        if issubclass(type(a), str):
            matches = _prodre.match(a)
            if not matches:
                raise ValueError("could not parse input: '{}'".format(a))
            s, r, abc = matches.group(1, 2, 4)
            if r is None:
                r = 1.0
            res.append((s, float(r), list(abc)))
        elif issubclass(type(a), tuple):
            s, r, abc, *rem = a
            res.append((s, float(r), list(abc)))
        else:
            raise TypeError("don't know what to do with type {}".format(type(a)))
    if len(res) == 1:
        return res[0]
    return res

def evaluateSystem(axiom, rules, n):
    """Evaluates a stochastic system. 
    
    Since there can be multiple production rules for a symbol in a stochastic 
    L-System we must enforce certain requirements. 
    
    For an input symbol S, its production rules (if any) has an associated 
    probability P. The total sum of P for all the rules for S must be less than
    or equal to 1.0.
    
    axiom is a list of starting symbols.
    rules is any of the following:
        TBD.
    n is the number of iterations.
    """ 
    pass
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
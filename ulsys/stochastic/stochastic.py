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
import random
import itertools

__all__ = ["production", "evaluateSystem"]

_prodre = re.compile("^([^->])(\s+[0-9]+(\.[0-9]*)?)?\s*->([^\s]+)$")

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

def evaluateSystem(axiom, rules, n, rng=None):
    """Evaluates a stochastic system. 
    
    A stochastic system consists of an axiom, an alphabet and the rules. In this
    module the alphabet is inferred from the axiom and the rules.
    
    Each rule has an associated symbol S, a probability R and a production Abc.
    
    Each iteration, every symbol S in the axiom is iterated. We find the rules
    for the symbol and based on the probability R we pick one. S is replaced
    with the rule's production Abc, itself a list of symbols.
    
    At the end of an iteration the axiom for the next iteration is set to the
    result of this process.
    
    Since there can be multiple production rules for a symbol in a stochastic 
    L-System we must enforce certain requirements. 
    
        For an input symbol S, its production rules (if any) has an associated 
        probability P. The total sum of P for all the rules for S must be 
        greater than zero. Each individual rules probability is scaled by the
        total sum, so for example two rules for S, with P 2 and 4 are scaled
        by 1/6 to 1/3 and 2/3.
        
    Being a stochastic system it is generally not deterministic, you can force
    determinism by providing your own pseudo-random number generator. This is 
    generally needed when simulating an evolving plant or other phenomena by 
    increasing n; if the seed is not the same each time the system is evaluated 
    it will yield different shapes for each "generation".
    
    axiom is a list of starting symbols.
    rules is any of the following:
        a dictionary type S->[(R, Symbols)], like {1: [(0.2, [1, 2, 3])]}
        a list of tuples as the ones produced by the function production()
        a single tuple as the ones produced by the function production()
    n is the number of iterations.
    
    rng is an optional value that is expected to be either None, or a function
    that returns a floating point value between 0 and 1.
    
    >>> evaluateSystem("AA", production("A 0.5->BA", "A 0.5->C"), 2, rng=lambda: 0.5)
    ['B', 'B', 'A', 'B', 'B', 'A']
    """ 
    if rng is None:
        rng = lambda: random.random()
    if not callable(rng):
        raise TypeError("rng is supposed to be callable")
    
    s_to_rules = dict()
    rtype = type(rules)
    
    if issubclass(rtype, dict):
        s_to_rules = rules
    else:
        if issubclass(rtype, tuple):
            rules = [rules]
            rtype = type(rules)
        
        if issubclass(rtype, list):
            for S, R, Abc, *t in rules:
                if S in s_to_rules:
                    s_to_rules[S].append((R, Abc))
                else:
                    s_to_rules[S] = [(R, Abc)]
        else:
            raise TypeError("rules is of an unsupported type {}".format(rtype))
    
    # Recursive implementation. To speed things up we avoid the above checks.
    def impl(curr_axiom, curr_n):
        if curr_n < 1:
            return curr_axiom
        newaxiom = []
        # Replace each symbol in the axiom
        for S in curr_axiom:
            if S in s_to_rules:
                # Todo: These steps could be moved out of the loop!
                # Sort by probability
                current_rules = sorted(s_to_rules[S], key=lambda x: x[0])
                # The total probability for all the rules for the given S
                prob_total = sum((R for R, Abc in current_rules))
                
                # Construct a list of weights, ordered and scaled by total
                weights = [R/prob_total for R, Abc in current_rules]
                weights_acc = list(itertools.accumulate(weights))
                p = rng()
                
                selected_rule = None
                last_w = 0
                for i,w in zip(range(0, len(weights_acc)), weights_acc):
                    if p >= last_w and p <= w:
                        selected_rule = current_rules[i]
                        break
                    else:
                        last_w = w
                _, Abc = selected_rule
                newaxiom.extend(Abc)
            else:
                newaxiom.append(S)
                continue
        return impl(newaxiom, curr_n - 1)
    return impl(axiom, n)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
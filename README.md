# ulsys
"Micro" LSys. A small Python 3+ library for evaluating Lindenmayer-systems, with a small accompanying turtle implementation for pretty drawings.

ULSYS IS VERY MUCH PRE-ALPHA RIGHT NOW AND THE INTERFACE WILL LIKELY CHANGE A LOT.

## Current status
- [X] Reasonable Turtle API
- [X] PyX Turtle Backend
- [X] PoC Simple L-System implementation
- [X] Package partitioned after L-System type
- [ ] Stochastic L-System support
- [ ] Interopability with Python stdlib turtle package

## Goals 
These are the desired goals with the library. ulsys is not an attempt to write the most performant, most feature complete L-System evaluator, at least for now. But it strives to be simple to use and good enough for most scenarios.

### Primary goals
- Very simple to use and get running.
- Evaluating simple Lindenmayer systems (non-stochastic, non-parametric)
- A small Turtle implementation that easily supports different backends
- Easy to read code, to serve as an example implementation of an L-System evaluator.
- At least one vector graphics Turtle backend

### Secondary goals
- Performance
- Support for stochastic Lindenmayer systems

# Examples
![Koch Snowflake Vector Image](example.svg)

Use the included "Tri" Koch Snowflake and the PyX library turtle to create an
SVG file:

```python
import ulsys
from ulsys import standard
from ulsys import turtle

t = turtle.PyXTurtle()

syms = standard.evaluateSystem(
    "-F+F+F",
    standard.production("F->-F-F+F+F+F"),
    8)
actions = ulsys.triKochFlake.turtleActions

turtle.mapActions(syms, actions, t)

from pyx import canvas, path, style
c = canvas.canvas()
c.stroke(path.path(*t.paths), [style.linewidth(0.15), style.linestyle(d=style.dash([1,2]))])

with open("test.svg", "wb") as f:
    c.writeSVGfile(f)
```

## Platform
Python 3+

## License
MIT license. 

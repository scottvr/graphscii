# phart

phart: Python Hierarchical ASCII Representation Tool - A Pure Python graph visualization in ASCII, no external dependencies\*

(\* except NetworkX, which we should probably mention prominently. We just mean no dependencies of the Perl or PHP/webserver types.)

## Features

- Pure Python implementation
- No external dependencies (except NetworkX)
- Multiple node styles (square, round, diamond)
- Customizable edge characters
- Support for directed and undirected graphs
- Handles cycles and complex layouts
- Bidirectional edge support

## Installation

```bash
# not yet in Pypi so, from github:
pip install git+https://github.com/scottvr/phart

# or if you are reading this from where you cloned the repo:
pip install -e .
```

## Quick Start

```python
import networkx as nx
from phart import ASCIIRenderer

# Create a simple graph
G = nx.DiGraph()
G.add_edges_from([("A", "B"), ("A", "C"), ("B", "D")])

# Render it in ASCII
renderer = ASCIIRenderer(G)
print(renderer.render())

     [A]
      │
   v  │   v
  [B]────[C]
   │
   │  v
   ──[D]
```

The renderer shows edge direction using arrows:

- v : downward flow
- ^ : upward flow
- > or < : horizontal flow

These directional indicators are particularly useful for:

- Dependency graphs
- Workflow diagrams
- Process flows
- Any directed relationships

## Extras

- DOT file support
- requires pydot
  `pip install -r requirements\extra.txt`

### Example

    >>> dot = '''
    ... digraph {
    ...     A -> B
    ...     B -> C
    ... }
    ... '''
    >>> renderer = ASCIIRenderer.from_dot(dot)
    >>> print(renderer.render())
    A
    |
    B
    |
    C
    >>>

### Note on DOT format support:

---

PHART uses pydot for DOT format support. When processing DOT strings containing
multiple graph definitions, only the first graph will be rendered. For more
complex DOT processing needs, you can convert your graphs using NetworkX's
various graph reading utilities before passing them to PHART.

## License

MIT License

```

```

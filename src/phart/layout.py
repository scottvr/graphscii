"""Layout management for PHART ASCII graph rendering.

This module handles the calculation of node positions and edge routing
for ASCII graph visualization.
"""

from typing import Dict, Set, Tuple

import networkx as nx  # type: ignore

from .styles import LayoutOptions


class LayoutManager:
    """
    Manages the calculation of node positions and layout logic.

    This class handles the conversion of graph structure into a
    2D coordinate system suitable for ASCII rendering.

    Parameters
    ----------
    graph : NetworkX graph
        Graph to lay out
    options : LayoutOptions
        Layout configuration

    Notes
    -----
    The layout algorithm uses a hierarchical approach optimized for
    directed graphs and trees. For undirected graphs, a root node
    is chosen based on degree centrality.
    """

    def __init__(self, graph: nx.Graph, options: LayoutOptions):
        self.graph = graph
        self.options = options
        self.node_positions: Dict[str, Tuple[int, int]] = {}
        self.max_width = 0
        self.max_height = 0

    def _get_node_width(self, node: str) -> int:
        """Calculate display width of a node including decorators.

        Parameters
        ----------
        node : str
            Node identifier

        Returns
        -------
        int
            Total width of node when rendered
        """
        prefix, suffix = self.options.get_node_decorators(str(node))
        return len(str(node)) + len(prefix) + len(suffix)

    def calculate_layout(self) -> Tuple[Dict[str, Tuple[int, int]], int, int]:
        """
        Calculate node positions using hierarchical layout.

        Returns
        -------
        positions : dict
            Dictionary mapping nodes to (x, y) coordinates
        width : int
            Maximum width of the layout
        height : int
            Maximum height of the layout

        Notes
        -----
        The layout algorithm:
        1. Groups nodes into layers based on path length from roots
        2. Within each layer, spaces nodes evenly
        3. Centers each layer horizontally
        4. Maintains consistent vertical spacing between layers
        """
        if not self.graph:
            return {}, 0, 0

        # Group nodes by layer using path lengths from roots
        layers: Dict[int, Set[str]] = {}

        # Find root nodes
        if self.graph.is_directed():
            roots = [n for n, d in self.graph.in_degree() if d == 0]
        else:
            # For undirected, use highest degree node as root
            roots = [max(self.graph.nodes(), key=lambda n: self.graph.degree(n))]

        if not roots:  # Handle cycles by picking arbitrary start
            roots = [next(iter(self.graph.nodes()))]

        # Calculate distances using shortest paths
        distances: Dict[str, int] = {}
        for root in roots:
            lengths = nx.single_source_shortest_path_length(self.graph, root)
            for node, dist in lengths.items():
                distances[node] = max(distances.get(node, 0), dist)

        # Group nodes by layer
        for node, layer in distances.items():
            if layer not in layers:
                layers[layer] = set()
            layers[layer].add(node)

        # Handle disconnected components
        unreached = set(self.graph.nodes()) - set(distances)
        if unreached:
            max_layer = max(layers.keys()) if layers else 0
            layers[max_layer + 1] = unreached

        # Calculate layout dimensions
        self.max_height = (max(layers.keys()) + 1) * (self.options.layer_spacing + 1)

        # Calculate layer widths
        layer_widths = {}
        for layer, nodes in layers.items():
            total_width = sum(self._get_node_width(n) for n in nodes)
            min_spacing = (len(nodes) - 1) * self.options.node_spacing
            layer_widths[layer] = total_width + min_spacing

        self.max_width = max(layer_widths.values()) + 4  # Add margins

        # Assign positions
        for layer, nodes in layers.items():
            y = layer * (self.options.layer_spacing + 1)
            total_width = layer_widths[layer]
            start_x = (self.max_width - total_width) // 2
            current_x = start_x

            for node in sorted(nodes):  # Sort for consistent layout
                self.node_positions[node] = (current_x, y)
                current_x += self._get_node_width(node) + self.options.node_spacing

        return self.node_positions, self.max_width, self.max_height

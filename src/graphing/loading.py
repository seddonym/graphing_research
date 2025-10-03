import networkx as nx
from pathlib import Path
import json


def load_graph_from_file(path: Path) -> nx.DiGraph:
    """
    Return a graph representing a Python codebase, saved by the script in saving.py.
    """
    graph_data = json.loads(path.read_text())
    return nx.node_link_graph(graph_data, edges="edges")

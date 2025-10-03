import grimp
import networkx
from pathlib import Path
import json


def hash_module_if_salt(module_name: str, salt: str):
    segments = module_name.split(".")
    return ".".join(hash_segment_if_salt(segment, salt) for segment in segments)


def hash_segment_if_salt(segment: str, salt: str):
    if salt:
        import hashlib

        combined = f"{segment}:{salt}"
        hash_value = int(hashlib.sha256(combined.encode()).hexdigest(), 16)
        return str(hash_value % 10**11)
    return segment


def save(package: str, destination: Path, hash_salt: str) -> networkx.DiGraph:
    grimp_graph = grimp.build_graph(package)

    # Build a NetworkX graph from the Grimp graph.
    networkx_graph = networkx.DiGraph()
    for module in grimp_graph.modules:
        hashed_module = hash_module_if_salt(module, hash_salt)
        networkx_graph.add_node(hashed_module)
        for imported in grimp_graph.find_modules_directly_imported_by(module):
            hashed_imported = hash_module_if_salt(imported, hash_salt)
            networkx_graph.add_edge(hashed_module, hashed_imported)

    graph_data = networkx.node_link_data(networkx_graph, edges="edges")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(graph_data, indent=2))

    return networkx_graph

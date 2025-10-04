import networkx as nx
import typer
from typing import Annotated
from pathlib import Path
from . import saving, loading

app = typer.Typer()


@app.command()
def save(
    package: Annotated[str, typer.Option()],
    destination: Annotated[Path, typer.Option()],
    hash_salt: Annotated[str, typer.Option()] = "",
) -> None:
    graph = saving.save(package, destination, hash_salt)

    if hash_salt:
        print(f"Saved to {destination} (hashed names).")
    else:
        print(f"Saved to {destination} (unhashed names).")

    _print_graph_summary(graph)


@app.command()
def load(source: Path) -> None:
    graph = loading.load_graph_from_file(source)
    _print_graph_summary(graph)


def _print_graph_summary(graph: nx.DiGraph) -> None:
    print("First few nodes:")
    for i, node in enumerate(graph.nodes):
        if i > 5:
            break
        print(f" - {node}")

    print("First few edges:")
    for i, edge in enumerate(graph.edges):
        if i > 5:
            break
        print(f" - {edge}")

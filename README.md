# Helpers for researching Python codebase graphs

Python code bases can be represented as a directed graphs, with the nodes being modules
and the edges being imports from one module to another.

This repo provides tooling to export existing codebase graphs to JSON files, and a Python API to load them.

Optionally, the module names can be obfuscated using a hash and salt. Note that each segment of the module
name is separately hashed, so `74185739980.87970842061` will be a child of `74185739980`.

## System requirements

`uv`: https://docs.astral.sh/uv/getting-started/installation/

(Note: using uv means you don't need to activate virtual environments, all commands can be run from this repository's directory.)

## How to use

### Saving the graph of an existing Python package

```
uv run app save --package=SOME_PACKAGE \
  --destination=./exports/FILENAME.json
```

To hash the names, pass an arbitrary string as a hash salt: 

```
uv run app save --package=PACKAGE \
  --destination=./exports/FILENAME.json --hash-salt=SALT
```

#### Example

This will analyze the `importlib` package and save it in `importlib.json`, using `some-salt` as a salt.

```
uv run app save --package=importlib \
 --destination=./exports/importlib.json --hash-salt=some-salt
```

#### Package importability

The passed package _must be importable_, i.e. on the Python path. For example, this will not work, as flask is not installed.

```
uv run app save --package=flask \
  --destination=./exports/flask.json
```

You have two options here:

1. If the package is installable, you can add the package using the command `uv add PACKAGE` first.
2. If it is in a project directory elsewhere on your computer, provide this directory as part of the `PYTHONPATH` environment variable when you run the command, e.g.:

```
PYTHONPATH="/path/to/directory:$PYTHONPATH" \
  uv run app save \
  --package=mypackage --destination=./exports/mypackage.json
```

### Loading the graph

Most likely you will want to load the networkx graph in Python. You can do this by calling `uv run python` and then:

```
>>> from pathlib import Path
>>> from graphing import loading
>>> graph = loading.load_graph_from_file(Path("./exports/FILENAME.json"))
>>> graph
<networkx.classes.digraph.DiGraph object at 0x1019f9640>
```

You can also load the graph from the command line, and print a summary, like this:

```
uv run app load ./exports/FILENAME.json
```

# Inheritance and DFS

## Inheritance

Paste and run the following code in a new python notebook called `debug.ipynb` in your mp4 folder:

```python
class Parent:
    def twice(self):
        self.message()
        self.message()
        
    def message(self):
        print("parent says hi")
        
class Child:
    def message(self):
        print("child says hi")
        
c = Child()
```

Modify `Child` so that it inherits from `Parent`.

What do you think will be printed if you call `c.twice()`?  Discuss
with your group, then run it to find out.

When `self.some_method(...)` is called, and there are multiple methods
named `some_method` in your program, the type of `self` (the original object that is calling the method from the class) is what
matters for determining which one runs.  It doesn't matter where the
`self.some_method(...)` is (could be any method).

## scrape.py

For this portion of the lab you are going to work on `scrape.py` in MP4, so make sure that you are in the correct branch before starting.

## GraphSearcher

Take a look and read over the starter code for the `GraphSearcher` class in `scrape.py`.

The graphs we search on for this project come in many shapes and formats (e.g. matrices, files or web), but it would be nice if we could use the same depth-first search (DFS) code when we want to search different kinds of graphs.  Therefore, we would like to implement a base class `GraphSearcher` and implement the DFS algorithm in it. This is also why visit_and_get_children will need to be different for each child class, as the parent-child relationship is defined in different ways for each type format.

For our purposes, we aren't using DFS to find a specific path.  We just want to see what nodes are reachable from a given starting `node`, so these methods don't need to return any value.  Your job is to replace the comments in `dfs_search` and `dfs_visit` with code (some comments may require a couple lines of code).

The `dfs_visit` method will call `visit_and_get_children` to record the node value and determine the children of a given node. Subclasses of `GraphSearcher` can override `visit_and_get_children` to lookup the children of a node in different kinds of graphs (e.g. matrices, files or web).

Try your code:

```python
g = GraphSearcher()
g.dfs_search("A")
```

You should get an exception.  The purpose of `GraphSearcher` is not to
directly create objects, it is to let other clases inherit `dfs_search` (we'll do the inheritance soon).

**Note:** Do not worry about `bfs_search` yet, you are going to work on this one later.

## Matrix Format

Paste and run the following in your debug notebook:

```python
import pandas as pd

df = pd.DataFrame([
    [0,1,0,1],
    [0,0,1,0],
    [0,0,0,1],
    [0,0,1,0],
], index=["A", "B", "C", "D"], columns=["A", "B", "C", "D"])
df
```

A grid of ones and zeros like this is a common way to represent
directed graphs.  A `1` in the "C" column of the "B" row means that
there is an edge from node B to node C.

Try drawing a directed graph on a piece of paper based on the above
grid.

`df.loc["????"]` looks up a row in a DataFrame.  Use it to lookup the
children of node B.

Complete the following to print all the children of "B" (should only be "C"):

```python
for node, has_edge in df.loc["B"].items():
    if ????:
        print(????)
```

Let's now work on the `GraphSearcher` class which deals with
graphs represented as matrices.

Complete the `TODO`s.  Test it, checking what nodes are reachable from each starting point:

```python
m = MatrixSearcher(df)
m.dfs_search(????)
m.order
```

From "A", for example, `m.order` should be `['A','B', 'C', 'D']`.  Look
back at the picture you drew of the graph and make sure you're getting
what you expect when starting from other nodes.

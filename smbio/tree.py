"""Utility functions for NetworkX graphs and digraphs."""


def roots_iter(G):
    """
    Return an iterator over the roots of a digraph.

    Use common sense!  If the graph is undirected, the term "root" doesn't make
    sense.  If there are cycles in the DiGraph, there may be no roots!
    Finally, there may also be multiple roots.

    A root is defined as any node with no incoming edges (note that this may
    not be how your tree is represented -- I like thinking of parents
    "pointing" towards their children, but some people do the opposite).

    :param networkx.DiGraph G: graph to find roots of
    :return: iterator yielding roots
    """
    return (v for v, d in G.in_degree_iter() if d == 0)


def roots(G):
    """
    Return a list of the roots of a digraph (see roots_iter).

    :param networkx.DiGraph G: graph to find roots of
    :return: list of roots
    """
    return list(roots_iter(G))


def root(T):
    """
    Return *the* root of tree T.

    Unlike the roots* functions, this function assumes that T is a tree, and
    therefore has only one root.  It will return exactly one node, and it will
    raise an exception if there is more or less than one root.

    :param networkx.DiGraph G: graph to find root of
    :return: a single root
    :raises RuntimeError: When there is more than one root.
    """
    root_list = roots(T)
    if len(root_list) != 1:
        raise RuntimeError('root: given tree does not have exactly 1 root')
    return root_list[0]

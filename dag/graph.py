""""""

from abc import ABC

from dag.singleton import SingletonABC


class ExprGraph(ABC, metaclass=SingletonABC):
    """A graph data structure for expressions."""
    pass

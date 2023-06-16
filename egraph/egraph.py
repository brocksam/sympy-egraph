"""The eqivalence graph data structure."""

from typing import Iterable, TypeVar

from .core import Node
from .rewrite import RewriteRule
from .union_find import UnionFind


TNodeOrIterableNode = TypeVar("T", Node, Iterable[Node])


class EClass:
    """
    - an array of terms in the class
    - an array of possible parent terms for efficiently propagating congruences
    """

    def __init__(self, expr):
        self.exprs = []
        self.add(expr)

    def add(self, exprs):
        if isinstance(exprs, Node):
            exprs = [exprs]
        for expr in exprs:
            if expr in self:
                continue
            self.exprs.append(expr)

    def __len__(self):
        return len(self.exprs)

    def __contains__(self, expr):
        return expr in self.exprs

    def __str__(self):
        return f"{self.__class__.__name__}()"

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class EGraph:
    """
    node_to_eclass_id_mapping: dict[Node, int]
        A map from hash-consed terms to class ids
    eclass_id_to_eclass_mapping: dict[id, EClass]
        A map from class-ids to equivalence classes
    eclass_id_union_find: UnionFind
        A unionfind data structure on class ids
    """

    def __init__(self, exprs: Node | Iterable[Node] | None = None) -> None:
        self.eclasses = []
        if exprs is not None:
            self.add(exprs)

    def add(self, exprs: Node | Iterable[Node]) -> None:
        if isinstance(exprs, Node):
            exprs = [exprs]
        for expr in exprs:
            if expr in self:
                continue
            eclass = EClass(expr)
            self.eclasses.append(eclass)

    def saturate(self, *, rewrite_rules: Iterable[RewriteRule] = None) -> None:
        pass

    def extract(
        self, exprs: TNodeOrIterableNode, *, objective: None = None, cost: None = None
    ) -> TNodeOrIterableNode:
        pass

    @property
    def number_eclasses(self):
        return len(self.eclasses)

    def __len__(self):
        return len(self.eclasses)

    def __contains__(self, item):
        if isinstance(item, Node):
            return any(item in eclass for eclass in self.eclasses)
        elif isinstance(item, EClass):
            return item in self.eclasses
        msg = f"Can only check membership of `Node` and `EClass` objects not {type(item)}."
        raise TypeError(msg)

    def __str__(self):
        return f"{self.__class__.__name__}()"

    def __repr__(self):
        return f"{self.__class__.__name__}()"

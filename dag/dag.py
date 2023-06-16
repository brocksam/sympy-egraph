""""""

from __future__ import annotations

import weakref

import sympy as sm

from dag.graph import ExprGraph


class DirectedAcyclicGraph(ExprGraph):

    _cache = set()

    def add_expression(self, expr: sm.Expr | DagExpr) -> DagExpr:
        if expr in self:
            return expr
        elif isinstance(expr, sm.Symbol):
            dag_expr = DagSymbol(expr)
            self._cache.add(dag_expr)
        return dag_expr

    def __contains__(self, item) -> bool:
        return item in self._cache


def _sort_args(args):
    tuple(sorted((_dagify(arg) for arg in args), key=sm.core.add._args_sortkey))
    return sorted_args


class DagNode:

    _cache = weakref.WeakValueDictionary()
    _dag = DirectedAcyclicGraph()

    def __call__(cls, *args, **kwargs):
        args = _sort_args(args)
        if args not in self._cache:
            obj = super().__call__(*args, **kwargs)
            self._cache[args] = obj
        return self._cache[args]

    @property
    def dag(self) -> DirectedAcyclicGraph:
        return self._dag

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __add__(self, other):
        return DagAdd(self, other)


class DagSymbol(DagNode, sm.Symbol):

    def __new__(cls, symbol: sm.Symbol) -> DagSymbol:
        if not isinstance(symbol, sm.Symbol):
            msg = (
                f'Value {symbol} passed to `symbol` argument is a '
                f'{type(symbol)}, must be a {sm.Symbol}.'
            )
            raise TypeError(msg)
        instance = super().__new__(cls, symbol.name)
        instance._hash = hash(symbol.name)
        cls._dag._cache.add(instance)
        return instance

    def __init__(self, symbol: sm.Symbol) -> None:
        self._symbol = symbol

    @property
    def symbol(self) -> sm.Symbol:
        return self._symbol


class DagExpr(DagNode, sm.Expr):

    _is_associative = False

    def __new__(cls, *args):
        instance = super().__new__(cls, *args)
        instance._hash = hash(args)
        cls._dag._cache.add(instance)
        return instance

    def __init__(self):
        pass


class DagAdd(DagExpr, sm.Add):

    def __init__(self, *args):
        self._args = tuple(sorted((_dagify(arg) for arg in args), key=sm.core.add._args_sortkey))

    @property
    def args(self):
        return self._args


class DagMul(DagExpr, sm.Mul):
    pass


class DagPow(DagExpr, sm.Pow):
    pass


class DagExp(DagExpr, sm.exp):
    pass


class DagSin(DagExpr, sm.sin):
    pass


_DAG_SINGLETON = DirectedAcyclicGraph()

def _dagify(expr: Expr | DagExpr) -> DagNode:
    if expr in _DAG_SINGLETON:
        return expr
    dag_func = SYMPY_EXPR_TO_DAG_EXPR_MAPPING.get(expr.func)
    if dag_func == DagSymbol:
        return dag_func(expr)
    dag_args = expr.args
    return dag_func(*dag_args)


SYMPY_EXPR_TO_DAG_EXPR_MAPPING = {
    sm.Symbol: DagSymbol,
    sm.Add: DagAdd,
    sm.Mul: DagMul,
    sm.Pow: DagPow,
    sm.exp: DagExp,
    sm.sin: DagSin,
}


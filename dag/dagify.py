""""""

from __future__ import annotations

from typing import TYPE_CHECKING

import sympy as sm

from dag.dag import DirectedAcyclicGraph

if TYPE_CHECKING:
    from dag.dag import DagExpr


def dagify(expr: sm.Expr) -> DagExpr:
    dag = DirectedAcyclicGraph()
    return dag.add_expression(expr)

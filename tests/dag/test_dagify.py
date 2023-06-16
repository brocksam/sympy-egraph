"""Tests for the ``dagify`` function."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
import sympy as sm
import sympy.physics.mechanics as me

from dag.dag import DagSymbol
from dag.dagify import dagify

if TYPE_CHECKING:
    from dag.dag import DagExpr


class TestDagify:

    @staticmethod
    @pytest.mark.parametrize(
        'expr, expected',
        [
            (sm.Symbol('x'), DagSymbol(sm.Symbol('x'))),
        ]
    )
    def test_dagify(expr: sm.Base, expected: DagExpr):
        dag_expr = dagify(expr)
        assert dag_expr == expected


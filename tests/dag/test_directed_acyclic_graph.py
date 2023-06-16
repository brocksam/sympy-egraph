"""Tests for the ``DirectedAcyclicGraph`` singleton class."""

from __future__ import annotations

import pytest
import sympy as sm
import sympy.physics.mechanics as me

from dag import DagAdd, DagSymbol, DirectedAcyclicGraph


class TestDagSymbol:

    @staticmethod
    def test_instantiate_symbol():
        x_sm = sm.Symbol('x')
        x_dag = DagSymbol(x_sm)
        assert hasattr(x_dag, 'symbol')
        assert x_dag.symbol == x_sm
        assert isinstance(x_dag, sm.Symbol)
        assert x_dag.name == x_sm.name

    @staticmethod
    def test_instance_is_singleton():
        x_dag_1 = DagSymbol(sm.Symbol('x'))
        x_dag_2 = DagSymbol(sm.Symbol('x'))
        assert x_dag_1 is x_dag_2

class TestDagAdd:

    @pytest.fixture(autouse=True)
    def _fixture(self):
        self.x_sm = sm.Symbol('x')
        self.y_sm = sm.Symbol('y')
        self.z_sm = sm.Symbol('z')
        self.x_dag = DagSymbol(self.x_sm)
        self.y_dag = DagSymbol(self.y_sm)
        self.z_dag = DagSymbol(self.z_sm)

    @pytest.mark.parametrize(
        'args',
        [
            (sm.Symbol('x'), sm.Symbol('y')),
            (sm.Symbol('y'), sm.Symbol('x')),
            (DagSymbol(sm.Symbol('x')), DagSymbol(sm.Symbol('y'))),
            (DagSymbol(sm.Symbol('y')), DagSymbol(sm.Symbol('x'))),
            (sm.Symbol('x'), DagSymbol(sm.Symbol('y'))),
            (sm.Symbol('y'), DagSymbol(sm.Symbol('x'))),
            (DagSymbol(sm.Symbol('x')), sm.Symbol('y')),
            (DagSymbol(sm.Symbol('y')), sm.Symbol('x')),
        ]
    )
    def test_binary_add_is_commutative(self, args):
        x_plus_y_dag = DagAdd(*args)
        assert isinstance(x_plus_y_dag, DagAdd)
        assert x_plus_y_dag.func == DagAdd
        assert x_plus_y_dag.args == (self.x_dag, self.y_dag)

    def test_is_cached(self):
        x_plus_y_dag = DagAdd(self.x_dag, self.y_dag)
        for k,v in DagSymbol._cache:
            print(k, v)
        assert x_plus_y_dag is DagAdd(self.y_dag, self.x_dag)

    @pytest.mark.parametrize(
        'args',
        [
            (sm.Symbol('x'), sm.Symbol('y'), sm.Symbol('z')),
        ]
    )
    def test_multiary_add_is_commutative_and_cached(self, args):
        x_plus_y_plus_z_dag = DagAdd(*args)
        assert isinstance(x_plus_y_plus_z_dag, DagAdd)
        assert x_plus_y_plus_z_dag.func == DagAdd
        assert x_plus_y_plus_z_dag.args == (self.x_dag, self.y_dag, self.z_dag)


class TestDagExpr:

    @staticmethod
    def test_baby_example():
        x1 = sm.Symbol('x1')
        x2 = sm.Symbol('x2')

        w0 = x2**(-1)
        w1 = sm.exp(x2)
        w2 = x1 * w0
        w3 = -1 * w1
        w4 = w2 + w3
        w5 = sm.sin(w2)
        w6 = w4 + w5
        w7 = w4 * w6

        expr = (sm.sin(x1/x2) + (x1/x2) - sm.exp(x2)) * ((x1/x2) - sm.exp(x2))


class TestDirectedAcyclicGraph:

    @staticmethod
    def test_is_singleton():
        dag_1 = DirectedAcyclicGraph()
        dag_2 = DirectedAcyclicGraph()
        assert dag_2 is dag_1

"""Test module for prototype directed acyclic graph (DAG) implementation."""

import sympy as sm
import pytest

import egraph


@pytest.mark.skip
def test_cache_commutative_args():
    a = sm.Symbol("a")
    b = sm.Symbol("b")
    c = sm.Symbol("c")

    assert egraph.Dag(a * b) == egraph.Dag(b * a)
    assert egraph.Dag(a + b) == egraph.Dag(b + a)
    assert egraph.Dag((a * b) * (b * a)) == egraph.Dag((b * a) * (b * a))


@pytest.mark.skip
def test_griewank_baby_example_dag():
    x1 = sm.Symbol("x1")
    x2 = sm.Symbol("x2")

    y = (sm.sin(x1 / x2) + (x1 / x2) - sm.exp(x2)) * ((x1 / x2) - sm.exp(x2))

    dag = egraph.Dag(y)

    print(dag)

    expected_nodes = {

    }

    assert False

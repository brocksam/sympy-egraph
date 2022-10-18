"""Tests for the drop-in replacement of SymPy's `Symbol` class."""


import pytest
from hypothesis import given, strategies as st

import egraph


def test_symbol_str_and_repr():
    a = egraph.Symbol("a")
    assert str(a) == "a"
    assert repr(a) == "Symbol('a')"


def test_symbol_caching():
    a = egraph.Symbol("a")
    assert a is egraph.Symbol("a")
    assert egraph.Symbol("b") is egraph.Symbol("b")


@given(st.integers() | st.floats())
def test_number_symbols_invalid(value):
    with pytest.raises(ValueError):
        _ = egraph.Symbol(value)


def test_integer_caching():
    zero = egraph.Integer(0)
    assert zero is egraph.Integer(0)
    assert egraph.Integer(1) is egraph.Integer(1)


def test_integer_str_repr():
    zero = egraph.Integer(0)
    assert str(zero) == "0"
    assert repr(zero) == "Integer(0)"


@given(
    st.floats(min_value=0.0, exclude_min=True)
    | st.floats(max_value=0.0, exclude_max=True)
)
def test_floating_point_integers_invalid(value):
    with pytest.raises(ValueError):
        _ = egraph.Integer(value)

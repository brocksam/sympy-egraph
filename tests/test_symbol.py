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
    assert egraph.Symbol("a") is egraph.Symbol("a")


@given(st.integers() | st.floats())
def test_number_symbols_invalid(value):
    with pytest.raises(ValueError):
        _ = egraph.Symbol(value)


def test_integer_str_repr():
    zero = egraph.Integer(0)
    assert str(zero) == "0"
    assert repr(zero) == "Integer(0)"


@given(st.complex_numbers() | st.floats() | st.fractions())
def test_non_integer_integers_invalid(value):
    with pytest.raises(ValueError):
        _ = egraph.Integer(value)

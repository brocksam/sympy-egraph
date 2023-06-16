"""Tests for rewrite rules."""

import pytest

from egraph import EGraph, Integer, Symbol


class TestRewriteRulesBasic:

    @pytest.mark.skip
    def test_factor(self):
        a = Symbol("a")
        b = Symbol("b")
        c = Symbol("c")

        expr = a*b + a*c
        expect = a*(b + c)

        egraph = EGraph()
        egraph.add(expr)
        egraph.saturate()

        assert expect in egraph
        assert egraph.extract(expr) == expect

    @pytest.mark.skip
    def test_expand(self):
        a = Symbol("a")
        b = Symbol("b")
        c = Symbol("c")

        expr = a*(b + c)
        expect = a*b + a*c

        egraph = EGraph()
        egraph.add(expr)
        egraph.saturate()

        assert expect in egraph
        assert egraph.extract(expr) == expr

    @pytest.mark.skip
    def test_constant_folding(self):
        zero = Integer(0)
        one = Integer(1)
        two = Integer(2)
        three = Integer(3)
        four = Integer(4)
        five = Integer(5)
        six = Integer(6)

        egraph = EGraph()
        egraph.add(zero + one + two + three)
        egraph.saturate()
        assert egraph.extract(zero + one) == one
        assert egraph.extract(zero + two) == two
        assert egraph.extract(zero + three) == three
        assert egraph.extract(one + two) == three
        assert egraph.extract(one + three) == four
        assert egraph.extract(two + three) == five
        assert egraph.extract(zero + one + two) == three
        assert egraph.extract(zero + one + three) == four
        assert egraph.extract(zero + two + three) == five
        assert egraph.extract(one + two + three) == six
        assert egraph.extract(zero + one + two + three) == six

    @pytest.mark.skip
    def test_symbol_add_zero(self):
        x = Symbol("x")
        zero = Integer(0)

        egraph = EGraph()
        egraph.add(x + zero)
        egraph.saturate()
        assert egraph.extract(x + zero) == x

    @pytest.mark.skip
    def test_multiply_by_zero(self):
        pass

    @pytest.mark.skip
    def test_multiply_by_one(self):
        pass


@pytest.mark.skip
def test_simplify_case_1():
    """Test rewriting `(x**2 + x) / x`, which can be nicely simplified.
    
    One possible simplification path using rewrite rules is:
    -> (x**2 + x) / x
    Apply: a**2 -> a*a
    -> (x*x + x) / x
    Apply: a -> a*1
    -> (x*x + x*1) / x
    Apply: a*b + a*c -> a*(b + c)
    -> (x*(x + 1)) / x
    Apply: (a * b) / c -> a * (b / c)
    -> x * ((x + 1) / x)
    Apply: a * (b / c) -> (a / c) * b
    -> (x / x) * (x + 1)
    Apply: a / a -> 1
    -> 1 * (x + 1)
    Apply: 1 * a -> a
    -> x + 1

    """
    x = Symbol("x")
    
    expr = (x**2 + x) / x
    expect = x + 1

    egraph = EGraph()
    egraph.add(expr)
    egraph.saturate()

    assert egraph.extract(expr) == expect


@pytest.mark.skip
def test_simplify_case_2():
    pass

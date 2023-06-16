"""Tests for operations."""


import pytest

from egraph import Add, Integer, Mul, Symbol


class TestAdd:

    @pytest.fixture(autouse=True)
    def initialise(self):
        self.x = Symbol("x")
        self.y = Symbol("y")
        self.zero = Integer(0)
        self.one = Integer(1)

    def test_add_symbol_instance_and_symbol_instance(self):
        x_add_y = self.x + self.y
        y_add_x = self.y + self.x
        assert isinstance(x_add_y, Add)
        assert isinstance(y_add_x, Add)
        assert x_add_y == y_add_x
        assert x_add_y is y_add_x
        assert str(x_add_y) == "x+y"
        assert repr(x_add_y) == "Add(Symbol('x'), Symbol('y'))"

    def test_add_symbol_instance_and_integer_instance(self):
        x_add_zero = self.x + self.zero
        zero_add_x = self.zero + self.x
        assert isinstance(x_add_zero, Add)
        assert isinstance(zero_add_x, Add)
        assert x_add_zero == zero_add_x
        assert x_add_zero is zero_add_x
        assert str(x_add_zero) == "0+x"
        assert repr(x_add_zero) == "Add(Integer(0), Symbol('x'))"

    def test_add_symbol_instance_and_int(self):
        x_add_zero = self.x + self.zero
        assert isinstance(self.x + 0, Add)
        assert isinstance(0 + self.x, Add)
        assert self.x + 0 == x_add_zero
        assert 0 + self.x == x_add_zero
        assert str(self.x + 0) == "0+x"
        assert repr(self.x + 0) == "Add(Integer(0), Symbol('x'))"

    def test_add_integer_instance_and_integer_instance(self):
        zero_add_one = self.zero + self.one
        one_add_zero = self.one + self.zero
        assert isinstance(zero_add_one, Add)
        assert isinstance(one_add_zero, Add)
        assert zero_add_one == one_add_zero
        assert zero_add_one is one_add_zero
        assert str(zero_add_one) == "0+1"
        assert repr(zero_add_one) == "Add(Integer(0), Integer(1))"


@pytest.mark.skip
class TestSub:
    pass


@pytest.mark.skip
class TestNeg:
    pass


@pytest.mark.skip
class TestMul:

    @pytest.fixture(autouse=True)
    def initialise(self):
        self.x = Symbol("x")
        self.y = Symbol("y")
        self.zero = Integer(0)
        self.one = Integer(1)

    def test_mul_symbol_instance_and_symbol_instance(self):
        x_mul_y = self.x * self.y
        y_mul_x = self.y * self.x
        assert isinstance(x_mul_y, Mul)
        assert isinstance(y_mul_x, Mul)
        assert x_mul_y == y_mul_x
        assert x_mul_y is y_mul_x
        assert str(x_mul_y) == "x*y"
        assert repr(x_mul_y) == "Mul(Symbol('x'), Symbol('y'))"

    def test_mul_symbol_instance_and_integer_instance(self):
        x_mul_zero = self.x * self.zero
        zero_mul_x = self.zero * self.x
        assert isinstance(x_mul_zero, Mul)
        assert isinstance(zero_mul_x, Mul)
        assert x_mul_zero == zero_mul_x
        assert x_mul_zero is zero_mul_x
        assert str(x_mul_zero) == "0*x"
        assert repr(x_mul_zero) == "Mul(Integer(0), Symbol('x'))"

    def test_mul_symbol_instance_and_int(self):
        x_mul_zero = self.x * self.zero
        assert isinstance(self.x * 0, Mul)
        assert isinstance(0 * self.x, Mul)
        assert self.x * 0 == x_mul_zero
        assert 0 * self.x == x_mul_zero
        assert str(self.x * 0) == "0*x"
        assert repr(self.x * 0) == "Mul(Integer(0), Symbol('x'))"

    def test_mul_integer_instance_and_integer_instance(self):
        zero_mul_one = self.zero * self.one
        one_mul_zero = self.one * self.zero
        assert isinstance(zero_mul_one, Mul)
        assert isinstance(one_mul_zero, Mul)
        assert zero_mul_one == one_mul_zero
        assert zero_mul_one is one_mul_zero
        assert str(zero_mul_one) == "0*1"
        assert repr(zero_mul_one) == "Mul(Integer(0), Integer(1))"


class TestDiv:
    pass


class TestRecip:
    pass


class TestPow:
    pass


class TestSqrt:
    pass

import pytest
import sympy as sym


@pytest.fixture
def griewank_baby_example():
    """Benchmark fixture using the baby example from Griewank & Walther, 2008."""
    x1 = sym.Symbol("x1")
    x2 = sym.Symbol("x2")

    y = (sym.sin(x1 / x2) + (x1 / x2) - sym.exp(x2)) * ((x1 / x2) - sym.exp(x2))
    
    return y


@pytest.fixture
def griewank_baby_example_cse():
    """Expected result from SymPy's CSE on the baby example."""
    x0 = sym.Symbol("x0")
    x1 = sym.Symbol("x1")
    x2 = sym.Symbol("x2")
    x3 = sym.Symbol("x3")

    cse = [
        (x0, x1 / x2),
        (x3, x0 - sym.exp(x2)),
    ]
    expr = [
        x3 * (x3 + sym.sin(x0)),
    ]

    return (cse, expr)


@pytest.fixture
def griewank_baby_example_jacobian():
    """Expected Jacobian for the baby example."""
    x1 = sym.Symbol("x1")
    x2 = sym.Symbol("x2")

    G = sym.Matrix([[
        (x1 / x2 - sym.exp(x2)) * (sym.cos(x1 / x2) / x2 + 1 / x2) + (x1 / x2 - sym.exp(x2) + sym.sin(x1 / x2)) / x2,
        (-x1 / x2**2 - sym.exp(x2)) * (x1 / x2 - sym.exp(x2) + sym.sin(x1 / x2)) + (x1 / x2 - sym.exp(x2)) * (-x1 * sym.cos(x1 / x2) / x2**2 - x1 / x2**2 - sym.exp(x2)),
    ]])

    return G


@pytest.fixture
def griewank_baby_example_jacobian_cse():
    """Expected result from SymPy's CSE on the baby example's Jacobian."""
    x0 = sym.Symbol("x0")
    x1 = sym.Symbol("x1")
    x2 = sym.Symbol("x2")
    x3 = sym.Symbol("x3")
    x4 = sym.Symbol("x4")
    x5 = sym.Symbol("x5")
    x6 = sym.Symbol("x6")
    x7 = sym.Symbol("x7")
    x8 = sym.Symbol("x8")
    x9 = sym.Symbol("x9")

    cse = [
        (x0, 1 / x2),
        (x3, x0 * x1),
        (x4, sym.exp(x2)),
        (x5, x3 - x4),
        (x6, x5 + sym.sin(x3)),
        (x7, sym.cos(x3)),
        (x8, x1 / (x2 ** 2)),
        (x9, x4 + x8),
    ]
    expr = [
        sym.Matrix([[x0 * x6 + x5 * (x0 * x7 + x0), x5 * (-x7 * x8 - x9) - x6 * x9]])
    ]

    return (cse, expr)


def test_benchmark_griewank_baby_example_cse(
    benchmark,
    griewank_baby_example,
    griewank_baby_example_cse,
):
    result = benchmark(sym.cse, griewank_baby_example)
    assert result == griewank_baby_example_cse


def test_benchmark_griewank_baby_example_jacobian(
    benchmark,
    griewank_baby_example,
    griewank_baby_example_jacobian,
):
    x1 = sym.Symbol("x1")
    x2 = sym.Symbol("x2")

    x = sym.Matrix([x1, x2])
    y = sym.Matrix([griewank_baby_example])

    result = benchmark(y.jacobian, x)
    assert result == griewank_baby_example_jacobian


def test_benchmark_griewank_baby_example_jacobian_cse(
    benchmark,
    griewank_baby_example,
    griewank_baby_example_jacobian_cse,
):

    def jacobian_cse(expr, wrt):
        return sym.cse(expr.jacobian(wrt))

    x1 = sym.Symbol("x1")
    x2 = sym.Symbol("x2")

    x = sym.Matrix([x1, x2])
    y = sym.Matrix([griewank_baby_example])

    result = benchmark(jacobian_cse, y, x)
    assert result == griewank_baby_example_jacobian_cse



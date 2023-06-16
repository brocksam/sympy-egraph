import sympy as sym
import pytest

from egraph import Integer, EGraph


@pytest.mark.skip
def test_instantiate_empty_egraph():
    egraph = EGraph()
    assert isinstance(egraph, EGraph)


@pytest.mark.skip
class TestEGraphInteger:

    @pytest.fixture(autouse=True)
    def initialise(self):
        self.zero = Integer(0)
        self.one = Integer(1)
        self.two = Integer(2)
        self.three = Integer(3)
        self.four = Integer(4)
        self.five = Integer(5)
        self.six = Integer(6)

    def test_instantiate_egraph_with_integer_instance(self):
        egraph = EGraph(self.zero)
        assert egraph.number_eclasses == 1
        assert self.zero in egraph
        assert self.one not in egraph

    def test_add_integer_eclass(self):
        egraph = EGraph()
        egraph.add(self.zero)
        assert egraph.number_eclasses == 1
        assert self.zero in egraph
        assert self.one not in egraph

        egraph = EGraph()
        egraph.add(self.zero)
        egraph.add([self.one, self.two])
        assert egraph.number_eclasses == 3
        assert self.zero in egraph
        assert self.one in egraph
        assert self.two in egraph

    def test_add_same_integer_instance_multiple_times(self):
        egraph = EGraph(self.zero)
        assert egraph.number_eclasses == 1
        assert self.zero in egraph

        egraph = EGraph([self.zero, self.zero])
        assert egraph.number_eclasses == 1
        assert self.zero in egraph

        egraph = EGraph()
        egraph.add(self.zero)
        egraph.add(self.zero)
        egraph.add([self.zero, self.zero])
        assert egraph.number_eclasses == 1
        assert self.zero in egraph

    def test_union_of_equal_integer_instances_and_integer_expression_instances(self):
        egraph = EGraph([self.zero, self.one, self.two])
        assert egraph.number_eclasses == 3

        egraph.add(self.zero + self.one)
        assert egraph.number_eclasses == 4
        
        egraph.add(self.zero + self.two)
        assert egraph.number_eclasses == 5

        egraph.add(self.one + self.two)
        assert egraph.number_eclasses == 6

        assert self.three not in egraph
        egraph.saturate()
        assert self.three in egraph
        
        assert egraph.extract(self.zero + self.one + self.two) == self.three


@pytest.mark.skip
def test_egraph_cache_commutative_args():
    a = sym.Symbol("a")
    b = sym.Symbol("b")

    assert egraph.EGraph(a * b) == egraph.EGraph(b * a)
    assert egraph.EGraph(a + b) == egraph.EGraph(b + a)
    assert egraph.EGraph((a * b) * (b * a)) == egraph.Dag((b * a) * (b * a))


@pytest.mark.skip
def test_egraph_cache_associative_add():
    a = sym.Symbol("a")
    b = sym.Symbol("b")
    b = sym.Symbol("c")

    assert egraph.EGraph((a + b) + c) == egraph.EGraph(a + (b + c))


@pytest.mark.skip
def test_egraph_cache_associative_mul():
    a = sym.Symbol("a")
    b = sym.Symbol("b")
    b = sym.Symbol("c")

    assert egraph.EGraph((a * b) * c) == egraph.EGraph(a * (b * c))


@pytest.mark.skip
def test_griewank_baby_example_egraph():
    x1 = sym.Symbol("x1")
    x2 = sym.Symbol("x2")

    y = (sym.sin(x1 / x2) + (x1 / x2) - sym.exp(x2)) * ((x1 / x2) - sym.exp(x2))

    egraph = egraph.EGraph(y)

    expected_nodes = (
        "-1",
        "x2",
        "x1",
        "exp(x2)",
        "1/x2",
        "-exp(x2)",
        "x1/x2",
        "x1/x2 - exp(x2))",
        "sin(x1/x2))]",
        "x1/x2 - exp(x2) + sin(x1/x2))]",
        "(x1/x2 - exp(x2))*(x1/x2 - exp(x2) + sin(x1/x2))",
    )

    assert egraph.nodes == expected_nodes

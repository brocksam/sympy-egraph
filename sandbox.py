import sympy as sm

import dag

# Not necessarily required as this is a singleton that ``dagify`` will reference
graph = dag.DirectedAcyclicGraph()

x_sm = sm.Symbol("x")
y_sm = sm.Symbol("y")

x = dag.dagify()

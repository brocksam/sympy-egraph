"""Rules to rewrite expressions within the e-graph."""


import dataclasses


@dataclasses.dataclass
class RewriteRule:
    """Definitions of rewrite rules."""

    lhs: str
    rhs: str
    assumption: str | None = None


REWRITE_RULES_BASIC = (
    RewriteRule("a*(b+c)", "(a*b) + (a*c)"),
    RewriteRule("(a*b) + (a*c)", "a*(b+c)"),
    RewriteRule("x+0", "x"),
    RewriteRule("x*1", "x"),
    RewriteRule("x*0", "0"),
)

REWRITE_RULES_C = (
    RewriteRule("x**2", "x*x"),
    RewriteRule("x**3", "x*x*x"),
)

REWRITE_RULES_FORTRAN = (
    RewriteRule("x**2", "x*x"),
    RewriteRule("x**3", "x*x*x"),
)

REWRITE_RULES_SPEED = (
    RewriteRule("sin(x)", "x", "x<<1"),
    RewriteRule("cos(x)", "1+x**2", "x<<1"),
)

REWRITE_RULES_STABILITY = (
    RewriteRule("sqrt(x+1)-sqrt(x)", "1/(sqrt(x+1)+sqrt(x))", "x>>0"),
)

"""Core components for simplified drop-in replacements for SymPy objects."""


import itertools
import weakref


class Cached(type):

    __cache = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        args = tuple(sorted(args))
        if str(args) not in self.__cache:
            obj = super().__call__(*args, **kwargs)
            self.__cache[str(args)] = obj
        return self.__cache[str(args)]


class Node(metaclass=Cached):

    def _cast_for_op(self, other, op, op_name, swap=False):
        if isinstance(other, str):
            other = Symbol(other)
        elif isinstance(other, int):
            other = Integer(other)
        else:
            msg = f"{title(op_name)} between {type(self)} and {type(other)} is not supported."
            raise ValueError
        if swap:
            return op(other, self)
        return op(self, other)

    def __add__(self, other):
        if isinstance(other, Node):
            return Add(self, other)
        return self._cast_for_op(other, Add, "addition")

    def __radd__(self, other):
        if isinstance(other, Node):
            return Add(other, self)
        return self._cast_for_op(other, Add, "addition", swap=True)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        if isinstance(other, Node):
            return Mul(self, other)
        return self._cast_for_op(other, Mul, "multiplication")

    def __rmul__(self, other):
        if isinstance(other, Node):
            return Mul(other, self)
        return self._cast_for_op(other, Mul, "multiplication", swap=True)

    def __truediv__(self, other):
        return Div(self, other)

    def __pow__(self, other):
        return Pow(self, other)

    def __lt__(self, other):
        return str(self._iden) < str(other._iden)


class Symbol(Node):
    """Simplified drop-in replacement for SymPy's `Symbol` class."""

    def __init__(self, name):
        if not isinstance(name, str):
            msg = f"Name {repr(name)} is invalid. Names should be strings, not {type(name)}."
            raise ValueError(msg)
        if len(name) == 0:
            msg = f"Name {repr(name)} is invalid. Names must be at least one character."
            raise ValueError(msg)
        elif name[0] == "@":
            msg = f"Name {repr(name)} is invalid. Names beginning with '{str('@')}' are reserved for internal use"
            raise ValueError(msg)
        self._iden = name

    @property
    def name(self):
        return self._iden

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    def __str__(self):
        return f"{self.name}"


class Integer(Node):
    """Simplified drop-in replacement for SymPy's `Integer` class."""

    def __init__(self, value):
        if not isinstance(value, int):
            msg = f"Value {repr(value)} is invalid. Values should be integers, not {type(value)}."
            raise ValueError(msg)
        self._iden = value

    @property
    def value(self):
        return self._iden

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __str__(self):
        return f"{self.value}"


class Op(Node):
    def __init__(self, *args, **kwargs):
        self._ops = args

    @property
    def operands(self):
        return self._ops

    @property
    def number_operands(self):
        return self._NUM_OPS


class UnaryOp(Op):

    _NUM_OPS = 1

    def __init__(self, op):
        super().__init__(op)
        self.op = op

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.op)})"

    def __str__(self):
        return f"{self._STR}({str(self.op)})"


class BinaryOp(Op):

    _NUM_OPS = 2

    def __init__(self, op1, op2):
        super().__init__(op1, op2)
        self.op1 = op1
        self.op2 = op2

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.op1)}, {repr(self.op2)})"

    def __str__(self):
        lhs = (
            f"{str(self.op1)}"
            if isinstance(
                self.op1, (self.__class__, Integer, Symbol, UnaryOp)
            )
            else f"({str(self.op1)})"
        )
        rhs = (
            f"{str(self.op2)}"
            if isinstance(
                self.op2, (self.__class__, Integer, Symbol, UnaryOp)
            )
            else f"({str(self.op2)})"
        )
        return f"{lhs}{self._STR}{rhs}"


class Add(BinaryOp):
    _STR = "+"

    def __str__(self):
        NO_PARENTHESIS_TYPES = (
            self.__class__,
            Symbol,
            Integer,
            UnaryOp,
            Add,
            Sub,
        )
        lhs = (
            f"{str(self.op1)}"
            if isinstance(self.op1, NO_PARENTHESIS_TYPES)
            else f"({str(self.op1)})"
        )
        rhs = (
            f"{str(self.op2)}"
            if isinstance(self.op2, NO_PARENTHESIS_TYPES)
            else f"({str(self.op2)})"
        )
        return f"{lhs}{self._STR}{rhs}"


class Sub(BinaryOp):
    _STR = "-"

    def __str__(self):
        NO_PARENTHESIS_TYPES = (
            self.__class__,
            Symbol,
            UnaryOp,
            int,
            float,
            Add,
            Sub,
        )
        lhs = (
            f"{str(self.op1)}"
            if isinstance(self.op1, NO_PARENTHESIS_TYPES)
            else f"({str(self.op1)})"
        )
        rhs = (
            f"{str(self.op2)}"
            if isinstance(self.op2, NO_PARENTHESIS_TYPES)
            else f"({str(self.op2)})"
        )
        print(lhs, rhs)
        return f"{lhs}{self._STR}{rhs}"


class Mul(BinaryOp):
    _STR = "*"


class Div(BinaryOp):
    _STR = "/"


class Pow(BinaryOp):
    _STR = "**"


class Exp(UnaryOp):
    _STR = "exp"


class Sin(UnaryOp):
    _STR = "sin"


class Cos(UnaryOp):
    _STR = "cos"


def exp(x):
    return Exp(x)


def sin(x):
    return Sin(x)


def cos(x):
    return Cos(x)

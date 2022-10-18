"""Core components for simplified drop-in replacements for SymPy objects."""


import itertools
import weakref


class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()
        self.__counter = itertools.count()

    def __call__(self, *args, **kwargs):
        if args not in self.__cache:
            obj = super().__call__(*args, **kwargs)
            obj._iden = f"@{next(self.__counter)}"
            self.__cache[args] = obj
        return self.__cache[args]


class CommutativeCached(Cached):
    def __call__(self, *args, **kwargs):
        args = sorted(args)
        return super().__call__(*args, **kwargs)


class NodeMixin:
    @property
    def name(self):
        return self._name

    def __add__(self, other):
        return Add(self, other)

    def __radd__(self, other):
        return Add(other, self)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        return Mul(other, self)

    def __truediv__(self, other):
        return Div(self, other)

    def __pow__(self, other):
        return Pow(self, other)

    def __lt__(self, other):
        return self._iden < other._iden

    def __hash__(self):
        return hash(self._iden)


class Symbol(NodeMixin, metaclass=Cached):
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
        self._name = name

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    def __str__(self):
        return f"{self.name}"


class Integer(NodeMixin, metaclass=Cached):
    """Simplified drop-in replacement for SymPy's `Integer` class."""

    def __init__(self, value):
        if not isinstance(value, int):
            msg = f"Value {repr(value)} is invalid. Values should be integers, not {type(value)}."
            raise ValueError(msg)
        self._value = value

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __str__(self):
        return f"{self.value}"


class OpMixin(NodeMixin):
    def __init__(self, *args, **kwargs):
        self._ops = args

    @property
    def operands(self):
        return self._ops

    @property
    def number_operands(self):
        return self._NUM_OPS


class UnaryOpMixin(OpMixin):

    _NUM_OPS = 1

    def __init__(self, op):
        super().__init__(op)
        self.op = op

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.op)})"

    def __str__(self):
        return f"{self._STR}({str(self.op)})"


class BinaryOpMixin(OpMixin):

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
                self.op1, (self.__class__, Symbolic, UnaryOpMixin, int, float)
            )
            else f"({str(self.op1)})"
        )
        rhs = (
            f"{str(self.op2)}"
            if isinstance(
                self.op2, (self.__class__, Symbolic, UnaryOpMixin, int, float)
            )
            else f"({str(self.op2)})"
        )
        return f"{lhs}{self._STR}{rhs}"


class Add(BinaryOpMixin, metaclass=CommutativeCached):
    _STR = "+"

    def __str__(self):
        NO_PARENTHESIS_TYPES = (
            self.__class__,
            Symbolic,
            UnaryOpMixin,
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
        return f"{lhs}{self._STR}{rhs}"


class Sub(BinaryOpMixin, metaclass=Cached):
    _STR = "-"

    def __str__(self):
        NO_PARENTHESIS_TYPES = (
            self.__class__,
            Symbolic,
            UnaryOpMixin,
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


class Mul(BinaryOpMixin, metaclass=CommutativeCached):
    _STR = "*"


class Div(BinaryOpMixin, metaclass=Cached):
    _STR = "/"


class Pow(BinaryOpMixin, metaclass=Cached):
    _STR = "**"


class Exp(UnaryOpMixin, metaclass=Cached):
    _STR = "exp"


class Sin(UnaryOpMixin, metaclass=Cached):
    _STR = "sin"


class Cos(UnaryOpMixin, metaclass=Cached):
    _STR = "cos"


def exp(x):
    return Exp(x)


def sin(x):
    return Sin(x)


def cos(x):
    return Cos(x)

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

"""Simplified drop-in replacement for SymPy's root node classes."""


from .core import Cached, NodeMixin


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

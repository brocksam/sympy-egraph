""""""

from abc import ABCMeta


class SingletonMeta(type):
    """Metaclass for making singleton instances."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Create a new instance of the class."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonABC(SingletonMeta, ABCMeta):
    """Combined metaclass of ``SingletonMeta`` and ``abc.ABC``."""
    pass

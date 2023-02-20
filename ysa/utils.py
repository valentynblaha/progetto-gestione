"""
Utilities module
"""
__all__ = ['Singleton', 'print_yellow']


class Singleton(type):
    """Singleton design pattern metaclass.
    Inherit from this class if you want your class to be a singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
            super()
        return cls._instances[cls]


__NC = '\033[0m'  # No Color

def print_yellow(*args, **kwargs):
    """Like print but in yellow
    """
    YELLOW = '\033[1;93m'
    print(YELLOW, *args, __NC, **kwargs)


def print_red(*args, **kwargs):
    """Like print but in red
    """
    RED = '\033[1;31m'
    print(RED, *args, __NC, **kwargs)

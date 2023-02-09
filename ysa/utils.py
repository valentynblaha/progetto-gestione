"""
Utilities module
"""
__all__ = ['Singleton', 'print_yellow']

class Singleton(type):
    _instances = {}    

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            super()
        return cls._instances[cls]




def print_yellow(*args, **kwargs):
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color
    print(YELLOW, *args, NC, **kwargs)

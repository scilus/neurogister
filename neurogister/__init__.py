
from .neurogister import Neurogister

__version__ = '0.2.0'


def get_root():
    import os
    return os.path.realpath(f"{os.path.dirname(os.path.abspath(__file__))}/..")


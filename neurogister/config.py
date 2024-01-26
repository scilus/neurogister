
from enum import Enum, auto


class Actions(Enum):
    DVC_PUSH = auto()


ON_PUSH = Actions.DVC_PUSH


def _authenticate(_action, _credentials):
    return True


def restricted(action, creadentials):
    def _fn(fn):
        def wrapper(*args, **kwargs):
            if _authenticate(action, creadentials):
                return fn(*args, **kwargs)
        return wrapper
    return _fn

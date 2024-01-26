
from enum import Enum, auto


class Actions(Enum):
    DVC_PUSH = auto()


ON_PUSH = Actions.DVC_PUSH

ACCESSES = {
    Actions.DVC_PUSH: False
}

REGISTRY_ROOT = "/data"
STORE_ROOT = "/store"
REPOSITORY = "https://github.com/AlexVCaron/scil_data.git"


def _authenticate(_action):
    return ACCESSES[_action]


def restricted(action):
    def _fn(fn):
        def wrapper(*args, **kwargs):
            print(args)
            if _authenticate(action):
                return fn(*args, **kwargs)
        return wrapper
    return _fn


from enum import Enum, auto
import inspect
import os
import yaml


class Actions(Enum):
    DVC_PUSH = auto()


ON_PUSH = Actions.DVC_PUSH

ACCESSES = {
    Actions.DVC_PUSH: {
        "default" : False
    }
}

REGISTRY_ROOT = "/data"
STORE_ROOT = "/store"
REPOSITORY = "https://github.com/AlexVCaron/scil_data.git"
DVC_DATA_BRANCH = "dvc-do-not-touch"


def _authenticate(_action, source="default"):
    if not ACCESSES[_action][source]:
        raise PermissionError(
            f"({source}) No permissions for {_action.name}")


def restricted(action):
    def _fn(fn):
        def wrapper(*args, **kwargs):
                _auth = False
                print(ACCESSES)
                for it in inspect.stack()[1:]:
                    if it.function == "main":
                        break

                    try:
                        source = it.frame.f_locals.get("self")
                        _authenticate(action, source or "default")
                    except PermissionError:
                        continue
                    except KeyError:
                        continue
                    else:
                        _auth = True
                        break

                if not _auth:
                    raise PermissionError(f"No permissions for {action.name}")

                return fn(*args, **kwargs)
        return wrapper
    return _fn


def authenticated(cls):
    _init = cls.__init__

    def _crinit(self, *args, **kwargs):
        _init_sig = inspect.signature(_init)
        _kwargs = {
            k: v.default
            for k, v in _init_sig.parameters.items()
            if v.default is not inspect.Parameter.empty
        }
        _kwargs.update(kwargs)

        _credfile = os.path.join(_kwargs["config"], "credentials.yml")
        if os.path.exists(_credfile):
            with open(_credfile) as f:
                _credentials = yaml.safe_load(f)
                for _act, _auth in _credentials["accesses"].items():
                    ACCESSES[Actions[_act]][self] = _auth

        return _init(self, *args, **kwargs)

    cls.__init__ = _crinit
    return cls


def get_root():
    import os
    return os.path.realpath(f"{os.path.dirname(os.path.abspath(__file__))}/..")


def get_dvc_directory():
    return f"{get_root()}/.dvc"

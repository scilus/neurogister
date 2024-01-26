
from dvc import config as dvc_conf
from dvc.api import DVCFileSystem
import os

from neurogister import PUSH_ACCESS, REPOSITORY
from neurogister.config import restricted, ON_PUSH


class DVCPush:
        def __init__(self, config):
            _conf = config
            if not _conf["remote"]:
                raise RuntimeError(
                    "Remote for dvc store is not set. Please run "
                    "dvc remote add <store-name> <type and remote>. "
                    "See https://dvc.org/doc/command-reference/")

        def _exec(self, _cmd):
            return os.system(_cmd)

        def do_push(self, path):
            self._exec(f"dvc add --no-commit {path}")
            self._exec(f"dvc commit -f {path}")
            self._exec(f"dvc push {path}")


class Registry:
    def __init__(self, config=None):
        self._config = dvc_conf.Config(config)

    def _fs(self, revision=None):
        return DVCFileSystem(
            REPOSITORY, rev=revision, remote_name="neurogister",
            remote_config=self._config["remote"]["neurogister"])

    def _assume_push_access(self):
        return PUSH_ACCESS

    def info(self):
        _fs = self._fs()
        _config = _fs.repo.config
        _repository = _fs.repo_url
        _remote = _config['core']['remote']

        print("Registry configuration :")
        print(f"  Core   :  repository {_repository}")
        print(f"            remote     {_remote}")
        print(f"            autostage  {_config['core']['autostage']}")
        print(f"  Cache  :  {_config['cache']['dir']}")
        print(f"            shared {_config['cache']['shared']}")
        print(f"            type   {_config['cache']['type']}")

        if _remote in _config['remote']:
            _rconfig = _config['remote'][_remote]
            print(f"  Remote :  {_remote}")
            print(f"            url      {_rconfig['url']}")
            if 'user' in _rconfig:
                print(f"            user     {_rconfig['user']}")
            if 'keyfile' in _rconfig:
                print(f"            keyfile  {_rconfig['keyfile']}")

    def pull(self, source, target, revision=None, recursive=False):
        self._fs(revision).get(source, target, recursive=recursive)

    @restricted(ON_PUSH)
    def push(self, source, target=None):
        if target is None:
            target = source
        else:
            os.symlink(os.path.realpath(source), target)

        DVCPush(self._config).do_push(target)

    def list(self, path, revision=None, details=False,
             recursive=True, maxdepth=None):
        if not maxdepth and recursive:
            return self._fs(revision).find(path, details=details,
                                           dvc_only=True, maxdepth=maxdepth)

        return [entry['name'] for entry in self._fs(revision).ls(
            path, details=details, dvc_only=True)]
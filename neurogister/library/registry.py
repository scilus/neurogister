
from dvc import config as dvc_conf
from dvc.api import DVCFileSystem
from git import Repo
import os
import subprocess
import sys


from neurogister.config import REPOSITORY, DVC_DATA_BRANCH, restricted, ON_PUSH


class DVCHelper:
        def __init__(self, config, fs):
            _conf = config
            if not _conf["remote"]:
                raise RuntimeError(
                    "Remote for dvc store is not set. Please run "
                    "dvc remote add <store-name> <type and remote>. "
                    "See https://dvc.org/doc/command-reference/")

            self._fs = fs

        def checkout(self, path=""):
            self._fs.repo.checkout(
                path, force=True, relink=True,
                recursive=not path or os.path.isdir(path))

        def do_push(self, path):
            self._fs.repo.add(path, no_commit=True)
            self._fs.repo.commit(force=True)
            self._fs.repo.push()


class Registry:
    def __init__(self, config=None):
        self._config = dvc_conf.Config(config)

    def _fs(self, revision=DVC_DATA_BRANCH):
        return DVCFileSystem(
            REPOSITORY, rev=revision, remote_name="neurogister",
            remote_config=self._config["remote"]["neurogister"])

    def initialize(self, path=""):
        DVCHelper(self._config, self._fs()).checkout(path)

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

        fs = self._fs()
        DVCHelper(self._config, fs).do_push(target)
        DVCHelper(self._config, fs).checkout(target)

    def list(self, path, revision=None, details=False,
             recursive=True, maxdepth=None):
        if not maxdepth and recursive:
            return self._fs(revision).find(path, details=details,
                                           dvc_only=True, maxdepth=maxdepth)

        return [entry['name'] for entry in self._fs(revision).ls(
            path, details=details, dvc_only=True)]

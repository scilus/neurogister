#!/usr/bin/env python3

import argparse
from dvc.api import DVCFileSystem
from dvc import config as dvc_conf
import os


class DVCHandler:

    def __init__(self):
        _conf = dvc_conf.Config("./.dvc")
        if not _conf["remote"]:
            raise RuntimeError("Remote for dvc store is not set. Please run "
                               "dvc remote add <store-name> <type and remote>."
                               " See https://dvc.org/doc/command-reference/")

    def _exec(self, _cmd):
        return os.system(_cmd)

    def add(self, path):
        cmd = "dvc add --no-commit " + path
        return self._exec(cmd)

    def commit_all(self):
        cmd = "dvc commit -f"
        return self._exec(cmd)

    def update_remote(self):
        cmd = "dvc push"
        return self._exec(cmd)


def _create_parser():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('package_name', help='Name of the package to create.')
    p.add_argument('files', nargs='+', help='Paths into the data registry to '
                                            'package into the store.')

    return p


def main():
    parser = _create_parser()
    args = parser.parse_args()

    if os.path.exists(args.package_name):
        raise ValueError('Package {} already exists.'.format(
            args.package_name))    

    os.makedirs(f"store/{args.package_name}")
    for file in args.files:
        os.symlink(os.path.realpath(file),
                   f"store/{args.package_name}/{os.path.basename(file)}")

    handler = DVCHandler()
    handler.add(f"store/{args.package_name}")
    handler.commit_all()
    handler.update_remote()


if __name__ == "__main__":
    main()

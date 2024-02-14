#!/usr/bin/env python3

import argparse

from neurogister import Neurogister
from neurogister.config import REGISTRY_ROOT, STORE_ROOT


def _create_parser():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('package_name', help='Name of the package to create.')
    p.add_argument('vendor_name', help='Name of the vendor into which to '
                                       'create the package.')
    p.add_argument('files', nargs='+',
                   help=f'Paths into the registry (.{REGISTRY_ROOT}) to '
                        f'package into the store (./{STORE_ROOT}).')
    p.add_argument('--create_vendor', action='store_true')

    return p


def main():
    parser = _create_parser()
    args = parser.parse_args()

    registry = Neurogister(f"./{REGISTRY_ROOT}", f"./{STORE_ROOT}")

    if not registry.vendor_exists(args.vendor_name):
        if args.create_vendor:
            registry.create_vendor(args.vendor_name, "Created by neurogister.")
        else:
            raise ValueError(f"Vendor {args.vendor_name} does not exist.")

    registry.create_package(args.vendor_name, args.package_name, args.files)

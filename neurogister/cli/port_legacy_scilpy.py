#!/usr/bin/env python3

import argparse
import json
import os

from neurogister import REGISTRY_ROOT, Neurogister
from neurogister.legacy import ScilpyFetcher


def _create_parser():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('gdrive_listing', help="Json file containing data archives "
                                          "to download (see description).")
    p.add_argument("--target_dir", default=f".{REGISTRY_ROOT}",
                   help="Directory where to upload. Will be postponed "
                        "with /legacy/scilpy (default: %(default)s)")

    return p


def main():
    parser = _create_parser()
    args = parser.parse_args()
    target = os.path.join(args.target_dir, "/legacy/scilpy")

    with open(args.gdrive_listing) as f:
        archive_list = json.load(f)

    fetcher = ScilpyFetcher(archive_list, target)
    fetcher.fetch_data()

    registry = Neurogister(args.target_dir, "./store")
    for dirpath, _, filenames in os.walk(target):
        for filename in filenames:
            _rp = os.path.relpath(dirpath, target)
            registry.push_dataset(os.path.join(_rp, filename))

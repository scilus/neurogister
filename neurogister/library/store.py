
import os

from neurogister.config import STORE_ROOT
from neurogister.library.registry import Registry


class Store:
    def __init__(self, store_directory, config=None):
        os.makedirs(store_directory, exist_ok=True)
        self.store_directory = store_directory
        self.store = Registry(config)

    def _validate_vendor(self, vendor):
        if self.vendor_exists(vendor):
            raise ValueError(f"Vendor {vendor} already exists.")

    def vendor_exists(self, vendor):
        return vendor in [v.split("/")[-1] for v in self.store.list(
            f"{STORE_ROOT}", recursive=False)]

    def package_exists(self, vendor, package_name):
        return package_name in [p.split("/")[-1] for p in self.store.list(
            f"{STORE_ROOT}/{vendor}", recursive=False)]

    def create_vendor(self, vendor, description):
        self._validate_vendor(vendor)

        os.makedirs(f"{self.store_directory}/{vendor}", exist_ok=True)
        with open(f"{self.store_directory}/{vendor}/README.md", "w") as f:
            f.write(description)

        self.store.push(f"{self.store_directory}/{vendor}")

    def create_package(self, vendor, package_name, files):
        _dest = f"{self.store_directory}/{vendor}/{package_name}"
        os.makedirs(_dest, exist_ok=True)
        for file in files:
            os.symlink(os.path.realpath(file),
                       f"{_dest}/{os.path.basename(file)}")

        self.push_package(vendor, package_name)

    def pull_package(self, vendor, package_name, revision=None):
        if not self.vendor_exists(vendor):
            raise ValueError(f"Vendor {vendor} does not exist.")

        self.store.pull(f"{STORE_ROOT}/{vendor}",
                        f"{self.store_directory}/{vendor}", revision)

        self.store.pull(f"{STORE_ROOT}/{vendor}/{package_name}",
                        f"{self.store_directory}/{vendor}/{package_name}",
                        revision)

    def push_package(self, vendor, package_name):
        if not self.vendor_exists(vendor):
            raise ValueError(f"Vendor {vendor} does not exist.")

        self.store.push(f"{self.store_directory}/{vendor}/{package_name}")

        with open(f"{self.store_directory}/{vendor}/README.md", "a") as f:
            f.write(f"\n - {package_name}")

        self.store.push(f"{self.store_directory}/{vendor}")

    def list_packages(self, vendor=None, list_content=False):
        if vendor is None:
            return [p for vendor in self.list_vendors() 
                      for p in self.store.list(vendor, recursive=False)]

        if not self.vendor_exists(vendor):
            raise ValueError(f"Vendor {vendor} does not exist.")

        return self.store.list(f"{STORE_ROOT}/{vendor}",
                               recursive=list_content)

    def list_vendors(self):
        return self.store.list(f"{STORE_ROOT}", recursive=False)


from neurogister.config import REGISTRY_ROOT, authenticated, get_dvc_directory
from neurogister.library.registry import Registry
from neurogister.library.store import Store


@authenticated
class Neurogister:
    def __init__(self, registry_directory, store_directory, 
                 config=get_dvc_directory()):
        self.registry = Registry(config)
        self.registry_directory = registry_directory
        self.store = Store(store_directory, config)
        self.registry.initialize()

    def info(self):
        print(f"Registry location : {self.registry_directory}")
        print(f"Store location    : {self.store.store_directory}")
        print()
        self.registry.info()

    def pull_datasets(self, dataset_names, revision=None):
        for dataset_name in dataset_names:
            self.registry.pull(f"{REGISTRY_ROOT}/{dataset_name}",
                               f"{self.registry_directory}/{dataset_name}",
                               revision)

    def create_vendor(self, vendor, description):
        self.store.create_vendor(vendor, description)

    def create_package(self, vendor, package_name, files):
        if self.store.package_exists(vendor, package_name):
            raise ValueError(f"Package {package_name} already exists.")

        self.store.create_package(vendor, package_name, files)

    def pull_package(self, vendor, package_name, revision=None):
        if not self.store.package_exists(vendor, package_name):
            raise ValueError(f"Package {package_name} does not exist.")

        self.store.pull_package(vendor, package_name, revision)

    def push_package(self, vendor, package_name):
        if not self.store.package_exists(vendor, package_name):
            raise ValueError(f"Package {package_name} does not exist.")

        self.store.push_package(vendor, package_name)

    def push_dataset(self, dataset_name):
        self.registry.push(f"{self.registry_directory}/{dataset_name}",
                           f"{REGISTRY_ROOT}/{dataset_name}")

    def list_packages(self, vendor=None):
        return self.store.list_packages(vendor)

    def list_datasets(self):
        return self.registry.list(f"{REGISTRY_ROOT}")

    def list_vendors(self):
        return self.store.list_vendors()

    def vendor_exists(self, vendor):
        return self.store.vendor_exists(vendor)

# Neurogister

Welcome to **Neurogister**, a DVC driven data registry for neuroimaging. It provides datasets for process validation and benchmarking, educational purposes, and more. 

# Installation

**NOT WORKING, USE THE CLONE**

Neurogister is delivered through Pypi. To install it, simply run:

```
pip install neurogister
```

**WORKING CLONE DOWN BELOW**

You can also clone the repository and install it from source. For that, you'll need [hatch](https://hatch.pypa.io/latest/) installed. Then, run the following commands :

```
git clone https://github.com/AlexVCaron/neurogister.git
hatch env create
hatch shell
```

# Usage

For now, *neurogister* doesn't offer much. It is mostly designed to serve as a test dataset creator and fetcher for [scilpy](https://github.com/scilus/scilpy) and [nf-scil](https://github.com/scilus/nf-scil).

You are free to roam it's current API. You can use the info, pull and list commands to get data from the registry. Try it and tell us about it !

## Raw access with DVC (REQUIRES GIT CLONE)

Once cloned, you can use **dvc** directly to interact with the registry. For example, to get the list of all datasets, run:

```
dvc list -R
```

To get a list of commands, run `dvc --help`.

# Storage structure

The data is stored in a DVC registry, stored online and versioned through this repository. The dataset **registry** is stored in the data/ folder and the package **store** in the store/ folder.

**Registry**

Inside the registry, you'll find several collection of datasets, in a more or less organized fashion,though each collection is stored in a separate folder. Files collected in a same folder should have a common role or exist in the same context or space.

**Store**

Comparatively to the registry, the store is a strictly organized collection of packages. Each entry is a curated vendor, registered with **neurogister**, that contains a set of validated and versioned packages **with purpose**. Every package in the store points to a collection of datasets in the registry.

# TODO

- Data structure schema
- Reorganize store in logical folders (departments)
- Create PR workflow for adding new data (in data/)
- Create PR workflow for adding new packages (in store/...)

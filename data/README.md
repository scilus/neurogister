# SCIL database

## Legacy

All content from the old SCIL database (backed by Google Drive) synced on DVC.

### Usage

Data here is currently not used, nor synced. The new deployment on DVC (in other datasets below) still uses old ways on distributing the content through archives.

### Potential

Since the database as been unpacked and saved to DVC as is, it proposes a playground for full DVC integration and distribution of content. However, nothing is straightforward in doing so, but it would be a good Data Science / Data Engineering project. API implementation, version management, artifact packing, versioning and distribution and many other aspects could be explored.

## nf_scil_archives

Actual `nf-neuro` dataset used for tests. Contains all test archives it uses. `nf-neuro/modules`loads those archives using HTTP on the public [SCIL DVC distribution endpoint](https://scil.usherbrooke.ca/scil_test_data/dvc-store/), a read-only access to the **Raw DVC storage**. Visit [`nf-neuro/modules`](https://github.com/nf-neuro/modules) for more on the interation with the distribution endpoint.

## scilpy_archives

New scilpy archives versioning and distribution. Contains all scilpy archives used for tests and examples. `scilpy` loads those archives using HTTP on the public [SCIL DVC distribution endpoint](https://scil.usherbrooke.ca/scil_test_data/dvc-store/), a read-only access to the **Raw DVC storage**. Visit [`scilpy`](https://github.com/scilus/scilpy) for more on the interation with the distribution endpoint.

## subject20slices

Reduced test dataset of a single subject from Penthera3T, cropped on 20 slices around the ventricles and inter-hemispheric passage of the corpus callosum. Full brain available in the **subjectWholeBrain** dataset `sources` (except raw data), described below. The whole directory is versionned using DVC, in-depth. The `archives` directory contains archives of all other directories (or their sub-directories) ready for distribution to `nf-neuro` and `scilus` tools.

### Diffusion datasets

Many DWI datasets can be found in the `raw` and `processed` directories. They are all sampled from the same Penthera3T acquisition, subsetting b-values and directions to create various single-shell (`DWIss`) and multi-shell (`DWIms`) test cases. Each dataset indicates its b-values and number of directions (`dir*`) in its name. Each dataset is archived individually in the `archives` directory.

## subjectWholeBrain

Contains processed data from a single Penthera3T subject. Uses the same organization as `subject20slices`.

## (Deprecated) templates

Dataset used to store template. Currently only hosts the MNI152 1mm symmetric template used in some SCIL processing pipelines. None other should be added and [Templateflow](https://templateflow.org/) should be used instead.
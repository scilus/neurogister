# Test data for nf-tractoflow pipeline automated tests

All data is contained in the **raw_database** directory aside this readme. nf-tractoflow
doesn't use those files directly, but loads them using the `samplesheets` located again
aside this readme.

## Test cases

### Light test

A very light test case composed of one subject (DWI+EPI+T1w).

DWI - 2mm iso, about 120 voxels squared in plane, 90 slices - 27 volumes total : 

- 1 b0
- 6 b300
- 10 b1000
- 10 b2000

### Light test with reverse DWI

A light test case composed of one subject (DWI+REV-DWI+T1w).

DWI - 2mm iso, about 120 voxels squared in plane, 90 slices - 27 volumes total : 

- 1 b0
- 6 b300
- 10 b1000
- 10 b2000

REV-DWI - same as DWI but with reversed phase encoding direction, same gradients directions.


#!/usr/bin/env python3


import argparse
import numpy as np
import nibabel as nib
# from spherecluster import VonMisesFisherMixture
from scilpy.gradients.bvec_bval_tools import identify_shells



def get_shells(bval, bvec, dwi):
    bvals = np.loadtxt(bval)
    bvecs = np.loadtxt(bvec)

    bvals, idxs = identify_shells(bvals)
    print(bvals)
    print(idxs)
    return {bval: (bvecs[:, idxs == i], dwi[..., idxs == i]) for i, bval in enumerate(bvals)}



def main(args):
    dwi = nib.load(args.dwi)
    out = np.empty(dwi.shape[:3] + (0,))
    grads = {}
    sizes = args.sizes
    for bval, (shell, vols) in get_shells(args.bval, args.bvec, dwi.get_fdata()).items():
        print(bval)
        print(shell.shape)
        if bval == 0:
            grads[bval] = shell
            out = np.concatenate([out, vols], axis=3)
            continue
        K = sizes.pop(0)
        idxs = np.random.choice(shell.shape[1], K, replace=False)
        grads[bval] = shell[:, idxs]
        out = np.concatenate([out, vols[..., idxs]], axis=3)
        #vmf_soft = VonMisesFisherMixture(n_clusters=K, posterior_type='soft')
        #vmf_soft.fit(shell)
        #centers = vmf_soft.cluster_centers_
        # Get closest points to centers
        #lbls = vmf_soft.labels_
        #grads[bval] = np.zeros((3, K))
        #for i in range(K):
        #    idx = np.where(lbls == i)
        #    minidx = np.argmin(np.linalg.norm(shell[idx] - centers[i], axis=1))
        #    grads[bval][:, i] = shell[idx][minidx]

    # Write out the gradients
    bvals = list(grads.keys())
    bvecs = np.concatenate([grads[bval] for bval in bvals], axis=1)
    bvals = np.concatenate(
        [np.ones((grads[bval].shape[1],)) * bval for bval in bvals])
    np.savetxt(f"{args.out}.bval", bvals, fmt="%d", newline=" ")
    np.savetxt(f"{args.out}.bvec", bvecs, fmt="%.8f")
    nib.save(nib.Nifti1Image(out, dwi.affine, dwi.header), f"{args.out}.nii.gz")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Subsample the gradients to a given number of "
                    "orientations per shell.")
    parser.add_argument("dwi", help="Path to the dwi file.")
    parser.add_argument("bval", help="Path to the bvals file.")
    parser.add_argument("bvec", help="Path to the bvecs file.")
    parser.add_argument("sizes", nargs="+", type=int,
                        help="Number of orientations per shell.")
    parser.add_argument("out", help="Path to the output bvec file.")
    args = parser.parse_args()
    main(args)

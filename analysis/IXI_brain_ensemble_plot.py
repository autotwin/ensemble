import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def save_path():
    self_path_file = Path(__file__)
    analysis_path = self_path_file.resolve().parent
    return analysis_path


# load results
analysis_path = save_path()
vol_bet_fsl = np.loadtxt(str(analysis_path) + "/volume_bet_fsl.txt")
vol_ss_fsl = np.loadtxt(str(analysis_path) + "/volume_ss_fsl.txt")
vol_synthstrip = np.loadtxt(str(analysis_path) + "/volume_synthstrip.txt")
vol_synthseg = np.loadtxt(str(analysis_path) + "/volume_synthseg.txt")
vol_ensemble = np.loadtxt(str(analysis_path) + "/volume_ensemble.txt")
mask_list_bet_fsl = np.load(str(analysis_path) + "/mask_list_bet_fsl.npy")
mask_list_ss_fsl = np.load(str(analysis_path) + "/mask_list_ss_fsl.npy")
mask_list_synthstrip = np.load(str(analysis_path) + "/mask_list_synthstrip.npy")
mask_list_synthseg = []
for zz in range(0, 10):
    mask_list_synthseg. append(np.load(str(analysis_path) + "/mask_list_synthseg_%i.npy" % (zz)))
mask_list_sum = np.load(str(analysis_path) + "/mask_list_sum.npy")
mask_list_ensemble = np.load(str(analysis_path) + "/mask_list_ensemble.npy")


# plot the individiual masks
for ix in range(0, 10):
    slice = 100
    fig, ax = plt.subplots(1, 6, figsize=(12, 2))
    ax[0].imshow(np.flip(mask_list_bet_fsl[ix][slice, :, :], axis=0))
    ax[0].set_title("fsl-1")
    ax[1].imshow(np.flip(mask_list_ss_fsl[ix][slice, :, :], axis=0))
    ax[1].set_title("fsl-2")
    ax[2].imshow(np.flip(mask_list_synthstrip[ix][slice, :, :], axis=0))
    ax[2].set_title("SynthStrip")
    ax[3].imshow(np.flip(mask_list_synthseg[ix][slice, :, :], axis=0))
    ax[3].set_title("SynthSeg")
    sum_mask = mask_list_sum[ix]
    ax[4].imshow(np.flip(sum_mask[slice, :, :], axis=0), cmap=plt.cm.plasma)
    ax[4].set_title("weighted sum")
    ax[5].imshow(np.flip(mask_list_ensemble[ix][slice, :, :], axis=0), cmap=plt.cm.binary)
    ax[5].set_title("ensemble")

    for kk in range(0, 6):
        ax[kk].set_axis_off()

    plt.savefig(str(analysis_path) + "/visualize_example_%i" % (ix))

# plot volume histograms
for with_ensemble in [True, False]:
    plt.figure()
    hist, bins = np.histogram(vol_bet_fsl, bins=10)
    width = 0.95 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width, label="fsl-1", color=(0.75, 0.75, 0.75))
    hist, bins = np.histogram(vol_ss_fsl, bins=10)
    width = 0.85 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width, label="fsl-2", color=(0.25, 0, 0))
    hist, bins = np.histogram(vol_synthstrip, bins=10)
    width = 0.75 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width, label="SynthStrip", color=(0.25, 0.25, 0.5))
    hist, bins = np.histogram(vol_synthseg, bins=10)
    width = 0.65 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width, label="SynthSeg", color=(0.5, 0.5, 1))
    if with_ensemble:
        hist, bins = np.histogram(vol_ensemble, bins=10)
        width = 0.55 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center, hist, align='center', width=width, label="ensemble", color=(1.0, 0.0, 0.0))
    plt.legend()
    plt.xlabel("brain volume, mm3")
    plt.ylabel("number of examples")
    plt.title("brain volume comparison, 122 examples from IXI dataset")
    if with_ensemble:
        plt.savefig(str(analysis_path) + "/histogram_brain_volume_ensemble")
    else:
        plt.savefig(str(analysis_path) + "/histogram_brain_volume")


# plot one example suitable for visualizing the whole thing
ix = 2
for slice in range(0, mask_list_sum[ix].shape[0]):
    fig, ax = plt.subplots(1, 2, figsize=(6, 3))
    ax[0].imshow(np.flip(mask_list_sum[ix][slice, :, :], axis=0), cmap=plt.cm.plasma)
    ax[0].set_title("weighted sum")
    ax[0].set_axis_off()
    ax[1].imshow(np.flip(mask_list_ensemble[ix][slice, :, :], axis=0), cmap=plt.cm.binary)
    ax[1].set_title("ensemble")
    ax[1].set_axis_off()
    plt.savefig(str(analysis_path) + "/anim_%i_%03d" % (ix, slice))
    plt.close()
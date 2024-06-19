import nibabel as nib
import numpy as np
from pathlib import Path
from scipy import ndimage


def NIfTI_to_numpy(input_file: Path) -> np.ndarray:
    input_file_name = str(input_file)
    file = nib.load(input_file_name)
    pixdim = file.header["pixdim"]
    file_data = file.get_fdata()
    return file_data, pixdim


def interpolate_to_equal(file_data: np.ndarray, pixdim: np.ndarray):
    dim_0 = pixdim[1]
    dim_1 = pixdim[2]
    dim_2 = pixdim[3]
    new_file_data = ndimage.zoom(file_data, (dim_0, dim_1, dim_2), order=0)
    return new_file_data


def input_to_brain_mask_FAST(seg_arr: np.ndarray) -> np.ndarray:
    mask = (seg_arr == 2).astype("uint8") + (seg_arr == 3).astype("uint8")
    return mask


def input_to_brain_mask_SynthStrip(seg_arr: np.ndarray) -> np.ndarray:
    mask = seg_arr.astype("uint8")
    return mask


def input_to_brain_mask_SynthSeg(seg_arr: np.ndarray):
    ix_include = [2, 3, 7, 8, 10, 11, 12, 13, 16, 17, 18, 26, 28, 41, 42, 46, 47, 49, 50, 51, 52, 53, 54, 58, 60]
    mask = np.zeros(seg_arr.shape)
    for ix in ix_include:
        mask += (seg_arr == ix).astype("uint8")
    return mask


def interpolate_all_masks(mask_list: list, pixdim_list: list) -> list:
    interp_mask_list = []
    num_masks = len(mask_list)
    for kk in range(0, num_masks):
        new_file_data = interpolate_to_equal(mask_list[kk], pixdim_list[kk])
        interp_mask_list.append(new_file_data)
    return interp_mask_list


def add_masks(mask_list: list, weight_list: list) -> np.ndarray:
    # make sure all sizes match
    num_masks = len(mask_list)
    size_arr = np.zeros((num_masks, 3))
    for kk in range(0, num_masks):
        sh = mask_list[kk].shape
        size_arr[kk, 0] = sh[0]
        size_arr[kk, 1] = sh[1]
        size_arr[kk, 2] = sh[2]
    dim_0 = int(np.min(size_arr[:, 0]))
    dim_1 = int(np.min(size_arr[:, 1]))
    dim_2 = int(np.min(size_arr[:, 2]))
    trim_mask_list = []
    for kk in range(0, num_masks):
        mask = mask_list[kk]
        trim_mask = mask[0:dim_0, 0:dim_1, 0:dim_2]
        trim_mask_list.append(trim_mask)
    # add the masks
    mask_sum = np.zeros((dim_0, dim_1, dim_2))
    for kk in range(0, num_masks):
        mask_sum += trim_mask_list[kk] * weight_list[kk]
    return mask_sum


def ensemble_masks(mask_list, weight_list):
    mask_sum = add_masks(mask_list, weight_list)
    total_weight = np.sum(weight_list)
    thresh = total_weight / 2.0
    ensemble_mask = (mask_sum > thresh).astype("uint8")
    return ensemble_mask


def get_volume(mask: np.ndarray):
    vol = np.sum(mask)
    return vol

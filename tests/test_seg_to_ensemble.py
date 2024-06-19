from ensemble import seg_to_ensemble as ste
import numpy as np
from pathlib import Path


def path_to_test_files(fname: str):
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    files_path = self_path.joinpath("files").resolve()
    pa = files_path.joinpath(fname).resolve()
    return pa


def test_NIfTI_to_numpy():
    fname = "test_mri.nii"
    pa = path_to_test_files(fname)
    file_data, pixdim = ste.NIfTI_to_numpy(pa)
    dim_0 = pixdim[1]
    dim_1 = pixdim[2]
    dim_2 = pixdim[3]
    assert np.isclose(dim_0, 5)
    assert np.isclose(dim_1, 5)
    assert np.isclose(dim_2, 5)
    assert file_data.shape == (39, 50, 50)


def test_interpolate_to_equal():
    fname = "test_mri.nii"
    pa = path_to_test_files(fname)
    file_data, pixdim = ste.NIfTI_to_numpy(pa)
    new_file_data = ste.interpolate_to_equal(file_data, pixdim)
    dim_0 = pixdim[1]
    dim_1 = pixdim[2]
    dim_2 = pixdim[3]
    assert new_file_data.shape[0] == file_data.shape[0] * dim_0
    assert new_file_data.shape[1] == file_data.shape[1] * dim_1
    assert new_file_data.shape[2] == file_data.shape[2] * dim_2


def test_input_to_brain_mask_FAST():
    fname = "test_ss_fast.nii"
    pa = path_to_test_files(fname)
    file_data, _ = ste.NIfTI_to_numpy(pa)
    mask = ste.input_to_brain_mask_FAST(file_data)
    assert np.max(mask) == 1
    assert np.min(mask) == 0


def test_input_to_brain_mask_SynthStrip():
    fname = "test_synthstrip.nii"
    pa = path_to_test_files(fname)
    file_data, _ = ste.NIfTI_to_numpy(pa)
    mask = ste.input_to_brain_mask_SynthStrip(file_data)
    assert np.max(mask) == 1
    assert np.min(mask) == 0


def test_input_to_brain_mask_SynthSeg():
    fname = "test_synthseg.nii"
    pa = path_to_test_files(fname)
    file_data, _ = ste.NIfTI_to_numpy(pa)
    mask = ste.input_to_brain_mask_SynthSeg(file_data)
    assert np.max(mask) == 1
    assert np.min(mask) == 0


def create_mask_list():
    fname_list = ["test_ss_fast.nii", "test_bet_fast.nii", "test_synthstrip.nii", "test_synthseg.nii"]
    pixdim_list = []
    mask_list = []
    file_data_list = []
    for kk in range(0, len(fname_list)):
        pa = path_to_test_files(fname_list[kk])
        file_data, pixdim = ste.NIfTI_to_numpy(pa)
        pixdim_list.append(pixdim)
        if kk == 0 or kk == 1:
            mask = ste.input_to_brain_mask_FAST(file_data)
        elif kk == 2:
            mask = ste.input_to_brain_mask_SynthStrip(file_data)
        else:
            mask = ste.input_to_brain_mask_SynthSeg(file_data)
        mask_list.append(mask)
        file_data_list.append(file_data)
    weight_list = [0.5, 0.5, 1.0, 1.0]
    return fname_list, mask_list, file_data_list, pixdim_list, weight_list


def test_interpolate_all_masks():
    fname_list, mask_list, file_data_list, pixdim_list, _ = create_mask_list()
    interp_mask_list = ste.interpolate_all_masks(mask_list, pixdim_list)
    for kk in range(0, len(fname_list)):
        assert interp_mask_list[kk].shape[0] == pixdim_list[kk][1] * file_data_list[kk].shape[0]
        assert interp_mask_list[kk].shape[1] == pixdim_list[kk][2] * file_data_list[kk].shape[1]
        assert interp_mask_list[kk].shape[2] == pixdim_list[kk][3] * file_data_list[kk].shape[2]


def create_example_masks():
    dim_0 = 10
    dim_1 = 12
    dim_2 = 15
    mask_list = []
    weight_list = []
    mask_sum = np.zeros((dim_0, dim_1, dim_2))
    num_masks = 5
    for kk in range(0, num_masks):
        arr = np.random.random((dim_0, dim_1, dim_2))
        ma = (arr > 0.6).astype("uint8")
        mask_sum += ma
        mask_list.append(ma)
        weight_list.append(1.0)
    ensemble_mask = (mask_sum > np.sum(weight_list) / 2.0).astype("uint8")
    return mask_list, weight_list, mask_sum, ensemble_mask


def test_add_masks():
    # MRI data
    _, mask_list, _, pixdim_list, weight_list = create_mask_list()
    interp_mask_list = ste.interpolate_all_masks(mask_list, pixdim_list)
    mask_sum = ste.add_masks(interp_mask_list, weight_list)
    assert np.isclose(np.max(mask_sum), np.sum(weight_list))
    assert np.isclose(np.min(mask_sum), 0.0)
    mask_list[0] = mask_list[0][:-1, :, :]
    mask_sum = ste.add_masks(interp_mask_list, weight_list)
    assert np.isclose(np.max(mask_sum), np.sum(weight_list))
    assert np.isclose(np.min(mask_sum), 0.0)
    # known test case
    mask_list, weight_list, mask_sum_known, _ = create_example_masks()
    mask_sum = ste.add_masks(mask_list, weight_list)
    assert np.allclose(mask_sum, mask_sum_known)


def test_ensemble_masks():
    # MRI data
    _, mask_list, _, pixdim_list, weight_list = create_mask_list()
    interp_mask_list = ste.interpolate_all_masks(mask_list, pixdim_list)
    ensemble_mask = ste.ensemble_masks(interp_mask_list, weight_list)
    assert np.isclose(np.max(ensemble_mask), 1.0)
    assert np.isclose(np.min(ensemble_mask), 0.0)
    # known test case
    mask_list, weight_list, _, ensemble_mask_known = create_example_masks()
    ensemble_mask = ste.ensemble_masks(mask_list, weight_list)
    assert np.allclose(ensemble_mask, ensemble_mask_known)


def test_get_volume():
    mask = np.zeros((10, 10, 10))
    mask[1, 1, 1] = 1
    mask[1, 2, 3] = 1
    vol = ste.get_volume(mask)
    assert np.isclose(vol, 2)

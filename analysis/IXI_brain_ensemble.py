from ensemble import seg_to_ensemble as ste
import glob
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def path_to_data():
    self_path_file = Path(__file__)
    ensemble_path = self_path_file.resolve().parent.parent
    autotwin_path = ensemble_path.resolve().parent
    scc_path = autotwin_path.joinpath("copied_to_scc").resolve()
    pa = scc_path.joinpath("chad_prototype").resolve()
    return pa


def save_path():
    self_path_file = Path(__file__)
    analysis_path = self_path_file.resolve().parent
    return analysis_path


pa = path_to_data()

# file names for all types of segmented MRIs
fname_list_bet_fsl = np.sort(glob.glob(str(pa) + "/*_05_brain_seg.nii.gz"))
mask_list_bet_fsl = []
pixdim_list_bet_fsl = []
fname_list_ss_fsl = np.sort(glob.glob(str(pa) + "/*_synthstripped_seg.nii.gz"))
mask_list_ss_fsl = []
pixdim_list_ss_fsl = []
fname_list_synthstrip = np.sort(glob.glob(str(pa) + "/*_mask_no_csf.nii"))
mask_list_synthstrip = []
pixdim_list_synthstrip = []
fname_list_synthseg = np.sort(glob.glob(str(pa) + "/*-T1_mri_synthseg.nii"))
mask_list_synthseg = []
pixdim_list_synthseg = []

for fname in fname_list_bet_fsl:
    file_data, pixdim = ste.NIfTI_to_numpy(str(fname))
    mask = ste.input_to_brain_mask_FAST(file_data)
    mask_list_bet_fsl.append(mask)
    pixdim_list_bet_fsl.append(pixdim)

for fname in fname_list_ss_fsl:
    file_data, pixdim = ste.NIfTI_to_numpy(str(fname))
    mask = ste.input_to_brain_mask_FAST(file_data)
    mask_list_ss_fsl.append(mask)
    pixdim_list_ss_fsl.append(pixdim)

for fname in fname_list_synthstrip:
    file_data, pixdim = ste.NIfTI_to_numpy(str(fname))
    mask = ste.input_to_brain_mask_SynthStrip(file_data)
    mask_list_synthstrip.append(mask)
    pixdim_list_synthstrip.append(pixdim)

for fname in fname_list_synthseg:
    file_data, pixdim = ste.NIfTI_to_numpy(str(fname))
    mask = ste.input_to_brain_mask_SynthSeg(file_data)
    mask_list_synthseg.append(mask)
    pixdim_list_synthseg.append(pixdim)

num_masks = len(fname_list_bet_fsl)
ix_mask = 0

volume_list_bet_fsl = []
save_mask_list_bet_fsl = []
volume_list_ss_fsl = []
save_mask_list_ss_fsl = []
volume_list_synthstrip = []
save_mask_list_synthstrip = []
volume_list_synthseg = []
save_mask_list_synthseg = []
save_mask_list_sum = []
save_mask_list_ensemble = []
volume_list_ensemble = []

for kk in range(0, num_masks):
    mask_list = [mask_list_bet_fsl[kk], mask_list_ss_fsl[kk], mask_list_synthstrip[kk], mask_list_synthseg[kk]]
    pixdim_list = [pixdim_list_bet_fsl[kk], pixdim_list_ss_fsl[kk], pixdim_list_synthstrip[kk], pixdim_list_synthseg[kk]]
    weight_list = [0.5, 0.5, 1.0, 1.0]
    interp_mask_list = ste.interpolate_all_masks(mask_list, pixdim_list)
    mask_sum = ste.add_masks(interp_mask_list, weight_list)
    ensemble_mask = ste.ensemble_masks(interp_mask_list, weight_list)
    # volume list
    volume_list_bet_fsl.append(ste.get_volume(interp_mask_list[0]))
    volume_list_ss_fsl.append(ste.get_volume(interp_mask_list[1]))
    volume_list_synthstrip.append(ste.get_volume(interp_mask_list[2]))
    volume_list_synthseg.append(ste.get_volume(interp_mask_list[3]))
    volume_list_ensemble.append(ste.get_volume(ensemble_mask))
    # mask list (save only first 10)
    if ix_mask < 10:
        save_mask_list_bet_fsl.append(interp_mask_list[0])
        save_mask_list_ss_fsl.append(interp_mask_list[1])
        save_mask_list_synthstrip.append(interp_mask_list[2])
        save_mask_list_synthseg.append(interp_mask_list[3])
        save_mask_list_sum.append(mask_sum)
        save_mask_list_ensemble.append(ensemble_mask)
    ix_mask += 1

# save results
analysis_path = save_path()
np.savetxt(str(analysis_path) + "/volume_bet_fsl.txt", np.asarray(volume_list_bet_fsl))
np.savetxt(str(analysis_path) + "/volume_ss_fsl.txt", np.asarray(volume_list_ss_fsl))
np.savetxt(str(analysis_path) + "/volume_synthstrip.txt", np.asarray(volume_list_synthstrip))
np.savetxt(str(analysis_path) + "/volume_synthseg.txt", np.asarray(volume_list_synthseg))
np.savetxt(str(analysis_path) + "/volume_ensemble.txt", np.asarray(volume_list_ensemble))
np.save(str(analysis_path) + "/mask_list_bet_fsl.npy", save_mask_list_bet_fsl)
np.save(str(analysis_path) + "/mask_list_ss_fsl.npy", save_mask_list_ss_fsl)
np.save(str(analysis_path) + "/mask_list_synthstrip.npy", save_mask_list_synthstrip)
for zz in range(0, 10):
    np.save(str(analysis_path) + "/mask_list_synthseg_%i.npy" % (zz), save_mask_list_synthseg[zz])
np.save(str(analysis_path) + "/mask_list_sum.npy", save_mask_list_sum)
np.save(str(analysis_path) + "/mask_list_ensemble.npy", save_mask_list_ensemble)



aa = 44
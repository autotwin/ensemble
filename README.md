# ensemble

[![python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)

## Getting Started

## Configuration

### Git 

Install [Git](https://git-scm.com/) version 2.2 or later:

```bash
# example
 (main) chovey@mac/Users/chovey/autotwin/ensemble> git --version
git version 2.39.3 (Apple Git-146)
```

For Windows, we recommend [Git Bash](https://git-scm.com/download/win).  For macOS and Linux, use the Bash shell or similar.  The [Fish](https://fishshell.com/) shell is also nice.

Configure Git:

```bash
git config --global user.name "your full name here"
git config --global user.email "your email here"

# example
git config --global user.name "Jeannette Rankin"
git config --global user.email "jrankin@umontana.edu"
```

To write to the repository, [set up ssh keys](https://cee-gitlab.sandia.gov/help/user/ssh.md) between your local computer and the repository. 

### Ensemble Repo

```bash
cd ~
mkdir autotwin # create a directory called `autotwin`
cd autotwin

# clone the ensemble repo
git clone git@github.com:autotwin/ensemble.git
```

### Python

Install [Python version 3.10](https://www.python.org/downloads/).  All references to `python` will be this version.

### Virtual Environment

We use a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) to support encapsulation and reproducibility.

With in the `autotwin/ensemble` directory, create a virtual environment:

```bash
python3.10 -m venv .venv # with python and the venv module, create a virtual environment called .venv

# activate the virtual environment with one of the following:
source .venv/bin/activate       # for bash shell
source .venv/bin/activate.csh   # for c shell
source .venv/bin/activate.fish  # for fish shell
.\.venv\Scripts/activate        # for powershell
```

Note: If `.venv` already exists from previous installs, then remove it:

```bash
(.venv) $ deactivate            # deactivate if the virtual environment is currently active
$ pip uninstall .venv           # uninstall
$ rm -rf ~/autotwin/ensemble/.venv  # remove the virtual environment folder with `rm -rf .venv/`.
```

Update `pip` and `setuptools`:

```bash
pip install --upgrade pip setuptools
```

### Ensemble Module

We currently support the module in a developer configuration.  Production and client configurations will be forthcoming.

* Reference: https://packaging.python.org/en/latest/tutorials/packaging-projects/

```bash
ensemble/
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   └── ensemble/
│       ├── __init__.py
│       └── example.py
└── tests/
```

Install the module as a developer:

```bash
pip install -e .  # install in dev mode, with the editable flag
```

### Freesurfer


Install [Freesurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall).  We use Freesurfer version 7.4.1, released June 2023.

* [Downloads](https://surfer.nmr.mgh.harvard.edu/fswiki/rel7downloads) for installation.  For example, the [macOS installation](https://surfer.nmr.mgh.harvard.edu/fswiki//FS7_mac) with the GUI Package install option, `freesurfer-macOS-darwin_x86_64-7.4.1.pkg` 6.6 GB, MD5: `e050d9a939cb1c969ff0f0d12c5d2749`.
* [Introduction to Freesurfer Output](https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/OutputData_freeview)

#### recon-all

* Get `aseg.mgz`(has the segmentation data we care about), is the last step in recon-all (command that runs 31 sequential analyses).
* https://surfer.nmr.mgh.harvard.edu/fswiki/SubcorticalSegmentation
  * *"In automatic subcortical segmentation, each voxel in the normalized brain volume is assigned one of about 40 labels, including: Cerebral White Matter, Cerebral Cortex, Lateral Ventricle, Inferior Lateral Ventricle, Cerebellum White Matter, Cerebellum Cortex, Thalamus, Caudate, Putamen, Pallidum, Hippocampus, Amygdala, Lesion, Accumbens area, Vessel, Third Ventricle, Fourth Ventricle, Brain Stem, Cerebrospinal Fluid."*
* https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all
* to date, SynthSeg is used in favor of recon-all.

#### SynthStrip

Use the [SynthStrip](https://surfer.nmr.mgh.harvard.edu/docs/synthstrip/) functionality within Freesurfer.

* Use SynthStrip, the command to remove the skull from the input scan.
* on the synthstrip website, e.g., `mri_synthstrip --i input.nii.gz --o stripped.nii.gz --no-csf`
* Processed 122 examples from the IXI dataset.

#### SynthSeg

Use the [SynthSeg](https://surfer.nmr.mgh.harvard.edu/fswiki/SynthSeg) functionality within Freesurfer.

* Use SynthSeg, the command to recapitulate recon-all directly from the input scan with a neural network.
* on the synthseg website, e.g., `mri_synthseg --i input.nii.gz --o segmented.nii.gz`
* note that we cound indicies `[2, 3, 7, 8, 10, 11, 12, 13, 16, 17, 18, 26, 28, 41, 42, 46, 47, 49, 50, 51, 52, 53, 54, 58, 60]` as brain
* Processed 122 examples from the IXI dataset.


### FSL

Install [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation).

Use the Brain Extraction Tool ([Bet](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/BET/UserGuide)).

```bash
# RMU workflow
FSL: /usr/local/fsl/bin/bet  [input file] [output file] -f 0.3 -m -B -A
```

Use the FMRIB's Automated Segmentation Tool ([FAST](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FAST)).

* Run FAST after performing skull stripping with either SynthStrip or FSL BET, e.g., `fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o input_name output_name`
* Processed 122 examples from the IXI dataset.


### Segment Anything Model (SAM) and MedSAM

Reference: https://segment-anything.com/

* [Assessment 2024-04-16](https://docs.google.com/document/d/1A5qQjNUQzTSburgUGZ3_Sk3jI4C2BvM3zpVnVZeXiZA/edit)


## BU SCC - running segmentation software

Modules:
```bash
module load freesurfer/7.4.1
module load fsl/6.0.7.8
```

Input file: `input_MRI.nii`

Output files:
* SynthStrip without CSF:
```bash
mri_synthstrip -i input_MRI.nii -m input_MRI_synthsrip_mask.nii --no-csf
```
relevant output file: `input_MRI_synthsrip_mask.nii`
* SynthStrip + FAST:
```bash
mri_synthstrip -i input_MRI.nii -o input_MRI_synthstrip_brain.nii

fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o input_MRI_synthstrip_brain input_MRI_synthstrip_brain
```
relevant output file: `input_MRI_synthsrip_brain_seg.nii.gz`
* BET + FAST:
```bash
bet input_MRI input_MRI_bet_brain -f 0.5 -g 0

fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o input_MRI_bet_brain input_MRI_bet_brain
```
relevant output file: `input_MRI_bet_brain_seg.nii.gz`
* SynthSeg:
```bash
mri_synthseg --i input_MRI.nii --o input_MRI_mri_synthseg.nii
```
relevant output file: `input_MRI_mri_synthseg.nii`

122 examples from the IXI dataset have been run with this workflow.

## Workflow

Run the test suite to assure the virtual environment and module work:

```bash
(.venv)  (main) chovey@mac/Users/chovey/autotwin/ensemble> pytest -v
================================================== test session starts ==================================================
platform darwin -- Python 3.10.11, pytest-8.1.1, pluggy-1.4.0 -- /Users/chovey/autotwin/ensemble/.venv/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/chovey/autotwin/ensemble
configfile: pyproject.toml
plugins: cov-5.0.0
collected 2 items                                                                                                       

tests/test_hello.py::test_hello PASSED                                  [ 50%]
tests/test_hello.py::test_adios PASSED                                  [100%]
```

Review the command line interface (CLI):

```bash
-----------------
autotwin.ensemble
-----------------

ensemble
    (this command)

process <pathfile>.yml
    Process the .yml input file.
    Example:
        process tests/files/getting_started.yml # TODO

pytest
    Runs the test suite (non-verbose option).

pytest -v
    Runs the test suite (verbose option).

validate <pathfile>.yml # TODO
    Validate the .yml input file against the module's schema.

version
    Prints the semantic version of the current installation.
```

## Preliminary Results - IXI dataset



## References

### 2024-03-25-0903

```bash
Hi Emma,

Just a follow-up from the last meeting.  It turns out that our current workflow uses FSL to obtain the skull mask, which is the skull segmentation that we use in our head model.  The quality of the skull segmentation from this tool is not consistent, so it often requires some manual corrections afterwards using 3D Slicer.

Here's an example command that we use in FSL: /usr/local/fsl/bin/bet  [input file] [output file] -f 0.3 -m -B -A

The input file is the MRI file and the output is the skull mask. The thresholding parameter (0.3 above) varies from 0 to 1, and this value is often selected via trial and error (usually between 0.3 and 0.8) to obtain the best segmentation.  Before obtaining the skull mask, we also perform a bias field correction (using ANTS software) and Gibbs correction (using Mrtrix software) on the original MRI file.  More details about this can be found here.

Hope this helps to clarify our current process.  It would be great to explore other tools that may produce an improved result for the skull segmentation.

Best,
Rika
```

### Slicer

* The RMU manual workflow user [Slicer](https://www.slicer.org).
* [RMU workflow](https://docs.google.com/document/d/1_AkVtCFgTakGihnByPyMeO1eAVWoLZ3XTU2a3a_VO9s/edit?usp=sharing)

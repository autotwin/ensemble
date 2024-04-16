# ensemble

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
python -m venv .venv # with python and the venv module, create a virtual environment called .venv

# activate the virtual environment with one of the following:
source .venv/bin/activate       # for bash shell
source .venv/bin/activate.csh   # for c shell
source .venv/bin/activate.fish  # for fish shell
.\.venv\Scripts/activate        # for powershell
```

Note: If `.venv` already exists from previous installs, then remove it as follows:

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

Install [Freesurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall).

Use the [SynthStrip](https://surfer.nmr.mgh.harvard.edu/docs/synthstrip/) functionality within Freesurfer.

### FSL

Install [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation).

Use the Brain Extraction Tool ([Bet](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/BET/UserGuide)).

```bash
# RMU workflow
FSL: /usr/local/fsl/bin/bet  [input file] [output file] -f 0.3 -m -B -A
```

### Segment Anything Model (SAM)

https://segment-anything.com/

### MedSAM

To come.

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

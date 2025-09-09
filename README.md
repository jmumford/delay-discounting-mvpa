# Delay Discounting Classifier Analysis Code

Code for running classifier analyses on delay discounting fMRI data.

## Setup

1. Install [uv](https://github.com/astral-sh/uv).
2. If you are on **Sherlock**:
   - Request an interactive compute session (do not run on the login node).
   - Load GCC:
     ```bash
     module load gcc/12.4.0
     ```
3. Clone this repository and `cd` into the root directory (where `pyproject.toml` is located).
4. Run:
   ```bash
   uv sync
   ```

## Directory structure

```
.
├── analysis_code
│   ├── notebooks          # Notebooks used to test and develop code
│   └── scripts            # Main scripts, batch scripts, and supporting files
├── configs                # Configuration YAML files
├── pyproject.toml
├── README.md
└── src
    └── delay_discounting_mvpa  # Core Python package code
```

## Main scripts

- `analysis_code/notebooks`: contains Jupyter notebooks used to test and develop the code.
- `analysis_code/scripts`: contains the main scripts for running analyses, including:
  - Batch scripts for SLURM
  - Python scripts called by the batch scripts
  - Supporting `.txt` files referenced by the scripts

## Usage

1. Edit the configuration file in `configs/config.yaml` as needed (this shouldn't be needed!).
2. Launch analyses via the batch scripts in `analysis_code/scripts`. For example:
   ```bash
   sbatch run_lsa_all.batch
   ```
3. Output (beta series, logs, etc.) will be saved according to the paths specified in your batch scripts and configuration.

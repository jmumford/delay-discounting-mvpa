# Delay Discounting Classifier Analysis Code

Code for running classifier analyses on delay discounting fMRI data.
Location: `/oak/stanford/groups/russpold/data/uh2/aim1/analysis_code/delay_discounting_mvpa`
---

## Setup

1. **Load the environment** by sourcing the setup script:  
   ```bash
   source setup_uv.sh
   ```
   This sets up modules, Python, and project environment variables.  

> If you are on Sherlock, the virtual environment is already prepared (`.vnenv`), so no further setup is needed.  
> Only need to run prior to using `uv add` or `uv sync`

---

## Directory structure (top-level)

```
.
├── analyses                # Analysis-specific code directories
├── analysis_registry       # Summaries of analyses for each directory in analyses
├── configs                 # Configuration YAML files for analyses (paths, rt, etc.)
├── src                     # Core Python package code
├── setup_uv.sh             # Script to set up environment modules and variables
├── slurm_logs              # Output logs from SLURM jobs
├── pyproject.toml
├── README.md
├── .env                    # Environment variable settings for uv
├── .gitignore
├── LICENSE
├── uv_cache
├── uv.lock
├── .venv
└── .python-version
```
> Only the first four directories are relevant for running or understanding analyses. The rest are for project/environment setup and version control.

---

## Analyses

- **`analyses/`**: Each subdirectory contains:
  - `notebooks/`: Jupyter notebooks for testing and developing code.  
  - `scripts/`: Python and batch scripts for executing analyses.  

- **`analysis_registry/`**: yaml files and a Markdown summaries of all analyses, including:
  - Individual `.yaml` files for each analysis (in /analysis_registry/analyses)
  - Combined `master_registry.yaml`
  - Github friendly README (same info as `master_registry.yaml`)
      - Quick summary table for all analyses  
      - Detailed reports for each analysis  

- **`configs/`**: YAML configuration files used by analyses. Contains paths, rt and other settings that are used in various analyses.

---

## Usage

1. Source the environment:  
   ```bash
   source setup_uv.sh
   ```
2. Run analyses in notebooks or using batch scripts, which should be contained in corresponding analysis directory.
  - batch scripts should include this to load the prep `uv` and then the following will run your script using the uv `.venv`.

      ```
      PROJECT_ROOT="/oak/stanford/groups/russpold/data/uh2/aim1/analysis_code/delay_discounting_mvpa"
      UV_SETUP="$PROJECT_ROOT/setup_uv.sh"
      source $UV_SETUP

      uv --directory "$PROJECT_ROOT" run python myscript.py
      ```
3. Outputs (beta series, logs, etc.) are saved according to paths specified in the scripts and configuration files.

---

### Notes for New Researchers

- Check `analysis_registry/README.md` (or `master_registry.yaml`) to understand which analyses have been run, status, and notes.  
- `analyses/*` directories contain notebooks (code development, figures, QA) and python scripts (analysis code typically paried with a batch script).  Take care in editing any scripts in directories created by others, as this could break analysis provenance.  
- `setup_uv.sh` must be run before executing scripts to ensure proper environment variables and module versions are loaded.

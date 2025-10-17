#!/bin/bash
# setup_uv.sh - load modules and project environment

# Set default permissions (files are group-readable)
umask 0006

# Load required modules
module load fsl
module load python/3.12.1
module load gcc/12.4.0
module load uv

# Export UV environment variables from .env
PROJECT_ROOT="/oak/stanford/groups/russpold/data/uh2/aim1/analysis_code/delay_discounting_mvpa"
export $(cat "$PROJECT_ROOT/.env" | xargs)

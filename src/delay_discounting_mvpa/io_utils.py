import os
import re
from glob import glob
from pathlib import Path
from typing import List

import pandas as pd

from delay_discounting_mvpa.config_loader import Config


def resolve_file(cfg: Config, subject_id: str, kind: str) -> Path:
    """
    Fetch a single file for a subject based on kind ('bold', 'mask', or 'behav').
    Ensures exactly one file is matched and returns it as a Path.

    Parameters
    ----------
    cfg : Config
        Configuration object with .paths attributes.
    subject_id : str
        BIDS-style subject ID (no "sub-" prefix).
    kind : str
        One of 'bold', 'mask', or 'behav'.

    Returns
    -------
    Path
        The matched file path.

    Raises
    ------
    ValueError
        If kind is invalid or if zero/multiple files are found.
    """
    if kind == 'bold':
        pattern = f'{cfg.fmriprep_dir}/sub-{subject_id}/{cfg.bold_file_glob}'
    elif kind == 'mask':
        pattern = f'{cfg.fmriprep_dir}/sub-{subject_id}/{cfg.bold_mask_file_glob}'
    elif kind == 'behav':
        pattern = f'{cfg.bids_dir}/sub-{subject_id}/{cfg.behav_file_glob}'
    else:
        raise ValueError(
            f"Unknown file kind: {kind!r}. Must be 'bold', 'mask', or 'behav'."
        )

    matches = glob(pattern)

    if not matches:
        raise ValueError(f'No files found for {kind!r} with pattern: {pattern}')
    if len(matches) > 1:
        raise ValueError(
            f'Multiple files found for {kind!r} with pattern: {pattern}\n{matches}'
        )

    return Path(matches[0])


def load_tsv_data(tsv_file: Path) -> pd.DataFrame:
    """
    Load behavioral data from a TSV file into a pandas DataFrame.

    Parameters
    ----------
    tsv_file : Path
        Path to the TSV file.

    Returns
    -------
    pd.DataFrame
        Data from the TSV file.

    Raises
    ------
    ValueError
        If the file does not have a .tsv extension.
    """
    if tsv_file.suffix != '.tsv':
        raise ValueError(f'Expected a .tsv file, got: {tsv_file}')

    return pd.read_csv(tsv_file, sep='\t')


def get_subids(cfg: Config) -> List[str]:
    """
    Extract unique subject IDs from cfg.fmriprep_dir.

    Looks for directories starting with 'sub-s###'.

    Parameters
    ----------
    cfg : Config
        Configuration object

    Returns
    -------
    list[str]
        Sorted list of subject IDs (e.g., ['s101', 's102']).
    """
    subids: set[str] = set()
    for d in os.listdir(cfg.fmriprep_dir):
        full_path = os.path.join(cfg.fmriprep_dir, d)
        if os.path.isdir(full_path):
            match = re.match(r'sub-s(\d+)', d)
            if match:
                subids.add('s' + match.group(1))
    return sorted(subids)

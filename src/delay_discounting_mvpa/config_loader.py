#!/usr/bin/env python3
"""
Minimal Config Loader for Delay Discounting MVPA
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Union

import yaml


class ConfigError(Exception):
    pass


def _to_path(v: Union[str, Path]) -> Path:
    """Convert string-like path values to Path objects."""
    return v if isinstance(v, Path) else Path(v)


@dataclass
class Config:
    # Required from YAML
    data_root: Path
    fmriprep_dir: Path
    bids_dir: Path
    output_root: Path
    task_name: str
    bold_func_glob: str
    bold_data_suffix: str
    mask_data_suffix: str
    behav_func_glob: str
    behav_data_suffix: str
    masks_dir: Path
    tr: float = 0.68

    # Derived fields
    bold_file_glob: str = field(init=False)
    bold_mask_file_glob: str = field(init=False)
    behav_file_glob: str = field(init=False)

    def __post_init__(self):
        # --- Ensure all path fields are Path objects ---
        path_fields = [
            'data_root',
            'fmriprep_dir',
            'bids_dir',
            'output_root',
            'masks_dir',
        ]
        for f in path_fields:
            setattr(self, f, _to_path(getattr(self, f)))

        # --- Normalize bold_func_glob (string only) ---
        if not isinstance(self.bold_func_glob, str):
            self.bold_func_glob = str(self.bold_func_glob)
        if not self.bold_func_glob.endswith('/'):
            self.bold_func_glob += '/'

        # --- Normalize behav_func_glob (string only) ---
        if not isinstance(self.behav_func_glob, str):
            self.behav_func_glob = str(self.behav_func_glob)
        if not self.behav_func_glob.endswith('/'):
            self.behav_func_glob += '/'

        # --- Derived glob patterns (still strings) ---
        self.bold_file_glob = (
            f'{self.bold_func_glob}*{self.task_name}{self.bold_data_suffix}'
        )
        self.bold_mask_file_glob = (
            f'{self.bold_func_glob}*{self.task_name}{self.mask_data_suffix}'
        )

        self.behav_file_glob = (
            f'{self.behav_func_glob}*{self.task_name}{self.behav_data_suffix}'
        )


def load_config(config_file: Union[str, Path]) -> Config:
    """Load YAML and return a Config object."""
    path = _to_path(config_file)
    if not path.exists():
        raise ConfigError(f'Config file not found: {config_file}')

    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    # Convert only *known* path fields to Path objects (not globs)
    path_keys = {
        'data_root',
        'fmriprep_dir',
        'bids_dir',
        'output_root',
        'masks_dir',
    }
    for key in path_keys:
        if key in data and isinstance(data[key], str):
            data[key] = Path(data[key])

    return Config(**data)


if __name__ == '__main__':
    cfg = load_config('config.yaml')
    print('✅ Config loaded successfully!')
    print('BOLD glob:', cfg.bold_file_glob)
    print('TR:', cfg.tr)

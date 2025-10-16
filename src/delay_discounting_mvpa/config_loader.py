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
    behavior_dir: Path
    output_root: Path
    output_dir: Path
    behavioral_output: Path
    mvpa_output: Path
    task_name: str
    bold_func_glob: str
    bold_data_suffix: str
    masks_dir: Path
    core_mask_files: Dict[str, str] = field(default_factory=dict)
    optional_mask_files: Dict[str, str] = field(default_factory=dict)
    tr: float = 0.68

    # Derived fields
    bold_file_glob: str = field(init=False)
    bold_mask_file_glob: str = field(init=False)
    resolved_core_masks: Dict[str, Path] = field(init=False)
    resolved_optional_masks: Dict[str, Path] = field(init=False)

    def __post_init__(self):
        # --- Ensure all path fields are Path objects ---
        path_fields = [
            'data_root',
            'fmriprep_dir',
            'behavior_dir',
            'output_root',
            'output_dir',
            'behavioral_output',
            'mvpa_output',
            'masks_dir',
        ]
        for f in path_fields:
            setattr(self, f, _to_path(getattr(self, f)))

        # --- Normalize bold_func_glob (string only) ---
        if not isinstance(self.bold_func_glob, str):
            self.bold_func_glob = str(self.bold_func_glob)
        if not self.bold_func_glob.endswith('/'):
            self.bold_func_glob += '/'

        # --- Derived glob patterns (still strings) ---
        self.bold_file_glob = (
            f'{self.bold_func_glob}*{self.task_name}{self.bold_data_suffix}'
        )
        self.bold_mask_file_glob = (
            f'{self.bold_func_glob}*{self.task_name}*desc-brain_mask.nii.gz'
        )

        # --- Resolve core and optional mask paths ---
        self.resolved_core_masks = {
            roi: self.masks_dir / fname for roi, fname in self.core_mask_files.items()
        }
        self.resolved_optional_masks = {
            roi: self.masks_dir / fname
            for roi, fname in self.optional_mask_files.items()
        }


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
        'behavior_dir',
        'output_root',
        'output_dir',
        'behavioral_output',
        'mvpa_output',
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
    print('Core masks:')
    for roi, path in cfg.resolved_core_masks.items():
        print(f'  {roi}: {path}')

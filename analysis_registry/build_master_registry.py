#!/usr/bin/env python3
"""
Build the master analysis registry by combining all YAML files in analyses/
and optionally generating a human-readable Markdown summary.
"""

from pathlib import Path
from typing import Any

import yaml

ANALYSIS_DIR = Path(__file__).parent / 'analyses'
MASTER_YAML = Path(__file__).parent / 'master_registry.yaml'
MASTER_MD = Path(__file__).parent / 'master_registry.md'


def load_yaml_files(yaml_dir: Path):
    """Load all YAML files in a directory and return a list of dicts."""
    all_entries = []
    for yaml_file in yaml_dir.glob('*.yaml'):
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
            all_entries.append(data)
    return all_entries


def write_master_yaml(entries, output_file: Path):
    with open(output_file, 'w') as f:
        yaml.safe_dump(entries, f, sort_keys=False)


def stringify_entry(entry: Any) -> str:
    """Convert a YAML field that may be a list or None into a string for Markdown."""
    if entry is None:
        return 'None'
    if isinstance(entry, list):
        return ', '.join(entry)
    return str(entry)


def write_markdown_summary(entries, output_file: Path):
    """Generate a simple Markdown table from the YAML entries."""
    headers = [
        'ID',
        'Name',
        'Description',
        'Code Dir',
        'Notebook',
        'Script',
        'Status',
        'Authors',
    ]
    md_lines = [
        '| ' + ' | '.join(headers) + ' |',
        '| ' + ' | '.join(['---'] * len(headers)) + ' |',
    ]

    for e in entries:
        row = [
            e.get('id', ''),
            e.get('name', ''),
            e.get('description', '').replace(
                '\n', ' '
            ),  # Flatten multiline descriptions
            e.get('code_dir', ''),
            stringify_entry(e.get('notebook_entry')),
            stringify_entry(e.get('script_entry')),
            e.get('status', ''),
            ', '.join(e.get('authors', [])),
        ]
        md_lines.append('| ' + ' | '.join(row) + ' |')

    with open(output_file, 'w') as f:
        f.write('\n'.join(md_lines))


def main():
    entries = load_yaml_files(ANALYSIS_DIR)
    write_master_yaml(entries, MASTER_YAML)
    write_markdown_summary(entries, MASTER_MD)
    print(f'Master YAML written to {MASTER_YAML}')
    print(f'Markdown summary written to {MASTER_MD}')


if __name__ == '__main__':
    main()

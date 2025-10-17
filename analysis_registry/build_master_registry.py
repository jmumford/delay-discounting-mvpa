#!/usr/bin/env python3
"""
Build the master analysis registry by combining all YAML files in analyses/
and generating a human-readable Markdown summary (block format).
"""

from pathlib import Path
import yaml

ANALYSIS_DIR = Path(__file__).parent / 'analyses'
MASTER_YAML = Path(__file__).parent / 'master_registry.yaml'
MASTER_MD = Path(__file__).parent / 'master_registry.md'


def load_yaml_files(yaml_dir: Path):
    """Load all YAML files in a directory and return a list of dicts."""
    all_entries = []
    for yaml_file in sorted(yaml_dir.glob('*.yaml')):
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
            all_entries.append(data)
    return all_entries


def write_master_yaml(entries, output_file: Path):
    with open(output_file, 'w') as f:
        yaml.safe_dump(entries, f, sort_keys=False)


def stringify_entry(entry):
    """Convert YAML lists, None, or scalars into strings."""
    if entry is None:
        return "None"
    if isinstance(entry, list):
        if not entry:
            return "None"
        return ", ".join(str(x) for x in entry)
    return str(entry)


def write_markdown_summary(entries, output_file: Path):
    """Write a section-style Markdown summary for each analysis entry."""
    md_lines = ["# Master Analysis Registry\n"]

    for e in entries:
        md_lines.append(f"## {e.get('id', 'Unknown ID')}")
        md_lines.append(f"**Name:** {e.get('name', 'None')}")
        md_lines.append(f"**Description:** {e.get('description', 'None').strip()}")
        md_lines.append(f"**Code Directory:** {e.get('code_dir', 'None')}")
        md_lines.append(f"**Dependencies:** {stringify_entry(e.get('dependencies'))}")
        md_lines.append(f"**Script Entry:** {stringify_entry(e.get('script_entry'))}")
        md_lines.append(f"**Notebook Entry:** {stringify_entry(e.get('notebook_entry'))}")
        md_lines.append(f"**Output Directory:** {stringify_entry(e.get('output_dir'))}")
        md_lines.append(f"**Hypothesis:** {stringify_entry(e.get('hypothesis'))}")
        md_lines.append(f"**Conclusion:** {stringify_entry(e.get('conclusion'))}")
        md_lines.append(f"**Notes:** {stringify_entry(e.get('notes'))}")
        md_lines.append(f"**Status:** {stringify_entry(e.get('status'))}")
        md_lines.append(f"**Last Updated:** {stringify_entry(e.get('last_updated'))}")
        md_lines.append(f"**Authors:** {stringify_entry(e.get('authors'))}")
        md_lines.append("\n---\n")

    with open(output_file, 'w') as f:
        f.write("\n".join(md_lines))


def main():
    entries = load_yaml_files(ANALYSIS_DIR)
    write_master_yaml(entries, MASTER_YAML)
    write_markdown_summary(entries, MASTER_MD)
    print(f"Master YAML written to {MASTER_YAML}")
    print(f"Markdown summary written to {MASTER_MD}")


if __name__ == '__main__':
    main()

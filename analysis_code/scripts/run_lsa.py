#!/usr/bin/env python3

import argparse

from delay_discounting_mvpa.config_loader import Config
from delay_discounting_mvpa.design_utils import create_design_matrices
from delay_discounting_mvpa.fmri_io import load_and_gm_scale_bold_data
from delay_discounting_mvpa.fmri_model import (
    compute_betas,
    save_beta_series,
)
from delay_discounting_mvpa.io_utils import load_tsv_data, resolve_file


def main(
    subid: str, hp_filter_cutoff: float, outdir: str, config_file: str = 'config.yaml'
):
    # Load config
    cfg = Config(config_file, validate=False)

    # fMRI setup
    tr = cfg.fmri.tr
    _, bold_paths, design_matrices = create_design_matrices(
        cfg, [subid], tr, hp_filter_cutoff
    )
    print(design_matrices[0].columns)

    # Load BOLD data
    print('loading data')
    data, data_masker = load_and_gm_scale_bold_data(
        cfg, subid, mask_type='brain', roi_mask_name=None
    )

    # Compute betas
    print('computing betas')
    betas = compute_betas(design_matrices[0], data)

    # Save results
    print('saving')
    save_beta_series(betas, design_matrices[0], data_masker, subid, outdir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run LSA analysis for a single subject.'
    )
    parser.add_argument('--subid', required=True, help='Subject ID (format: s###)')
    parser.add_argument(
        '--hp_filter', type=float, default=1 / 450, help='High-pass filter cutoff (Hz)'
    )
    parser.add_argument('--output_dir', required=True, help='Directory to save outputs')
    parser.add_argument(
        '--config', default='config.yaml', help='Path to configuration YAML'
    )

    args = parser.parse_args()
    main(args.subid, args.hp_filter, args.output_dir, args.config)

from typing import List, Tuple

import nibabel as nib
import numpy as np
import pandas as pd
from nilearn.glm.first_level.hemodynamic_models import spm_hrf, spm_time_derivative
from scipy.signal import fftconvolve

from delay_discounting_mvpa.config_loader import Config
from delay_discounting_mvpa.io_utils import load_tsv_data, resolve_file


def make_stick_array(
    onsets: np.ndarray,
    durations: np.ndarray,
    length: float,
    resolution: float = 0.2,
) -> np.ndarray:
    """
    Create a binary stick-function array for event onsets/durations.

    Parameters
    ----------
    onsets : np.ndarray
        Array of event onset times (in seconds).
    durations : np.ndarray
        Array of event durations (in seconds).
    length : float
        Total duration (in seconds) of the array.
    resolution : float, default=0.2
        Temporal resolution of the array (in seconds).

    Returns
    -------
    np.ndarray
        Stick function array of shape (n_points,).
    """
    n_points = int(np.ceil(length / resolution))
    sf = np.zeros(n_points, dtype=np.float32)
    for onset, dur in zip(onsets, durations):
        start_idx = int(np.floor(onset / resolution))
        end_idx = int(np.ceil((onset + dur) / resolution))
        sf[start_idx:end_idx] = 1.0
    return sf


def create_cosine_drift(cutoff_hz: float, timepoints: np.ndarray) -> np.ndarray:
    """
    Create a discrete cosine basis set for high-pass filtering.

    Parameters
    ----------
    cutoff_hz : float
        Cutoff frequency in Hz (e.g., 1/128 for a 128s cutoff).
    timepoints : np.ndarray
        Time points (in seconds).

    Returns
    -------
    np.ndarray
        Array of shape (len(timepoints), n_cosines). Empty if no cosines are needed.
    """
    t = np.array(timepoints)
    n = len(t)
    n_cos = int(np.floor(2 * (t[-1] - t[0]) * cutoff_hz))
    if n_cos < 1:
        return np.zeros((n, 0))

    dct_basis = np.zeros((n, n_cos))
    for k in range(1, n_cos + 1):
        dct_basis[:, k - 1] = np.cos(np.pi * (2 * t + 1) * k / (2 * n))
    return dct_basis


def create_design_matrix(
    events_df_long: pd.DataFrame,
    hp_filter_cutoff: float,
    oversampling: int = 20,
    tr: float = 1.0,
    num_trs: int = 100,
    verbose: bool = False,
    add_deriv: bool = False,
) -> pd.DataFrame:
    """
    Create an fMRI design matrix by convolving events with an HRF.

    Parameters
    ----------
    events_df_long : pd.DataFrame
        Long-format events DataFrame with columns 'onset', 'duration', 'trial_type'.
    hp_filter_futoff : float
        High-pass filter cutoff frequency in Hz (e.g., 1/128 for 128s cutoff).
    oversampling : int, default=20
        Temporal oversampling factor for convolution.
    tr : float, default=1.0
        Repetition time (TR) in seconds.
    num_trs : int, default=100
        Number of timepoints in the BOLD run.
    verbose : bool, default=False
        If True, print diagnostic information.
    add_deriv : bool, default=False
        If True, include HRF temporal derivative regressors.

    Returns
    -------
    pd.DataFrame
        Design matrix of shape (num_trs, n_regressors).
    """
    maxtime = tr * num_trs
    conv_resolution = tr / oversampling
    timepoints_data = np.linspace(0, maxtime, num_trs, endpoint=False)
    conv_points = int(num_trs * oversampling)
    timepoints_conv = np.linspace(0, maxtime, conv_points, endpoint=False)

    # Precompute HRF
    hrf = spm_hrf(tr, oversampling=oversampling)
    hrf_deriv = (
        spm_time_derivative(tr, oversampling=oversampling) if add_deriv else None
    )

    conv_dict: dict[str, np.ndarray] = {}

    trial_types = events_df_long['trial_type'].unique()
    if verbose:
        print(
            f'Maxtime: {maxtime}, TRs: {num_trs}, conv points: {len(timepoints_conv)}'
        )
    for trial_type in trial_types:
        trial_events = events_df_long[events_df_long['trial_type'] == trial_type]
        onsets = trial_events['onset'].values
        durations = trial_events['duration'].values

        sf_array = make_stick_array(onsets, durations, maxtime, conv_resolution)

        # Convolve with HRF using FFT
        conv_signal = fftconvolve(sf_array, hrf)[: len(sf_array)]
        conv_dict[trial_type] = conv_signal[::oversampling]  # downsample to TRs

        if add_deriv and hrf_deriv is not None:
            deriv_signal = fftconvolve(sf_array, hrf_deriv)[: len(sf_array)]
            conv_dict[f'{trial_type}_derivative'] = deriv_signal[::oversampling]
    desmtx_conv = pd.DataFrame(conv_dict, index=timepoints_data)
    desmtx_conv['constant'] = 1.0

    if hp_filter_cutoff:
        dct_basis = create_cosine_drift(hp_filter_cutoff, timepoints_data)
        dct_df = pd.DataFrame(
            dct_basis, columns=[f'cosine{i}' for i in range(dct_basis.shape[1])]
        )
        dct_df = dct_df.loc[:, dct_df.nunique() > 1]  # drop redundant columns
        desmtx_conv = pd.concat(
            [desmtx_conv.reset_index(drop=True), dct_df.reset_index(drop=True)], axis=1
        )

    return desmtx_conv


def create_design_matrices_OLD(
    cfg, subids: List[str], tr: float, hp_filter_cutoff: float
) -> Tuple[List[str], List[str], List[pd.DataFrame]]:
    """
    Create first-level design matrices for each subject.

    Returns:
        valid_subids: list of subjects successfully processed
        bold_paths: list of BOLD paths corresponding to valid subjects
        design_matrices: list of DataFrames, one per subject
        hp_filter_cutoff: high-pass filter cutoff frequency in Hz
    """
    valid_subids = []
    bold_paths = []
    design_matrices = []

    for subid in subids:
        print(f'Processing {subid}...')
        # Load behavioral data
        try:
            behav_file = resolve_file(cfg, subid, 'behav')
            events_data_loop = load_tsv_data(behav_file)
        except (FileNotFoundError, KeyError, ValueError) as e:
            print(f'Skipping {subid} (behav error): {e}')
            continue

        # Load BOLD path
        try:
            bold_file = resolve_file(cfg, subid, 'bold')
        except (FileNotFoundError, KeyError, ValueError) as e:
            print(f'Skipping {subid} (BOLD missing): {e}')
            continue

        # Try to get number of TRs from header without loading full data
        try:
            bold_img = nib.load(bold_file)  # loads header only lazily
            n_scans = bold_img.shape[-1]
            scan_duration = n_scans * tr
        except Exception as e:
            print(f'Skipping {subid} (cannot read BOLD header): {e}')
            continue

        # Prepare events DataFrame
        events = pd.DataFrame(
            {
                'onset': events_data_loop['onset'],
                'duration': events_data_loop['duration'],
                'trial_index': np.arange(len(events_data_loop)),
            }
        )

        # Remove trials with negative onsets
        num_negative = (events['onset'] < 0).sum()
        if num_negative > 0:
            print(f'{subid}: removing {num_negative} trial(s) with negative onset(s)')
            events = events[events['onset'] >= 0].reset_index(drop=True)

        # Create trial_type after filtering
        events['trial_type'] = (
            events_data_loop.loc[events.index, 'choice']
            + '_'
            + (events['trial_index'] + 1).astype(str)
        )

        # Check that all events fit within the scan duration
        max_onset = events['onset'].max()
        if max_onset > scan_duration:
            print(
                f'Skipping {subid}: last event onset ({max_onset:.2f}s) exceeds '
                f'scan duration ({scan_duration:.2f}s)'
            )
            continue

        # Make design matrix
        try:
            design_matrix = create_design_matrix(
                events[['onset', 'duration', 'trial_type']],
                hp_filter_cutoff,
                oversampling=10,
                tr=tr,
                num_trs=n_scans,
            )
        except Exception as e:
            print(f'Skipping {subid} (design matrix error): {e}')
            continue

        # Store results
        valid_subids.append(subid)
        bold_paths.append(bold_file)
        design_matrices.append(design_matrix)

    return valid_subids, bold_paths, design_matrices


def get_exclusion_data(cfg: Config) -> pd.DataFrame:
    """
    Load and preprocess the suggested_exclusions.csv file.

    Steps:
    - Read exclusions CSV from the BIDS directory under cfg.data_root.
    - Rename the 'Unnamed: 0' column to 'subject_task'.
    - Split 'subject_task' into 'subject' and 'task' columns.
    - Filter rows for task == 'discountFix'.
    - Drop redundant columns and reorder so 'subject' is first.

    Parameters
    ----------
    cfg : Config
        Configuration object containing data_root path.

    Returns
    -------
    pd.DataFrame
        Cleaned exclusions data for the discountFix task.
    """
    exclusion_file = cfg.data_root / 'BIDS' / 'suggested_exclusions.csv'

    if not exclusion_file.exists():
        raise FileNotFoundError(f'Exclusion file not found: {exclusion_file}')

    exclusion_data = pd.read_csv(exclusion_file)

    # Ensure expected column exists
    if 'Unnamed: 0' not in exclusion_data.columns:
        raise ValueError(
            f"'Unnamed: 0' column not found in {exclusion_file}. "
            'Expected subject_task labels in first column.'
        )

    # Clean up and split columns
    exclusion_data = exclusion_data.rename(columns={'Unnamed: 0': 'subject_task'})
    exclusion_data[['subject', 'task']] = exclusion_data['subject_task'].str.split(
        '_', n=1, expand=True
    )

    # Filter for discountFix
    exclusion_discount_fix = exclusion_data.query("task == 'discountFix'").copy()

    # Drop redundant and reorder columns
    exclusion_discount_fix = exclusion_discount_fix.drop(columns=['subject_task'])
    ordered_cols = ['subject'] + [
        c for c in exclusion_discount_fix.columns if c != 'subject'
    ]
    exclusion_discount_fix = exclusion_discount_fix[ordered_cols]

    return exclusion_discount_fix


def create_design_matrices(
    cfg, subids: List[str], tr: float, hp_filter_cutoff: float
) -> Tuple[List[str], List[str], List[pd.DataFrame], pd.DataFrame]:
    """
    Create first-level design matrices for each subject.

    Returns:
        valid_subids: list of subjects successfully processed
        bold_paths: list of BOLD paths corresponding to valid subjects
        design_matrices: list of DataFrames, one per subject
        status_df: DataFrame summarizing inclusion/exclusion status
    """
    valid_subids = []
    bold_paths = []
    design_matrices = []
    status_records = []

    # exclusion previously define by Patrick
    exclusion_data = get_exclusion_data(cfg)

    for subid in subids:
        print(f'Processing {subid}...')

        # --- Load behavioral data ---
        try:
            behav_file = resolve_file(cfg, subid, 'behav')
            events_data_loop = load_tsv_data(behav_file)
        except (FileNotFoundError, KeyError, ValueError) as e:
            reason = f'behav missing: {e}'
            print(f'Skipping {subid} ({reason})')
            status_records.append({'sub_id': subid, 'include': False, 'reason': reason})
            continue

        # --- Check exclusion criteria from suggested_exclusions.csv ---
        sub_excl_row = exclusion_data[exclusion_data['subject'] == subid]
        if not sub_excl_row.empty:
            # Drop 'subject' and 'task' columns, only keep columns with nonzero values
            nonzero_cols = sub_excl_row.drop(columns=['subject', 'task']).astype(bool)
            criteria_met = nonzero_cols.columns[nonzero_cols.iloc[0]].tolist()
            if criteria_met:
                reason = (
                    'met suggested_exclusion.csv criteria: ' + ', '.join(criteria_met)
                )
                print(f'Skipping {subid} ({reason})')
                status_records.append({'sub_id': subid, 'include': False, 'reason': reason})
                continue

        # --- Check for both choice types ---
        num_ss = (events_data_loop['choice'] == 'smaller_sooner').sum()
        num_ll = (events_data_loop['choice'] == 'larger_later').sum()
        if num_ss == 0 or num_ll == 0:
            reason = (
                f'singular response: {num_ss} smaller sooner / {num_ll} larger later'
            )
            print(f'Skipping {subid} ({reason})')
            status_records.append({'sub_id': subid, 'include': False, 'reason': reason})
            continue

        # --- Load BOLD path ---
        try:
            bold_file = resolve_file(cfg, subid, 'bold')
        except (FileNotFoundError, KeyError, ValueError) as e:
            reason = f'BOLD missing: {e}'
            print(f'Skipping {subid} ({reason})')
            status_records.append({'sub_id': subid, 'include': False, 'reason': reason})
            continue

        # --- Get header info ---
        try:
            bold_img = nib.load(bold_file)
            n_scans = bold_img.shape[-1]
            scan_duration = n_scans * tr
        except Exception as e:
            reason = f'cannot read BOLD header: {e}'
            print(f'Skipping {subid} ({reason})')
            status_records.append({'sub_id': subid, 'include': False, 'reason': reason})
            continue

        # --- Prepare events DataFrame ---
        events = pd.DataFrame(
            {
                'onset': events_data_loop['onset'],
                'duration': events_data_loop['duration'],
                'trial_index': np.arange(len(events_data_loop)),
            }
        )

        num_negative = (events['onset'] < 0).sum()
        if num_negative > 0:
            print(f'{subid}: removing {num_negative} trial(s) with negative onset(s)')
            events = events[events['onset'] >= 0].reset_index(drop=True)

        events['trial_type'] = (
            events_data_loop.loc[events.index, 'choice']
            + '_'
            + (events['trial_index'] + 1).astype(str)
        )

        # --- Check scan duration ---
        max_onset = events['onset'].max()
        if max_onset > scan_duration:
            reason = f'onset beyond scan duration: max onset={max_onset:.2f}s, scan duration={scan_duration:.2f}s'
            print(f'Skipping {subid}: {reason}')
            status_records.append({'sub_id': subid, 'include': False, 'reason': reason})
            continue

        # --- Try design matrix creation ---
        try:
            design_matrix = create_design_matrix(
                events[['onset', 'duration', 'trial_type']],
                hp_filter_cutoff,
                oversampling=10,
                tr=tr,
                num_trs=n_scans,
            )
        except Exception as e:
            reason = f'design matrix error: {e}'
            print(f'Skipping {subid} ({reason})')
            status_records.append({'sub_id': subid, 'include': False, 'reason': reason})
            continue

        # --- Success ---
        valid_subids.append(subid)
        bold_paths.append(bold_file)
        design_matrices.append(design_matrix)
        status_records.append(
            {'sub_id': subid, 'include': True, 'reason': 'Passed all checks'}
        )

    status_df = pd.DataFrame(status_records)
    return valid_subids, bold_paths, design_matrices, status_df

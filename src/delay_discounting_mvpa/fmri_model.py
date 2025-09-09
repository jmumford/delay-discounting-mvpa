import re
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
from nilearn.input_data import NiftiMasker


def compute_betas(
    desmat: Union[pd.DataFrame, np.ndarray],
    data_array: np.ndarray,
) -> np.ndarray:
    """
    Compute OLS beta estimates for all voxels using matrix multiplication.

    Parameters
    ----------
    desmat : pd.DataFrame or np.ndarray
        Design matrix, shape (ntime, nbetas).
    data_array : np.ndarray
        Time series data, shape (ntime, nvox).

    Returns
    -------
    betas : np.ndarray
        Estimated betas, shape (nbetas, nvox).
    """
    X = np.asarray(desmat)  # (ntime, nbetas)
    Y = np.asarray(data_array)  # (ntime, nvox)

    # Compute (X^T X)^-1
    XtX_inv = np.linalg.inv(X.T @ X)  # (nbetas, nbetas)

    # Compute betas: (X^T X)^-1 X^T Y
    betas = np.einsum('ij,jk->ik', XtX_inv @ X.T, Y)  # (nbetas, nvox)

    return betas


def save_beta_series(
    betas: np.ndarray,
    desmat: pd.DataFrame,
    data_masker: NiftiMasker,
    subid: str,
    output_dir: Union[str, Path],
) -> list[str]:
    """
    Save filtered beta series (only trial regressors) to NIfTI and CSV.

    Parameters
    ----------
    betas : np.ndarray
        Beta estimates, shape (nbetas, nvox).
    desmat : pd.DataFrame
        Design matrix with column labels (length = nbetas).
    data_masker : NiftiMasker
        Fitted masker used for inverse transform.
    subid : str
        Subject ID for file naming.
    output_dir : str or Path
        Directory to save outputs.

    Returns
    -------
    labels : list of str
        Filtered labels corresponding to betas kept.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Step 1: find trial regressors of interest
    keep_mask = desmat.columns.str.contains(r'(?:smaller|larger|false)', regex=True)
    kept_labels = desmat.columns[keep_mask]

    # Step 2: simplify names (remove trailing "_number")
    simplified_labels = [re.sub(r'_\d+$', '', lbl) for lbl in kept_labels]

    # Step 3: filter betas
    betas_kept = betas[keep_mask, :]

    # Step 4: save 4D beta image
    beta_img = data_masker.inverse_transform(betas_kept)
    beta_file = output_path / f'sub-{subid}_beta_series.nii.gz'
    beta_img.to_filename(str(beta_file))

    # Step 5: save labels to CSV
    labels_file = output_path / f'sub-{subid}_beta_labels.csv'
    pd.Series(simplified_labels, name='beta_condition').to_csv(labels_file, index=False)

    print(f'Saved beta series: {beta_file}')
    print(f'Saved labels: {labels_file}')

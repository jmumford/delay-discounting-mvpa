import sys
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from nilearn.image import resample_to_img
from nilearn.input_data import NiftiMasker

from delay_discounting_mvpa.config_loader import Config
from delay_discounting_mvpa.io_utils import (
    resolve_file,
)


def calculate_grand_mean_scale(
    cfg: Config, subid: str
) -> Tuple[float, np.ndarray, NiftiMasker]:
    """
    Compute brain scale factor and scaled whole-brain data.

    Parameters
    ----------
    cfg : Config
        Configuration object.
    subid : str
        Subject ID.

    Returns
    -------
    scale_factor : float
        Factor to scale global mean to 100.
    scaled_brain_data : np.ndarray
        2D (timepoints x voxels) scaled whole-brain data.
    brain_masker : NiftiMasker
        Fitted masker for inverse-transform.
    """
    bold_file = resolve_file(cfg, subid, 'bold')
    brain_mask_file = resolve_file(cfg, subid, 'mask')

    brain_masker = NiftiMasker(mask_img=brain_mask_file, standardize=False)
    brain_data = brain_masker.fit_transform(bold_file)

    grand_mean = brain_data.mean()
    scale_factor = 100.0 / grand_mean

    scaled_brain_data = brain_data * scale_factor
    return scale_factor, scaled_brain_data, brain_masker


def load_and_gm_scale_bold_data(
    cfg: Config,
    subid: str,
    mask_type: str = 'brain',
    roi_mask_name: Optional[str] = None,
) -> Tuple[np.ndarray, NiftiMasker]:
    """
    Load and grand mean scale BOLD data for brain or ROI.

    Note: The scale factor is 100 divided by the mean of the mean BOLD
          time series within the brain mask (even when an ROI mask is used).

    Parameters
    ----------
    cfg : Config
        Configuration object.
    subid : str
        Subject ID.
    mask_type : str, optional
        One of "brain" or "roi" (default: "brain").
    roi_mask_name : str, optional
        Filename of ROI mask (required if mask_type='roi').

    Returns
    -------
    data : np.ndarray
        Scaled time series (timepoints x voxels)
    masker : NiftiMasker
        Masker for inverse-transform

    Raises
    ------
    ValueError
        If `mask_type` is invalid or `roi_mask_name` is required but not provided.
    FileNotFoundError
        If ROI mask file does not exist.
    """
    bold_file = resolve_file(cfg, subid, 'bold')
    scale_factor, scaled_brain_data, brain_masker = calculate_grand_mean_scale(
        cfg, subid
    )

    if mask_type == 'brain':
        return scaled_brain_data, brain_masker

    if mask_type == 'roi':
        if roi_mask_name is None:
            raise ValueError("roi_mask_name must be provided for mask_type='roi'.")

        roi_mask_file = Path(cfg.masks_dir) / roi_mask_name
        if not roi_mask_file.exists():
            raise FileNotFoundError(f'ROI mask file does not exist: {roi_mask_file}')

        # Resample ROI mask to match BOLD data
        roi_mask_resamp = resample_to_img(
            roi_mask_file,
            bold_file,
            interpolation='nearest',
            force_resample=True,
            copy_header=True,
        )

        roi_masker = NiftiMasker(mask_img=roi_mask_resamp, standardize=False)
        roi_data = roi_masker.fit_transform(bold_file)
        roi_data_scaled = roi_data * scale_factor
        return roi_data_scaled, roi_masker

    raise ValueError(f'Unknown mask_type: {mask_type!r}')


def load_bold_estimates(
    cfg,
    contrast_file: Path,
    mask_type: str = 'brain',
    roi_mask_name: Optional[str] = None,
) -> Tuple[np.ndarray, NiftiMasker]:
    """
    Load unscaled BOLD estimate data (e.g., beta or contrast maps) for the whole brain
    or for a specific ROI.

    Parameters
    ----------
    cfg : Config
        Configuration object containing directory paths and other settings.
    contrast_file : Path
        Path to the input BOLD estimate file (e.g., beta-series or contrast map).
    mask_type : str, optional
        Type of mask to apply. One of {"brain", "roi"} (default: "brain").
    roi_mask_name : str, optional
        Filename of the ROI mask (required if mask_type="roi").

    Returns
    -------
    data : np.ndarray
        Unscaled voxel data with shape (timepoints x voxels) if applicable.
    masker : NiftiMasker
        Fitted NiftiMasker object for inverse transforms.

    Raises
    ------
    FileNotFoundError
        If `contrast_file` or the specified ROI mask file does not exist.
    ValueError
        If `mask_type` is invalid or `roi_mask_name` is missing for an ROI mask.
    """

    # Check that the input contrast file exists
    contrast_file = Path(contrast_file)
    if not contrast_file.exists():
        raise FileNotFoundError(f'Contrast file does not exist: {contrast_file}')

    if mask_type == 'brain':
        brain_mask_file = Path(cfg.masks_dir) / 'brain_mask.nii.gz'
        if not brain_mask_file.exists():
            raise FileNotFoundError(f'Brain mask not found: {brain_mask_file}')

        masker = NiftiMasker(mask_img=brain_mask_file, standardize=False)
        data = masker.fit_transform(contrast_file)
        return data, masker

    if mask_type == 'roi':
        if roi_mask_name is None:
            raise ValueError("roi_mask_name must be provided for mask_type='roi'.")

        roi_mask_file = Path(cfg.masks_dir) / roi_mask_name
        if not roi_mask_file.exists():
            raise FileNotFoundError(f'ROI mask file does not exist: {roi_mask_file}')

        # Resample ROI mask to match the BOLD file dimensions
        roi_mask_resamp = resample_to_img(
            roi_mask_file,
            contrast_file,
            interpolation='nearest',
            force_resample=True,
            copy_header=True,
        )

        masker = NiftiMasker(mask_img=roi_mask_resamp, standardize=False)
        data = masker.fit_transform(contrast_file)
        return data, masker

    raise ValueError(f'Unknown mask_type: {mask_type!r}')

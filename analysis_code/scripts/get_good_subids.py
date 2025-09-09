from delay_discounting_mvpa.config_loader import Config
from delay_discounting_mvpa.design_utils import create_design_matrices
from delay_discounting_mvpa.io_utils import get_subids

cfg = Config('config.yaml', validate=False)
tr = cfg.fmri.tr
subids = get_subids(cfg)
hp_filter_cutoff = 1 / 450


model_subids, bold_paths, design_matrices = create_design_matrices(
    cfg, subids, tr, hp_filter_cutoff
)

subid_outpath = '/home/users/jmumford/josh/delay-discounting-mvpa/analysis_code/scripts'

with open('good_subids.txt', 'w') as f:
    for sid in model_subids:
        f.write(f'{sid}\n')

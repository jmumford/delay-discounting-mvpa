# Master Analysis Registry

## Summary

| ID | Description | Status | Notes |
|----|------------|--------|-------|
| data_orientation | Notebooks for plotting various aspects of raw behavioral and other data as needed | ongoing | None |
| get_good_subjects | Assess each subject against multiple criteria to provide a  simple subject_status.csv in output_dir that defines  good/bad subjects and why they were excluded. | completed | Josh approved exclusion criteria |
| group_analysis_reality_check | Checking how well averaging beta maps recreates a standard analysis group map of the choice contrast. | complete | None |
| lsa_modeling | The notebook develops the code, which is then run using the batch/py files on all subjects who passes all exclusion  criteria | complete | Estimates need to be evaluated for outliers prior to further use |
| pattern_similarity_exploration | Exploring the behavior of the RSA matrices and analyses we plan to run more widely.  Focusing on relationships that should be highly powered  such as correlations with RT and differences by choice. | in progress | Get feedback from Josh |

---

## Detailed Reports

### data_orientation
**Name:** Data figure playground<br>
**Description:** Notebooks for plotting various aspects of raw behavioral and other data as needed<br>
**Code Directory:** analyses/data_orientation<br>
**Dependencies:** None<br>
**Script Entry:** None<br>
**Notebook Entry:** looking_at_data.ipynb<br>
**Output Directory:** None<br>
**Hypothesis:** NA<br>
**Conclusion:** NA<br>
**Notes:** None<br>
**Status:** ongoing<br>
**Last Updated:** 2025-10-16<br>
**Authors:** Jeanette Mumford<br>

---

### get_good_subjects
**Name:** Define subject exclusion criteria<br>
**Description:** Assess each subject against multiple criteria to provide a  simple subject_status.csv in output_dir that defines  good/bad subjects and why they were excluded.<br>
**Code Directory:** analyses/good_subjects<br>
**Dependencies:** None<br>
**Script Entry:** None<br>
**Notebook Entry:** get_good_subjects.ipynb<br>
**Output Directory:** get_good_subjects/<br>
**Hypothesis:** NA<br>
**Conclusion:** 85 subjects pass the exclusion criteria<br>
**Notes:** Josh approved exclusion criteria<br>
**Status:** completed<br>
**Last Updated:** 2025-10-16<br>
**Authors:** Jeanette Mumford<br>

---

### group_analysis_reality_check
**Name:** Assessing beta series estimates<br>
**Description:** Checking how well averaging beta maps recreates a standard analysis group map of the choice contrast.<br>
**Code Directory:** analyses/group_analysis_reality_check<br>
**Dependencies:** None<br>
**Script Entry:** None<br>
**Notebook Entry:** develop_choice_contrast_comparison.ipynb<br>
**Output Directory:** None<br>
**Hypothesis:** NA<br>
**Conclusion:** There is a very weak correspondence between the two group maps indicating there is likely low SNR in the beta map estimates.
<br>
**Notes:** None<br>
**Status:** complete<br>
**Last Updated:** 2025-10-20<br>
**Authors:** Jeanette Mumford<br>

---

### lsa_modeling
**Name:** LSA setup and execution<br>
**Description:** The notebook develops the code, which is then run using the batch/py files on all subjects who passes all exclusion  criteria<br>
**Code Directory:** analyses/lsa_modeling<br>
**Dependencies:** None<br>
**Script Entry:** run_lsa.py, run_lsa.batch<br>
**Notebook Entry:** dev_lsa_code.ipynb<br>
**Output Directory:** /oak/stanford/groups/russpold/data/uh2/aim1/derivatives/delay_discounting_mvpa/lsa_estimates<br>
**Hypothesis:** NA<br>
**Conclusion:** Models ran successfully for 77 subjects<br>
**Notes:** Estimates need to be evaluated for outliers prior to further use<br>
**Status:** complete<br>
**Last Updated:** 2025-10-17<br>
**Authors:** Jeanette Mumford<br>

---

### pattern_similarity_exploration
**Name:** Reality check analyses in motor ROI for pattern similarity<br>
**Description:** Exploring the behavior of the RSA matrices and analyses we plan to run more widely.  Focusing on relationships that should be highly powered  such as correlations with RT and differences by choice.<br>
**Code Directory:** analyses/pattern_similarity_exploration<br>
**Dependencies:** None<br>
**Script Entry:** None<br>
**Notebook Entry:** motor_roi_exploration.ipynb<br>
**Output Directory:** analyses/pattern_similarity_exploration (contains summary pdf)<br>
**Hypothesis:** Do relationships we expect to be present in the motor ROI exist?   Do RSA values differ by choice and do they relate to RT distance?
<br>
**Conclusion:** WIP, but aside from a weak correlation between BOLD/RT distances,  I don't see much here.
<br>
**Notes:** Get feedback from Josh<br>
**Status:** in progress<br>
**Last Updated:** 2025-10-20<br>
**Authors:** Jeanette Mumford<br>

---

# Master Analysis Registry

## data_orientation
**Name:** Data figure playground
**Description:** Notebooks for plotting various aspects of raw behavioral and other data as needed
**Code Directory:** analyses/data_orientation
**Dependencies:** None
**Script Entry:** None
**Notebook Entry:** get_good_subjects.ipynb
**Output Directory:** None
**Hypothesis:** NA
**Conclusion:** NA
**Notes:** None
**Status:** ongoing
**Last Updated:** 2025-10-16
**Authors:** Jeanette Mumford

---

## get_good_subjects
**Name:** Define subject exclusion criteria
**Description:** Assess each subject against multiple criteria to provide a  simple subject_status.csv in output_dir that defines  good/bad subjects and why they were excluded.
**Code Directory:** analyses/good_subjects
**Dependencies:** None
**Script Entry:** None
**Notebook Entry:** get_good_subjects.ipynb
**Output Directory:** get_good_subjects/
**Hypothesis:** NA
**Conclusion:** 77 subjects pass the exclusion criteria
**Notes:** Josh needs to approve all exclusion criteria
**Status:** completed
**Last Updated:** 2025-10-16
**Authors:** Jeanette Mumford

---

## lsa_modeling
**Name:** LSA setup and execution
**Description:** The notebook develops the code, which is then run using the batch/py files on all subjects who passes all exclusion  criteria
**Code Directory:** analyses/lsa_modeling
**Dependencies:** None
**Script Entry:** run_lsa.py, run_lsa.batch
**Notebook Entry:** dev_lsa_code.ipynb
**Output Directory:** /oak/stanford/groups/russpold/data/uh2/aim1/derivatives/delay_discounting_mvpa/lsa_estimates
**Hypothesis:** NA
**Conclusion:** Models ran successfully for 77 subjects
**Notes:** Estimates need to be evaluated for outliers prior to further use
**Status:** complete
**Last Updated:** 2025-10-17
**Authors:** Jeanette Mumford

---

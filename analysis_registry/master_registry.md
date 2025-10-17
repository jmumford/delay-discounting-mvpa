# Master Analysis Registry

## Summary

| ID | Description | Status | Notes |
|----|------------|--------|-------|
| data_orientation | Notebooks for plotting various aspects of raw behavioral and other data as needed | ongoing | None |
| get_good_subjects | Assess each subject against multiple criteria to provide a  simple subject_status.csv in output_dir that defines  good/bad subjects and why they were excluded. | completed | Josh needs to approve all exclusion criteria |
| lsa_modeling | The notebook develops the code, which is then run using the batch/py files on all subjects who passes all exclusion  criteria | complete | Estimates need to be evaluated for outliers prior to further use |

---

## Detailed Reports

### data_orientation
**Name:** Data figure playground<br>
**Description:** Notebooks for plotting various aspects of raw behavioral and other data as needed<br>
**Code Directory:** analyses/data_orientation<br>
**Dependencies:** None<br>
**Script Entry:** None<br>
**Notebook Entry:** get_good_subjects.ipynb<br>
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
**Conclusion:** 77 subjects pass the exclusion criteria<br>
**Notes:** Josh needs to approve all exclusion criteria<br>
**Status:** completed<br>
**Last Updated:** 2025-10-16<br>
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

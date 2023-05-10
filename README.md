# **SLICE** - **S**emi-supervised **L**earning approach for **I**mage segmentation of **C**rop field boundari**E**s

**AIM**: Produce accurate field boundary segmentation maps in regions with little to no ground truth labels.

**METHOD**: Semi-supervised Instance segmentation

**TRACKER**: Notion [link](https://www.notion.so/SLICE-1a7a0d79974943c2bc19831db9738c35?pvs=4)

---

### Guidelines

- Following semantic versioning with ```Major.Minor.Patch```
- Every small changes will come under ```patch``` version. (bugfix, bug)
- Every feature introduction will change the ```minor``` version.
- Every interface logic change will change the ```major``` version.
- Example of the versioning
  - 2.0.005
    - Major version - 2
    - Minor Version - 0
    - Patch Version - 005
  - Always create a new branch for a feature introduction and raise a pull request accordingly.
  - Releases will be tagged either ```Pre Release``` or ```Latest Release``` from the main branch only.
  - Git commits will have the changelogs description as the commit message. e.g. **2.0.005 (feature+update)**
  - Definition of keywords
    - **feature** - Any introduction of a new feature
    - **bug** - With the commited change the system is in a buggy state.
    - **bugfix** - for any patches applied over a bug.
    - **update** - general updates like updating readme. (this won't increment any version numbers)
    - **experimental** - This stays out of the main branch unless the experiment is solidified to create a feature out of it.

---

### Changelogs

##### 0.0.1 (feature + bugfix)
- Added Segment Anything Project as a submodule.
- Fixed and issue with the setup_sol.sh file.

##### 0.0.2 (feature)
- Added code to extract tf record.
- Added code to generate pseudo masks for the image dataset using SAM.

##### 0.0.3 (bug + bugfix)
- The conversion code for tf record is not working properly. -> BUG
- Added script for downloading the model checkpoints.
- Made path changes in generate_pseudo_masks.sh file.

##### 0.0.4 (feature + bugfix)
- Conversion for TFrecord
- Extract images script for inference
- Output visualization script .ipynb
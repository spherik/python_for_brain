# python_for_brain
Various scripts and jupyter notebooks with python code for brain image analysis and visualization

### Dependencies

To execute these scripts and jupyter notebooks I've used conda to create an environment and get the necessary libraries:
1. Download and install [Anaconda](https://www.anaconda.com/download/)
1. Create an environment:
```bash
conda env create -n brain_env
source activate brain_env
```
1. Install necessary packages:
```bash
conda install -n brain_env jupyter ipython numpy scipy scikit-learn nibabel matplotlib
pip install nilearn nipype
```

## nilearn_brain_atlases.ipynb

Jupyter notebook with different [nilearn atlases](http://nilearn.github.io/modules/reference.html#module-nilearn.datasets) plots.  

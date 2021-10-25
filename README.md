# Supplementary code and data for Sims-Williams (2022), Token frequency as a determinant of morphological change.


## Code

*lepage_py3.py*

A Python 3 implementation of the algorithm described in section 2.2.1 of the paper.

*Token frequency as a determinant of morphological change.ipynb*

A jupyter notebook (https://jupyter.org/) which runs through each step of the model with comments and generates tables, figures and statistics used in the paper.
This can be viewed online as static output or downloaded and run (quickstart instructions: https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/index.html).


## Data Files

*synchronic_data.csv* – Synchronic Greek data (aorist active indicative forms) described in section 2.1.1.

*diachronic_data.csv* – Diachronic Greek data consisting of changes to the forms in the synchronic data, described in section 2.1.2. 

*cell_frequency.csv* – Token frequency statistics from a selection of Greek authors writing in the Attic dialect. See section 2.3 for details. These figures were derived from:

 - The *Perseus Project's* corpus of Greek texts: http://www.perseus.tufts.edu/hopper/opensource/download

 - Morphological analyses and wordlists packaged as part of the *Diogenes* software package, created by Peter Heslin: https://d.iogen.es/d/. The data can be downloaded at https://github.com/pjheslin/diogenes-prebuilt-data and ultimately comes from the Perseus Project's *Morpheus* parsing tool: https://github.com/PerseusDL/morpheus

*regression_data.csv* – Logistic regression data for section 4.1, showing effect of base and target frequency on the probability that an analogical proportion generates a diachronically attested form.

*combined_model_data.csv* – Logistic regression data for section 4.3, showing the effect of the probability score calculated as described in section 4.2.



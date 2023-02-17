This repository contains the extra material about the article "Attribute Inference Attacks in Online Multiplayer Video Games: a Case Study on Dota 2", accepted at the 13th ACM Conference on Data and Application Security and Privacy (ACM CODASPY). If you use any of the resources contained herein, we kindly ask you to cite our paper:

```
@inproceedings{tricomi2022attribute,
  title={{Attribute Inference Attacks in Online Multiplayer Video Games: a Case Study on Dota2}},
  author={Tricomi, Pier Paolo and Facciolo, Lisa and Apruzzese, Giovanni and Conti, Mauro},
  booktitle={Proc. 13th ACM Conference on Data and Application Security and Privacy (CODASPY)},
  year={2023}
}
```

A preprint version of our paper can be found here: [arXiv link](https://arxiv.org/abs/2210.09028)

# Description

This repository contains 3 folders:

* **supplementary**, which contains some supplementary documents for better understanding our paper (and referenced in our paper);
* **correlation_heatmaps**, which contains all the correlation heatmaps of our analyses;
* **code**, which contains the code we developed for our analyses.

For privacy reasons, we cannot disclose our dataset.

## "Supplementary" folder

This folder contains three files:

* *dataset_features_explanation.pdf*, providing the list and descriptions of the features used for our analysis;
* *survey_dota.pdf*, containing the entire questionnaire used for our survey;
* *appendix.pdf*, containing the appendix of our paper (which could not be included in the version submitted to the ACM DL).

## "Correlation heatmaps" folder

Here, we provide the heatmaps relative to Cramer and Spearman indices for the appropriate target features and several significance thresholds (0.01, 0.05, and 0.1). We recall that our analyses are divided in two "levels": _match_ and _player_ (i.e., the "M" and "P" datasets mentioned in our paper). Therefore "match level" and "player level" folders contain plots for the respective studies. Files are available in the pdf format and their names follow the scheme: analysis level_correlation metric_threshold.
Note that in the "match level" directory there are two subfolders, one containing correlations measured on the whole match dataset (all matches, i.e., "M"), and one with correlations computed with at maximum 30 matches by every player and additional features related to chat analysis (i.e., the "distilled" version of "M"). In this last case, files are preceded by the prefix "reduced_" and then respect the same name format reported above.

## "Code" folder

This folder contains three files:

* *hyperparameters.py*, including the details of our hyperparameter optimization;
* *match-lvl_extract_chat.py*, containing he code for extracting the "chat features";
* *code_correlations.py*, where the code used to compute correlations is presented. 

Note that, for the *code_correlations.py* is only meant for illustrative purposes, and hence is just a snippet (we cannot share the various datasets due to ethical reasons). Values relative to attribute names and thresholds are arbitrary, considering the explanatory purpose of the file. The same holds for *match-lvl_extract_chat.py*, which reports the code used to create chat features with domain knowledge.

# Contact

For any inquiry on the material contained in this repository, contact Pier Paolo Tricomi (tricomi.pierpaolo@math.unipd.it).

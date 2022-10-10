This repository contains the extra material about the article "Attribute Inference Attacks in Online Multiplayer Video Games: a Case Study on Dota 2". We suggest to download the files you are interested in, since there may be some problems due to the rendering of the anonymization tool. 

File "dataset_features_explanation.pdf" provides the list and the descriptions per groups of the features used for both analysis levels. The code for the "chat features" is also provided in the root of this repository.

The "hyperparameters.py" file includes the details of our hyperparameter optimization.

In file "surver_dota.pdf" are reported the questions asked for the data collection. Note that, in the very first page, a brief description of survey's structure is provided.

Inside the "correlation heatmaps" directory, one can found heatmaps relative to Cramer and Spearman indices for the appropriate target features and several significance thresholds (0.01, 0.05, and 0.1). Once again analysis is distinguished per levels, therefore "match level" and "player level" folders contain plots for the respective studies. Files are available in the pdf format and their names follow the scheme: analysis level_correlation metric_threshold.
Note that in the "match level" directory there are two subfolders, one containing correlations measured on the whole match dataset (all matches), and one with correlations computed with at maximum 30 matches by every player and additional features related to chat analysis (reduced). In this last case, files are preceded by the prefix "reduced_" and then respect the same name format reported above.

Finally, we also provide the "code_correlations.py" file, where the code used to compute correlations is presented. Note that this is only done in order to provide an example of snippet, since we cannot share the various datasets due to ethical reasons. Values relative to attribute names and thresholds are arbitrary, considering the explanatory purpose of the file. The same holds for "match-lvl_extract_chat.py", which reports the code used to create chat features with domain knowledge.

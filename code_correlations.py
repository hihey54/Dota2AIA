#imports 
import pandas as pd
import numpy as np
import math
from  scipy import stats

#definition of auxiliary methods
def cramers_V(var1,var2) :
    """
    Returns Cramer's V p-value and correlation coefficient between var1 and va2. 
    It calculates chi square statistics, together with its p-value in order to assess the 
    significance of the correlation, and then computes Cramer using its formula definition.
    """

    #build the cross table
    crosstab = np.array(pd.crosstab(var1,var2, rownames=None, colnames=None))

    #store statistics and p-value of chi square test
    chi2 = stats.chi2_contingency(crosstab)[0]
    p_value = stats.chi2_contingency(crosstab)[1]

    #compute V using its formula
    obs = np.sum(crosstab)
    mini = min(crosstab.shape)-1
    return math.sqrt(chi2/(obs*mini)), p_value


def Cramer(targets, attributes):
    """
    Given two dataframes with categorical columns, targets and attributes, returns matrices 
    of Cramer's coeffiecients and p-values for the correlation of every column of targets for
    all the columns of attributes.
    """
    #create dataframes to store the outputs
    mat = pd.DataFrame(columns=list(attributes.columns), dtype=float)
    p_mat = pd.DataFrame(columns=list(attributes.columns), dtype=float)
    
    for y in targets.columns:
        for x in attributes.columns:

            #compute correlation intensity and p-value
            v, p = cramers_V(targets[y], attributes[x])

            #update dataframes
            mat.loc[y, x] = v 
            p_mat.loc[y, x] = p
    
    return mat, p_mat

def Spearman(targets, attributes):
    """
    Given dataframe targets with categorical columns and dataframe attributes with numerical ones,
    returns matrices of Spearman's coeffiecients and p-values for the correlation of every column 
    of targets for all the columns of attributes.
    """
    #create dataframes to store the outputs
      
    mat = pd.DataFrame(columns=list(attributes.columns),dtype=float) #matrix of correlation indeces 
    p_mat = pd.DataFrame(columns=list(attributes.columns), dtype=float) #matrix of p_values
    
    for y in targets.columns:
        for x in attributes.columns:

            #compute correlation intensity and p-value
            rho, p = stats.spearmanr(targets[y], attributes[x]) 

            #update dataframes
            mat.loc[y, x] = rho
            p_mat.loc[y, x] = p
    
    return mat, p_mat


###1. dataset loading
data = pd.read_csv('dataset.csv')
# note: remember to drop constant columns, since they do not provide any information
updated = data.loc[:, (data != data.iloc[0]).any()] 
data.drop(columns=[el for el in data.columns if el not in updated.columns], inplace=True)

###2. declaration of target features and of categorical variables
target_features = ['gender', 'age', 'occupation', 'purchase_habits', 'extraversion', 'agreeableness', 'conscientiousness', 'neuroticism', 'openness']
X_categorical = ['account_id', 'dota_plus', 'top_hero_pr_attr', 'top_hero_melee_atk', 'top_hero_complexity', 'top_hero_gender', 'top_hero_species']

data[target_features + X_categorical] = data[target_features + X_categorical].astype('category')

###3. declaration of ordinal targets and numerical attributes
target_ordinal = ['age', 'purchase_habits', 'extraversion', 'agreeableness', 'conscientiousness', 'neuroticism', 'openness']
X_numerical = [el for el in data.columns if el not in target_features+X_categorical]

for el in target_ordinal:
    data[el].cat.as_ordered(inplace=True)

###4. correlations

#Cramer - correlations between categorical variables
#be careful to not include account id
cramer_mat, cramer_p_mat = Cramer(data[target_features], data[X_categorical[1:]])
#only keep significant (i.e. p-values < th) indices
th_cr = 0.01
cramer_corr = cramer_mat[cramer_p_mat < th_cr]
#if you want to consider only significant coefficients with value > th_cr_coef
th_cr_coef = 0.1
cramer_corr = cramer_corr[cramer_corr > th_cr_coef]
#drop now rows/columns with all NaNs
cramer_corr.dropna(axis=0, how='all', inplace=True)
cramer_corr.dropna(axis=1, how='all', inplace=True)
print(cramer_corr)

#Spearman - correlations between ordinal and numerical variables
spearman_mat, spearman_p_mat = Spearman(data[target_ordinal], data[X_numerical])
#only keep significant (i.e. p-values <th) indexes
th_sp = 0.01
spearman_corr = spearman_mat[spearman_p_mat < th_sp]
#if you want to consider only significant coefficients with value > th_sp_coef
th_sp_coef = 0.1
spearman_corr = spearman_corr[abs(spearman_corr) > th_cr_coef]
#drop now rows/columns with all NaNs
spearman_corr.dropna(axis=0, how='all', inplace=True)
spearman_corr.dropna(axis=1, how='all', inplace=True)
print(spearman_corr)
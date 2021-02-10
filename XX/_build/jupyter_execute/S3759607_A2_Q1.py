I solemnly swear that I have not discussed my assignment solutions with anyone in any way and the solutions I am submitting are my own personal work.

Full Name: Wei Zhang

Student ID: S3759607

## Question 1 - Part A

First, read the csv file into the notebook and check the first 5 rows.

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

data1 = pd.read_csv('A2_Q1.csv', sep = ',')

data1.head()

`Annual_Income` column is selected. Calculate the probability distribution of each type of income in target feature. 

income = data1['Annual_Income']
income_probs = income.value_counts(normalize=True)
income_probs

One way to measure impurity degree is using entropy. Recall that Shannon's model defines entropy as
$$H(x) := - \sum_{i=1}^{\ell}(P(t=i) \times \log_{2}(P(t=i))$$
Then we calculate the impurity of the `Annual_Income` feature using the entropy criterion.

entropy = -1 * np.sum(np.log2(income_probs) * income_probs)
entropy.round(3)

Another way to measure impurity degree is using Gini index. It is defined as 
$$ \mbox{Gini}(x) := 1 - \sum_{i=1}^{\ell}P(t=i)^{2}$$
The impurity of the `Annual_Income` feature using Gini index is calculated as below.

gini = 1 - np.sum(np.square(income_probs))
gini.round(3)

### Part B

Dataset is sorted by the continuous `Age` feature in ascending order. Then the whole dataset is displayed as below.

data1.sort_values(by='Age')

By looking at `Age` and `Annual_Income` features, candidate `Age` thresholds are decided: ≥24, ≥27, ≥38 and ≥42. The four thresholds are chosen as they are the age point when income level changes. Therefore, 4 new columns answering whether the age is over the given thresholds are added to the dataset as below. Masks are used to achieve this.

mask24 = data1['Age'] >= 24
mask27 = data1['Age'] >= 27
mask38 = data1['Age'] >= 38
mask42 = data1['Age'] >= 42
data1['Age≥24'] = mask24
data1['Age≥27'] = mask27
data1['Age≥38'] = mask38
data1['Age≥42'] = mask42
data1.head()

As `ID` and `Age` columns are not used as splitting features for impurity calculation, we remove the `ID` and `Age` column in this dataset.


data1_new = data1.drop(['ID', 'Age'], axis=1)
data1_new.head()

For convenience, we define a function called `compute_gini()` that calculates the impurity of a feature using Gini Index. We use this function to calculate the impurity of `Annual_Income` feature in the original dataset again.

def compute_gini(feature):
    probs = feature.value_counts(normalize=True)
    impurity = 1 - np.sum(np.square(probs))
    return(round(impurity, 3))
compute_gini(income)

Next, a new function is defined to calculate the information gain for certain feature using Gini Index.

def comp_feature_infor_gain_gini(df, target, feature):
    """
    This function calculates information gain for splitting on a particular descriptive feature for
    a given dataset using Gini Index.
    """
    print('target feature: ', target)
    print('descriptive_feature: ', feature)
    
    target_gini = compute_gini(df[target])
    
    gini_list = list()
    weight_list = list()
    
    for value in df[feature].unique():
        df_feature_value = df[df[feature] == value]
        gini_value = compute_gini(df_feature_value[target])
        gini_list.append(round(gini_value, 3))
        weight = len(df_feature_value) / len(df)
        weight_list.append(round(weight, 3))
        
    print('impurity of partitions: ', gini_list)
    print('weights of partitions: ', weight_list)
    
    feature_remain_gini = round(np.sum(np.array(gini_list)*np.array(weight_list)), 3)
    print('remaining impurity: ', feature_remain_gini)
    
    information_gain = round(target_gini - feature_remain_gini, 3)
    print('information_gain: ', information_gain)
    
    print('=========')

Now we will call this function for each descriptive feature in the dataset. A for-loop is used to calculate the information gain for each of the descriptive features.

for feature in data1_new.drop(columns = 'Annual_Income').columns:
    feature_info_gain = comp_feature_infor_gain_gini(data1_new, 'Annual_Income', feature)

Based on the output above, using Gini Index the highest information gain occurs with the age threshhold at 24. 

df_splits = pd.DataFrame(columns = ['Split', 'Remainder', 'Information_Gain', 'Is_Optimal'])
df_splits.loc[len(df_splits)] = ['Education', 0.537, 0.018, False]
df_splits.loc[len(df_splits)] = ['Marital_Status', 0.468, 0.087, False]
df_splits.loc[len(df_splits)] = ['Occupation', 0.433, 0.122, False]
df_splits.loc[len(df_splits)] = ['Age_24', 0.353, 0.202, True]
df_splits.loc[len(df_splits)] = ['Age_27', 0.36, 0.195, False]
df_splits.loc[len(df_splits)] = ['Age_38', 0.529, 0.026, False]
df_splits.loc[len(df_splits)] = ['Age_42', 0.473, 0.082, False]
df_splits

### Part C

Assume `Education` feature is at the root node, this dataset is first splitted based on Education value.

data1['Education'].unique()

The dataset is then splitted into 3 subsets based on the education level.

edu_bachelors = data1[data1['Education'] == 'bachelors']
edu_doctorate = data1[data1['Education'] == 'doctorate']
edu_hs = data1[data1['Education'] == 'high school']

edu_bachelors.head()

edu_doctorate.head()

edu_hs.head()

A for-loop is created to calculate the income distribution in each subset.

for df in [edu_bachelors, edu_doctorate, edu_hs]:
    probs = df['Annual_Income'].value_counts(normalize=True)
    print('Income probability')
    print(probs)

According to above output, we have the following predictions.

df_prediction = pd.DataFrame(columns = ['Leaf_Condition', 'Low_Income_Prob', 'Mid_Income_Prob', 'High_Income_Prob', 'Leaf_Prediction'])
df_prediction.loc[len(df_prediction)] = ['Education==high school', 0.25, 0.50, 0.25, 'mid']
df_prediction.loc[len(df_prediction)] = ['Education==bachelors', 0.125, 0.625, 0.25, 'mid']
df_prediction.loc[len(df_prediction)] = ['Education==doctorate', 0, 0.75, 0.25, 'mid']
df_prediction

# Part B answer, age at 24 gives the best information gain and therefore can be used at root node.
df_splits


```{toctree}
:hidden:
:titlesonly:


S3759607_A2_Q2
WebScrapingExample
HealthNeedsAssessment2021
```

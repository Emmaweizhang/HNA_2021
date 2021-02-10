## Mice Cortex Analysis

### Retrieving and Preparing the Data 

#import warnings
#warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None) 

data = pd.read_csv('Data_Cortex_Nuclear.csv', sep = ',')
data.head()

print ("Rows: ",data.shape[0])
print ("Columns: ",data.shape[1])

An overview of data size and the first 5 rows shows that no information is lost after retrieving from UCI. 
Column names are:
- 1. Mouse ID
- 2-78. Values of expression levels of 77 proteins; the names of proteins are followed by `_N` indicating that they were measured in the nuclear fraction. 
- 79. Genotype: control (c) or trisomy (t)
- 80. Treatment type: memantine (m) or saline (s)
- 81. Behavior: context-shock (CS) or shock-context (SC)
- 82. Class: c-CS-s, c-CS-m, c-SC-s, c-SC-m, t-CS-s, t-CS-m, t-SC-s, t-SC-m

print("Columns: \n",data.columns.tolist())

# check data types and missing values
data.info()

data.isnull().sum()

Data types are all reasonable, but missing values exist. There are many protein columns that have 3 missing values, which indicate empty rows? As it only accounts for 0.28% of the rows, it's safe to remove.

DYRK1A_percent_missing = data['DYRK1A_N'].isnull().sum() * 100 / len(data)
DYRK1A_percent_missing

data1 = data[data['DYRK1A_N'].notna()]
data1.info()

#data1[data1['ELK_N', 'MEK_N', 'Bcatenin_N'].notna()]
data2 = data1.dropna(axis=0, subset=('ELK_N', 'MEK_N', 'Bcatenin_N'))
data2.shape

data2.info()

#BAD_N              849 non-null float64
#BCL2_N             777 non-null float64
#pCFOS_N            972 non-null float64
#H3AcK18_N          867 non-null float64
#EGR1_N             852 non-null float64
#H3MeK4_N           777 non-null float64
for col in ['BAD_N', 'BCL2_N', 'pCFOS_N', 'H3AcK18_N', 'EGR1_N', 'H3MeK4_N']:
    percent_missing = data2[col].isnull().sum() * 100 / len(data2)
    print(col, 'percentage of missing values:', percent_missing)

Number of missing values in columns 'BAD_N', 'BCL2_N', 'pCFOS_N', 'H3AcK18_N', 'EGR1_N', 'H3MeK4_N' are all over 5%. It's not a good idea to remove NULL in this case. We'll replace NULL with mean.

for col in ['BAD_N', 'BCL2_N', 'pCFOS_N', 'H3AcK18_N', 'EGR1_N', 'H3MeK4_N']:
    data2[col].fillna(data2[col].mean(), inplace=True)
data2.info()

# An overview of the data
data2.describe(include = np.object)

data2.describe(include = np.number).round(3)

data3 = data2.drop(['MouseID'], axis = 1)
data3.shape

# Check Unique values in object feature
object_col = data3.columns[data3.dtypes==object].tolist()

for col in object_col:
    print('The unique values and numbers of', col, 'are:')
    print(data3[col].value_counts())
    print('=========')

According to the output and the dataset description, column `class` contain the information in `Genotype`, `Treatment` and `Behavior` already. Therefore, they can be dropped in data4.

Use `data4` for modelling, but we'll use `data3` for the exploration.

data4 = data3.drop(['Genotype', 'Treatment', 'Behavior'], axis = 1)
data4.shape

data4.head()

We end up with a data with 77 descriptive features (proteins) and one target feature (class).

### Data exploration

import altair as alt
alt.data_transformers.disable_max_rows()

#### Single column 

import matplotlib.pyplot as plt

alt.Chart(data3, width=400).mark_bar().encode(x=alt.X('class', sort='-y'), y='count()').properties(
    title='Number of Measurements for each class')

Target feature values are not quite balanced according to the bar chart.

# Boxplot for column 'DYRK1A_N'
data3.boxplot(column = 'DYRK1A_N')
plt.title("Box Plot Distribution of 'DYRK1A_N' Column")
plt.ylabel('Expression Levels')
plt.show()

The Box Plot Distribution of 'DYRK1A_N' Column shows that this protein level distribution is quite skewed. In particular, there are some outliers shown in the box plot. It's unclear if they are true outliers or just skewed data, so they won't be removed at this stage. Further investigation is needed to understand this feature more.

for-loop is used to explore the box plot distribution of 8 other columns as below.

for col in ['ITSN1_N', 'BDNF_N', 'NR1_N', 'NR2A_N', 'pAKT_N', 'pERK_N', 'pJNK_N', 'PKCA_N']:
    data3.boxplot(column = col)
    plt.title("Box Plot Distribution of Protein Expression Levels")
    plt.ylabel('Expression Levels')
    plt.show()

alt.Chart(data3).mark_bar().encode(
    alt.X("pBRAF_N", bin=alt.Bin(extent=[0.1, 0.325], step=0.0125)),
    y='count()').properties(title='Histogram distribution of protein expression')

Histogram of pBRAF_N and pCAMKII_N protein expression levels are right-skewed as per the output. 

alt.Chart(data3).mark_bar().encode(alt.X('pCAMKII_N', bin=alt.Bin(extent=[1, 7.5], step=0.5)), y = 'count()').properties(
        title='Histogram distribution of protein expression')

#### Relationship between pairs of attributes 

alt.Chart(data3, width=500).mark_boxplot().encode(y='CaNA_N', x='class').properties(
    title='Box Plot of CaNA_N level by Class')

alt.Chart(data3, width=300).mark_boxplot().encode(y='EGR1_N', x='Genotype').properties(
    title='Box Plot of EGR1_N level by Genotype')

alt.Chart(data3, width=300).mark_boxplot().encode(y='SYP_N', x='Behavior').properties(
    title='Box Plot of SYP_N level by Behavior')

alt.Chart(data3, width=300).mark_boxplot().encode(y='H3MeK4_N', x='Treatment').properties(
    title='Box Plot of H3MeK4_N level by Treatment')

alt.Chart(data3).mark_point().encode(x='SNCA_N', y='Ubiquitin_N').properties(
    title='Scatter plot for SNCA_N vs. Ubiquitin_N')

alt.Chart(data3).mark_point().encode(x='PSD95_N', y='pCASP9_N').properties(
    title='Scatter plot for PSD95_N vs. pCASP9_N')

alt.Chart(data3).mark_point().encode(x='P3525_N', y='IL1B_N').properties(
    title='Scatter plot for P3525_N vs. IL1B_N')

alt.Chart(data3).mark_point().encode(x='GluR4_N', y='GluR3_N').properties(
    title='Scatter plot for GluR4_N vs. GluR3_N')

alt.Chart(data3).mark_point().encode(x='GFAP_N', y='Tau_N').properties(
    title='Scatter plot for GFAP_N vs. Tau_N')

alt.Chart(data3).mark_point().encode(x='nNOS_N', y='ERBB4_N').properties(
    title='Scatter plot for nNOS_N vs. ERBB4_N')

### Data Modelling using two Classiﬁcation models

#### Feature encoding and scaling

# descriptive features
Data = data4.drop(columns = 'class')
# target feature
target = data4['class']

target.shape

target_names = data4['class'].unique()

target.value_counts()

target = target.replace({'c-SC-m': 0, 'c-CS-m':1, 't-SC-m':2, 't-CS-m':3, 't-SC-s':4, 'c-SC-s':5, 'c-CS-s':6, 't-CS-s':7})
target.value_counts()

Data.shape

from sklearn import preprocessing

Data_df = Data.copy()

Data_scaler = preprocessing.MinMaxScaler()
Data_scaler.fit(Data)
Data = Data_scaler.fit_transform(Data)

pd.DataFrame(Data).head()

df = pd.DataFrame(Data, columns=Data_df.columns)
df.shape

df.head()

#### Feature selection

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from sklearn.utils import shuffle
new_Ind = [] 
cur_MaxScore = 0
col_num = 77 
col_Ind_Random = shuffle(range(0, col_num), random_state=1)

for cur_f in range(0, col_num):
    new_Ind.append(col_Ind_Random[cur_f])
    newData = Data[:, new_Ind]
    D_train, D_test, t_train, t_test = train_test_split(newData,
                                                       target,
                                                       test_size = 0.3,
                                                       random_state=0)
    clf = KNeighborsClassifier(5, weights='distance', p=1)
    fit=clf.fit(D_train, t_train)
    cur_Score = clf.score(D_test, t_test)
    if cur_Score < cur_MaxScore:
        new_Ind.remove(col_Ind_Random[cur_f])
    else:
        cur_MaxScore = cur_Score
        print("Score with " + str(len(new_Ind))+" selected features: "+str(cur_Score))

print("There are " + str(len(new_Ind)) + " features selected:")

print(new_Ind)

dataset = pd.DataFrame(Data[:, new_Ind], columns=Data_df.columns[new_Ind])

dataset.shape

dataset.head()

D_train, D_test, t_train, t_test = train_test_split(dataset,
                                                   target,
                                                   test_size=0.3,
                                                   stratify=target.values,
                                                   random_state=999)

print(D_train.shape)
print(D_test.shape)
print(t_train.shape)
print(t_test.shape)

### KNN
There are several hyperparameters for KNN, for instance

- number of neighbors
- weights
- the type of distance p 

Build the KNN classifier with 5 neighbors

KNN_5 = KNeighborsClassifier(5)
fit = KNN_5.fit(D_train, t_train)
t_pre = fit.predict(D_test)

t_pre.shape

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(t_test, t_pre)
print(cm)

from sklearn.metrics import classification_report
print(classification_report(t_test, t_pre))

### Hyperparameter tunning
While keeping 'n_neighbors = 5', different parameters are set for 'weights' and 'p'.

KNN_5_w = KNeighborsClassifier(5, weights = 'distance')
fit = KNN_5_w.fit(D_train, t_train)
t_pre = fit.predict(D_test)
cm = confusion_matrix(t_test, t_pre)
print(cm)
print(classification_report(t_test, t_pre))

It seems that weights helped with the accuracy. While keeping'n_neighbors = 5' and weights, we set p value to 1.

KNN_5_w_1 = KNeighborsClassifier(5, weights = 'distance', p = 1)
fit = KNN_5_w_1.fit(D_train, t_train)
t_pre = fit.predict(D_test)
cm = confusion_matrix(t_test, t_pre)
print(cm)
print(classification_report(t_test, t_pre))

p=1 or p=2 produces similar accuracy rate. Let's try lower number of neighbors with p = 2.

KNN = KNeighborsClassifier(4, weights = 'distance', p = 2)
fit = KNN.fit(D_train, t_train)
t_pre = fit.predict(D_test)
cm = confusion_matrix(t_test, t_pre)
print(cm)
print(classification_report(t_test, t_pre))

Let's use grid search to see what's the best number of neighbors to usem

#### Using grid search method

from sklearn.model_selection import StratifiedKFold, GridSearchCV

cv_method = StratifiedKFold(n_splits=3,shuffle=True, random_state=999)

# define the parameter values
KNN_para = {'n_neighbors': [1, 2, 3, 4, 5,6, 7], 'p': [1, 2]}
KNN_gs = GridSearchCV(KNeighborsClassifier(weights = 'distance'), KNN_para, cv=cv_method, scoring = 'accuracy')

KNN_gs.fit(D_train, t_train)

KNN_gs.best_params_

KNN_gs.best_estimator_

KNN_gs.best_score_

KNN_results=pd.DataFrame(KNN_gs.cv_results_)[['mean_test_score', 'std_test_score', 'params']]
KNN_results_sorted=KNN_results.sort_values('mean_test_score', ascending=False)
KNN_results_sorted.head()

Using the best method from grid search and test it on testing set

clf = KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
                     metric_params=None, n_jobs=None, n_neighbors=2, p=2,
                     weights='uniform')
fit = clf.fit(D_train, t_train)
t_pre = fit.predict(D_test)
cm = confusion_matrix(t_test, t_pre)
print(cm)
print(classification_report(t_test, t_pre))

Better results than others. However, t test will need to be conducted to know if this model is significantly better than others. 
Also, when k =1, the model is likely to be overfitting.

#### DecisionTree

Train and evaluate the model appropriately.

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state = 999)
fit = clf.fit(D_train, t_train)
t_pre = fit.predict(D_test)
t_pre.shape

cm = confusion_matrix(t_test, t_pre)
print(cm)
print(classification_report(t_test, t_pre))
print(clf.tree_.max_depth)

Set entropy as the criterion

clf = DecisionTreeClassifier(criterion = 'entropy',random_state = 999)
fit = clf.fit(D_train, t_train)
t_pre = fit.predict(D_test)
t_pre.shape
cm = confusion_matrix(t_test, t_pre)
print(cm)
print(classification_report(t_test, t_pre))
print(clf.tree_.max_depth)

clf = DecisionTreeClassifier(criterion = 'entropy',min_samples_split = 10, random_state = 999)
fit = clf.fit(D_train, t_train)
t_pre = fit.predict(D_test)
t_pre.shape
cm = confusion_matrix(t_test, t_pre)
print(cm)
print(classification_report(t_test, t_pre))
print(clf.tree_.max_depth)

Using entropy slightly improve the performance. Now set max_depth as 5.

clf = DecisionTreeClassifier(criterion = 'entropy',max_depth = 5,min_samples_split = 10, random_state = 999)
fit = clf.fit(D_train, t_train)
t_pre = fit.predict(D_test)
t_pre.shape
cm = confusion_matrix(t_test, t_pre)
print(cm)
print(classification_report(t_test, t_pre))
print(clf.tree_.max_depth)

clf = DecisionTreeClassifier(max_depth = 5, min_samples_split = 10, min_samples_leaf=10, random_state = 999)
fit = clf.fit(D_train, t_train)
t_pre = fit.predict(D_test)
t_pre.shape
cm = confusion_matrix(t_test, t_pre)
print(cm)
print(classification_report(t_test, t_pre))
print(clf.tree_.max_depth)

params_DT = {'max_depth': [5, 8, 10, 12], 'min_samples_split': [5, 10, 15], 'min_samples_leaf': [5, 10, 15]}

gs_DT = GridSearchCV(DecisionTreeClassifier(criterion = 'entropy'), 
                          param_grid=params_DT, 
                          cv=cv_method,
                          scoring='accuracy') 

gs_DT.fit(D_train, t_train)

gs_DT.best_params_

gs_DT.best_estimator_

gs_DT.best_score_

DT_results=pd.DataFrame(gs_DT.cv_results_)[['mean_test_score', 'std_test_score', 'params']]
DT_results_sorted=DT_results.sort_values('mean_test_score', ascending=False)
DT_results_sorted.head()

clf = DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=8,
                       max_features=None, max_leaf_nodes=None,
                       min_impurity_decrease=0.0, min_impurity_split=None,
                       min_samples_leaf=5, min_samples_split=10,
                       min_weight_fraction_leaf=0.0, presort=False,
                       random_state=None, splitter='best')
fit = clf.fit(D_train, t_train)
t_pre = fit.predict(D_test)
t_pre.shape
cm = confusion_matrix(t_test, t_pre)
print(cm)
print(classification_report(t_test, t_pre))
print(clf.tree_.max_depth)

from sklearn import tree
with open('mice_protein.dot', 'w') as f:
    f=tree.export_graphviz(clf, out_file=f, feature_names = dataset.columns,
                          class_names=target_names, filled=True, rounded=True,
                          special_characters=True)
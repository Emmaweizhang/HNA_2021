I solemnly swear that I have not discussed my assignment solutions with anyone in any way and the solutions I am submitting are my own personal work.

Full Name: Wei Zhang

Student ID: S3759607

## Question 2, Part A

#!pip install --upgrade altair

#!pip install vega vega_datasets

First, read the csv file into the notebook and check the first 5 rows.

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

data2 = pd.read_csv('A2_Q2.csv', sep = ',')
data2.head()

Use the score of 0.5 as the threshold. A new column `Prediction` is created based on the `Score` feature. Above the threshold of 0.5, the prediction is positive (True). Otherwise, the prediction becomes negative (False).

data2['Prediction'] = data2['Score'] >= 0.5
data2.head()

pd.crosstab(data2.Target, data2.Prediction, margins=True)

Above is the confusion matrix for the given model.
Now we calculate the metrics based on the confusion matrix to answer Part B.

### Part B

Compute the following 5 metrics:

- Error Rate
- Precision
- TPR (True Positive Rate) (also known as Recall)
- F1-Score
- FPR (False Positive Rate)

# Error Rate
error_rate = round((6+4)/30, 3)
error_rate

# Precision
Precision = round(9/(9+6), 3)
Precision

#TPR (True Positive Rate) (also known as Recall)
Recall = round(9/(9+4), 3)
Recall

#F1-Score: harmonic mean of precision and recall
F1 = round(2 * (Precision*Recall)/(Precision+Recall), 3)
F1

# FPR (False Positive Rate)
FPR = round(6/(11+6), 3)
FPR

df_metrics = pd.DataFrame(columns = ['Metric', 'Value'])
df_metrics.loc[len(df_metrics)] = ['Error Rate', error_rate]
df_metrics.loc[len(df_metrics)] = ['Precision', Precision]
df_metrics.loc[len(df_metrics)] = ['TPR(Recall)', Recall]
df_metrics.loc[len(df_metrics)] = ['F1-Score', F1]
df_metrics.loc[len(df_metrics)] = ['FPR', FPR]

df_metrics

### Part C

Create a for-loop to calculate the TPR and FPR at different thresholds.

thresholds = []
tpr_list = []
fpr_list = []
for threshold in np.arange(0.1, 1, 0.1):
    
    # create new column 'Prediction_new' as per this threshold, and store this threshold in the list
    data2['Prediction_new'] = data2['Score'] >= threshold
    thresholds.append(threshold)
    
    # calculate the number of true positives (Target and Prediction_new columns are both True value)
    # calculate the number of actual positive values based on Target column
    # store the true positive rates in the list
    true_positive = len(data2[(data2.Target == True)&(data2.Prediction_new == True)])
    positive = len(data2[data2.Target == True])
    TPR = round(true_positive / positive, 3)
    tpr_list.append(TPR)
    print('TPR for threshold ',threshold, 'is ', TPR)
    
    # calculate the number of false positives (Target is Falise and Prediction_new columns is True)
    # calculate the number of False values based on Target column
    # store the false positive rates in the list
    false_positive = len(data2[(data2.Target == False)&(data2.Prediction_new == True)])
    negative = len(data2[data2.Target == False])
    FPR = round(false_positive / negative, 3)
    fpr_list.append(FPR)
    print('FPR for threshold ', threshold, 'is ', FPR)
    print('============')

df_roc = pd.DataFrame({'Threshold': thresholds, 'TPR': tpr_list, 'FPR': fpr_list})
df_roc

# Part B answer, compare when threshold=0.5, the results agree with that in df_metrics
df_metrics

### Part D
Using the answer in the above part, an ROC curve with appropriate axes labels and a title are displayed.  ROC (Receiver Operating Characteristic) curves.

import altair as alt
alt.renderers.enable('notebook')

base = alt.Chart(df_roc, 
                 title='ROC Curve at Different Thresholds'
                ).properties(width=300)

roc_curve = base.mark_line(point=True).encode(
    alt.X('FPR', title='False Positive Rate (FPR)',  sort=None),
    alt.Y('TPR', title='True Positive Rate (TPR) (a.k.a Recall)'),
)

roc_rule = base.mark_line(color='green').encode(
    x='FPR',
    y='TPR',
    size=alt.value(2)
)

(roc_curve + roc_rule).interactive()
# Jobseeker Analysis

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None) 

js_april = pd.read_csv('jobseeker-april.csv', sep = ',',skiprows=6)
js_april.head()

sa = pd.read_csv('SA2_2016_AUST.csv')
sa.head()

sa2 = sa[['SA2_5DIGITCODE_2016', 'SA2_NAME_2016', 'STATE_NAME_2016']]
sa2.head()

sa2.shape

js_march = pd.read_csv('jobseeker-march.csv', sep = ',', skiprows=6)
js_march.head()

js_april = js_april.iloc[0:2292, 1:3]
js_march = js_march.iloc[0:2292, 1:3]
js_april['Month'] = 4
js_march['Month'] = 3

js = pd.concat([js_april, js_march],ignore_index=True)
js.shape

#pd.merge(df1, df3, left_on="employee", right_on="name").drop('name', axis=1)
js=pd.merge(js, sa2, left_on='SA2 Name', right_on='SA2_NAME_2016').drop('SA2_NAME_2016', axis=1)
js.head()

indexNames = js[js['JobSeeker Payment'] == '<5'].index
 
# Delete these row indexes from dataFrame, rows with '<5' value
js.drop(indexNames , inplace=True)

js['JobSeeker Payment'] = js['JobSeeker Payment'].str.split(',').str.join('').astype(int)

js

import altair as alt
alt.data_transformers.disable_max_rows()

select_month = alt.selection_single(
    name='Select', fields=['Month'], init={'Month': 3},
    bind=alt.binding_range(min = 1, max = 12, step= 1)
)

chart = alt.Chart(js).mark_bar().encode(
    x=alt.X('Number of JobSeeker Payment'),
    y=alt.Y('SA2 Name', sort='-x'),
    tooltip=['SA2 Name','JobSeeker Payment']
).properties(title='SA2 with Top10 Number of JobSeeker Payment each Month'
).add_selection(select_month
).transform_filter(select_month
).transform_window(
    rank='rank(JobSeeker Payment)',
    sort=[alt.SortField('JobSeeker Payment', order='descending')]
).transform_filter(alt.datum.rank < 10)

chart

select_month = alt.selection_single(
    name='Select', fields=['Month'], init={'Month': 3},
    bind=alt.binding_range(min = 1, max = 12, step= 1)
)
selection = alt.selection_multi(fields=['STATE_NAME_2016', 'Month'])

color = alt.condition(select_month,
                      alt.Color('STATE_NAME_2016:N', legend=None),
                      alt.value('lightgray'))

chart = alt.Chart(js).mark_bar().encode(
    x=alt.X('Number of JobSeeker Payment:Q'),
    y=alt.Y('SA2 Name', sort='-x'),
    tooltip=['SA2 Name','JobSeeker Payment']
).properties(title='SA2 with Top10 Number of JobSeeker Payment each Month'
).add_selection(select_month
).transform_filter(select_month
).transform_window(
    rank='rank(JobSeeker Payment)',
    sort=[alt.SortField('JobSeeker Payment', order='descending')]
).transform_filter(alt.datum.rank < 10)

legend = alt.Chart(js).mark_rect().encode(
    y=alt.Y('STATE_NAME_2016:N', axis=alt.Axis(orient='right')),
    x='Month:O',
    color=color
).add_selection(
    select_month
)

chart | legend

#conda install -c conda-forge altair_saver

#chart.save('chart.html')

#chart.save('chart.html', embed_options={'renderer':'svg'})
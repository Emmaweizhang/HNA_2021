## COVID Immunization planning

import numpy as np
import pandas as pd

clinic = pd.read_excel('296 GP clinics.xlsx')
clinic.head()

import altair as alt
alt.data_transformers.disable_max_rows()

conda install -c conda-forge altair

clinic.head()

select_tier = alt.selection_single(
    name='Select', fields=['Tier'], init = {'Tier': 1},
    bind=alt.binding_range(min = 1, max = 6, step = 1)
)

selection = alt.selection_multi(fields = ['NIP only', 'Tier'])

color = alt.condition(select_tier, 
                     alt.Color('NIP only:N', legend = None),
                     alt.value('lightgray'))

chart = alt.Chart(clinic).mark_bar().encode(
    x = alt.X('Postcode:Q'),
    y = alt.Y('Practice name', sort = '-x'),
    tooltip = ['Practice name', 'Postcode']
).properties(title='GP clinics for immunization'
            ). add_selection(select_tier).transform_filter(select_tier).transform_window(rank='rank(Postcode)',
                                                                                        sort=[alt.SortField('Postcode', order='descending')]
                                                                                        )

legend = alt.Chart(clinic).mark_rect().encode(
    y=alt.Y('NIP only:N', axis=alt.Axis(orient='right')),
    x='Tier:O', color=color).add_selection(select_tier)

chart | legend


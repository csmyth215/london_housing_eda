import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

changes_df = pd.read_csv('../raw_data/focus_borough_changes.csv', index_col=[0])

# Confirm data set structure:
changes_df.info()

# Explore changes in population by age bracket
age_changes = changes_df.groupby(['borough'])[['18_24_change', '25_34_change', '35_44_change', 
'45_54_change','55_64_change', '65+_change']].sum(numeric_only=True).unstack(level=0).reset_index()
age_changes = age_changes.rename(columns={'level_0': 'age_band', 0: 'net_pop_change'})
age_changes.replace(to_replace=['18_24_change', '25_34_change', '35_44_change', '45_54_change',
 '55_64_change', '65+_change'], value=['18 to 24', '25 to 34', '35 to 44', '45 to 54', 
 '55 to 64', '65+'], inplace=True)

# Colour steeps red, slights yellow
steeps = ['westminster', 'kensington and chelsea', 'city of london', 'hackney', 'islington']
slights = ['hounslow', 'bexley', 'sutton', 'havering', 'croydon']
age_changes.loc[age_changes['borough'].isin(steeps), 'rank'] = 'steep'
age_changes.loc[age_changes['borough'].isin(slights), 'rank'] = 'slight'
pal = {'steep': '#e31a1c', 'slight': '#fed976'}

g = sns.FacetGrid(age_changes, col='age_band', hue ='rank', palette=pal, col_wrap=6,  height=4, aspect=.5)
g = g.map(plt.bar, 'borough', 'net_pop_change')
g = g.map(plt.axhline, y=0, color='grey', linewidth=2)
g = g.set_titles('{col_name}')
for ax in g.axes.flat:
    for label in ax.get_xticklabels():
        label.set_rotation(90)

font = {'size': 8}
g = g.set_ylabels('Population Change', fontdict=font)
g = g.fig.suptitle('Figure 8 - Net Population Change, 2015 vs 2002')
plt.tight_layout()
plt.subplots_adjust(top=0.8)
# plt.savefig('Fig8_net_pop_change_by_age_band.png')

""" 
Biggest change in 25-34 age group.  
Price hikes in Hackney and Kensington and Chelsea cannot, however, be explained by this population change:
Opposite phenomena: Hackney with biggest 25-34 increase, K&C with biggest decrease.
"""


g2 = sns.FacetGrid(age_changes, col='borough', hue ='rank', palette=pal, col_wrap=5,)
g2 = g2.map(plt.bar, 'age_band', 'net_pop_change')
g2 = g2.map(plt.axhline, y=0, color='grey', linewidth=2)
g2 = g2.set_titles('{col_name}')
for ax in g2.axes.flat:
    for label in ax.get_xticklabels():
        label.set_rotation(90)
g2.set_ylabels('Net Population Change', fontdict=font)
g2 = g2.fig.suptitle('Figure 9 - Net Population Change, 2015 vs 2002')
plt.tight_layout()
plt.subplots_adjust(top=0.8)
# plt.savefig('Fig9_net_pop_change_by_borough.png')

"""
City of London population almost stagnant.  
Hike in prices therefore not due primarily to population change.
"""
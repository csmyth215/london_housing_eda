import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

regional_view = pd.read_csv('C:/Users/csmyth/Desktop/Code/london_housing_eda/regions_dataset.csv')

# Confirm data set structure
regional_view.info()
regional_view['date'] = pd.to_datetime(regional_view['date'])
regional_view['date'] = regional_view['date'].dt.strftime('%Y')

first = regional_view['date'].min()
last = regional_view['date'].max()

# Compare regions
mean_regional_price = regional_view.groupby('area')['average_price'].mean().astype('int64').sort_values(ascending=True).reset_index()
mean_regional_sales_count = regional_view.groupby('area')['houses_sold'].mean().astype('int64').reset_index()
averages = pd.merge(mean_regional_price, mean_regional_sales_count, how='left', on='area')
averages.to_markdown()

"""London by far most expensive region, 
yet average London number of houses sold below South East and almost matched by North West
P15Y Housing picture in Yorshire similar to that in the Midlands.
"""

# Show trends in annual sales per region
g = plt.figure()
g = sns.FacetGrid(regional_view, col='area', col_wrap=5,)
g = g.map(plt.plot, 'date', 'houses_sold', color='dimgrey').set(xlim=(first, last), xticks=['1995', '2008', '2019'])
g = g.map(plt.fill_between, 'date', 'houses_sold', alpha=0.2, color='darkgrey')
g = g.set_titles("{col_name}")
g = g.set_axis_labels('Year', 'N sold')

plt.subplots_adjust(top=0.8, left=0.125)
g = g.fig.suptitle('Figure 1 - Count of houses sold per region')
plt.savefig('Fig1_annual_house_sale_count_per_region.png')

""" 2008 financial crisis noticeable. """ 
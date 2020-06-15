import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../raw_data/pops_sales_and_prices.csv', index_col=[0])

# Ascertain correlations between Year, Population, House Sales, and Sell Prices:
grid = sns.pairplot(df, vars=['year', 'all_ages', 'houses_sold', 'average_price'], kind="reg", diag_kind=None, 
plot_kws={'color': 'dimgrey', 'line_kws':{'color':'red'}}, diag_kws={'color': 'dimgrey'})

years = df['year'].unique().tolist()
print(years)
grid.axes[0, 0].set_xticks([years[3], years[8], years[13]])
grid.axes[0, 3].set_yticks([years[3], years[8], years[13], 2020])
plt.title('Figure 4')
plt.tight_layout()
# plt.savefig('Fig4_pops_sales_prices_pairplot.png')

""" 
Intuitive correlations/trends:
1. As house sales increase, average house price decreases;
2. As population increases, house sales increase.
-- -- Both only slight trends (low gradients of regression lines). -- -- 

Other observations:
a) Two separate increases in house sales - 2002-2007 / 2008-2015.  
-- -- Sales activity hadn't returned to pre-2008 level by 2015; -- -- 
-- -- Sell price had exceeded 2008 level in some boroughs; -- --
b) Increasing number of expensive price outliers in recent years; 
-- -- Increasing gap in purchase price between majority of boroughs and most expensive boroughs. -- -- 
"""

# Next analysis step: Borough-view - rank and focus in on 10 most significant boroughs
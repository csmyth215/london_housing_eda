import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

borough_view = pd.read_csv('C:/Users/csmyth/Desktop/Code/london_housing_eda/borough_dataset.csv')

# Confirm data set structure:
borough_view.info()
borough_names = borough_view['area'].unique().tolist()
borough_view = borough_view.rename(columns={'area': 'borough'})
borough_view['date'] = pd.to_datetime(borough_view['date'])

# Compare boroughs:

# 1. Show how monthly sell price varies per borough:
plt.figure()
boxes = sns.boxplot(x='borough', y='average_price', data=borough_view, color='dimgrey', )
boxes.set_xticklabels(borough_names, rotation=90)
boxes.set_title('Fig2')
boxes.set_xlabel('')
boxes.set_ylabel('Monthly average sell price 1995 - 2019 (£)')
plt.tight_layout()
plt.savefig('Fig2_borough_sell_prices_boxplot.png')

""" Kensington and Chelsea, Westminster, City of London, Camden, 
Hammersmith and Fulham have biggest ranges.
The majority of other boroughs noticeably have third quartile close to the median, 
suggesting prices closely grouped slightly above median. """

# 1b. Later Revision after focus boroughs established.
steeps = ['westminster', 'kensington and chelsea', 'city of london', 'hackney', 'islington']
slights = ['hounslow', 'bexley', 'sutton', 'havering', 'croydon']
""" Use Colorbrewer to highlight focus boroughs """
pal = {borough: "#e31a1c" if borough in steeps else "#fed976" if borough in slights else "dimgrey" for borough in borough_names}

boxes2 = sns.boxplot(x='borough', y='average_price', data=borough_view, palette=pal)
boxes2.set_xticklabels(borough_names, rotation=90)
boxes2.set_xlabel('')
boxes2.set_title('Fig5')
boxes2.set_ylabel('Figure 5 - Monthly average sell price 1995 - 2019 (£)')
plt.tight_layout()
plt.savefig('Fig5_borough_sell_prices_boxplot(2).png')


# 2. Rank boroughs based on average sell price:

##  Simple Mean:
mean_borough_price = borough_view.groupby('borough')['average_price'].mean().astype('int64').sort_values(ascending=False)
mean_borough_price.to_markdown()

### Consistent rank:
borough_view['monthly_rank'] = borough_view.groupby(['date'])['average_price'].rank(ascending=False).astype('int64')

### Top 10 most consistently among the most expensive boroughs each month:
top_10 = borough_view.groupby(['borough'])['monthly_rank'].sum().sort_values(ascending=True).head(10).reset_index()
expensive_boroughs = top_10['borough'].tolist()
top_10_prices = borough_view.loc[borough_view['borough'].isin(expensive_boroughs)]

fig, ax = plt.subplots()
ax = sns.lineplot(data=top_10_prices, x='date', y='monthly_rank', hue='borough', palette='YlOrRd')
ax.invert_yaxis()
ax.set_ylim(10, 0)
plt.title('''Figure 6
10 Boroughs most consistently showing highest monthly average sell price; 
their rank among all London boroughs over time''', fontsize=8)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.tight_layout()
plt.savefig("Fig6_top_10_expensive_boroughs_ranked.png")


""" Kensington and Chelsea and Westminster consistently most expensive, despite outliers and large IQR in prices. 
Haringey only enters Top 10 consistently in latest decade.
City of London has biggest rise in rankings, starting low.
Barnet shows the opposite, dropping out of Top 10. """
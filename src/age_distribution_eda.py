import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

df = pd.read_csv('../raw_data/borough_changes.csv', index_col=[0])

# Confirm data set structure:
df.info()
df['year'] = df['year'].astype('str')

boroughs = df['borough'].unique().tolist()
variables = ['45_54', 'houses_sold', 'average_price']



views = []
for borough in boroughs:
    borough_view = [borough, ]
    for variable in variables:
        start_df = df.loc[(df['borough'] == borough) & (df['year'] == '2002')]
        start = start_df[variable].values[0]

        end_df = df.loc[(df['borough'] == borough) & (df['year'] == '2015')]
        end = end_df[variable].values[0]

        borough_view.append(start)
        borough_view.append(end)
    views.append(borough_view)

gen_x = pd.DataFrame(views)
gen_x.columns = ['borough', '2002_x_pop', '2015_x_pop', '2002_sales', '2015_sales', '2002_price', '2015_price']

gen_x['pop_pct_change'] = 100 * gen_x['2015_x_pop'] / gen_x['2002_x_pop']
gen_x['sales_change'] = 100 * gen_x['2015_sales'] / gen_x['2002_sales']
gen_x['price_change'] = 100 * gen_x['2015_price'] / gen_x['2002_price']

gen_x_changes = gen_x[['pop_pct_change', 'sales_change', 'price_change']]
corr = gen_x_changes.corr()

fig = plt.figure(figsize=(6, 4))
correlation = sns.heatmap(corr, annot=True, cmap='YlOrRd')
correlation.set_yticklabels(labels=['45-54 population', 'sales', 'price'], rotation=45, ha='right', )
correlation.set_xticklabels(labels=['45-54 population', 'sales', 'price'], rotation=45, ha='right')
plt.title('Correlations between changes in 45-54 populations,\n house sales and house prices\n', fontdict={'size': 12})
fig.tight_layout()
plt.tight_layout()


plt.show()

# Consider % of borough population in each age bracket:
age_columns = df.columns[3:10].tolist()
for bracket in age_columns:
    df[f'{bracket}_fraction'] = df[bracket] / df['all_ages']
borough_view = df.groupby(['borough', 'year']).sum(numeric_only=True).reset_index()

# Plot sales and prices against population age %:
fig, ax = plt.subplots(1,2, figsize=(12, 6))

colours = plt.cm.get_cmap('YlOrRd')
current_colour = 0

for age_fraction in ['minor_fraction', '18_24_fraction', '25_34_fraction', '35_44_fraction', '45_54_fraction', 
'55_64_fraction', '65+_fraction']:
    plt.subplot(1, 2, 1)
    plt.scatter(x=(borough_view[age_fraction] * 100), y=borough_view['houses_sold'], label=age_fraction[:-9], 
    c=np.array([colours(current_colour)]))
    plt.title('Monthly sales against borough age distribution')
    plt.ylabel('N houses sold (monthly)')
    plt.ylim(0, 14000)
    plt.xlabel('% Borough Population')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.scatter(x=(borough_view[age_fraction] * 100), y=borough_view['average_price'], label=age_fraction[:-9], 
    c=np.array([colours(current_colour)]))
    plt.title('Average house sell price against borough age distribution')
    plt.ylabel('Average Sell Price (£)')
    plt.ylim(0, 1400000)
    plt.xlabel('% Borough Population')
    plt.grid(True)

    current_colour += 0.125

plt.legend()
plt.suptitle('Fig10')
plt.subplots_adjust(top=0.8)
plt.tight_layout()
#plt.savefig('Fig10_sales_prices_against_borough_age_distribution.png')

""" The most expensive boroughs have small disparity between size of age groups.  
Fewest houses sold in areas with highest proportions of minors and 25-34 year olds """
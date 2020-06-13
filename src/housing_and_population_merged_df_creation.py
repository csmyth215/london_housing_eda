import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Compare and merge ages and prices data sets:

ages = pd.read_csv('C:/Users/csmyth/Desktop/Code/london_housing_eda/population_dataset_bracketed.csv', index_col=[0])
prices = pd.read_csv('C:/Users/csmyth/Desktop/Code/london_housing_eda/borough_dataset.csv')


# Confirm data set structure:
ages.info()
prices.info()
ages['year'] = ages['year'].astype('str')
prices['date'] = pd.to_datetime(prices['date']).dt.strftime('%Y')

# match appelations:
ages['borough'] = ages['borough'].str.lower()
prices = prices.rename(columns={'date': 'year', 'area': 'borough'})
# check appelations and counts match:
boroughs1 = set(ages['borough'].unique().tolist())
boroughs2 = set(prices['borough'].unique().tolist())
shared_values = boroughs1.intersection(boroughs2)
len(boroughs1), len(boroughs2), len(shared_values)

# Group ages by borough:
borough_ages = ages.drop(columns=['ward_code', 'ward_name'])
borough_ages = borough_ages.groupby(['borough', 'year']).sum().reset_index()

# Group house sales and prices by borough and year:
annual_sales = prices.groupby(['borough', 'year'])['houses_sold'].sum().astype('int64').reset_index()
mean_annual_prices = prices.groupby(['borough', 'year'])['average_price'].mean().astype('int64').reset_index()
annual_housing = pd.merge(annual_sales, mean_annual_prices, how='left', on=['borough', 'year'])

# Create borough population and housing data set:
df = pd.merge(borough_ages, annual_housing, how='left', on=['borough', 'year'])
df.to_csv('pops_sales_and_prices.csv')
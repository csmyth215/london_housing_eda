import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Import housing data set:
housing_df = pd.read_csv('../raw_data/housing_in_london_monthly_variables.csv')

# Understand data set structure:
housing_df.info()
housing_df.head()
housing_df['date'] = pd.to_datetime(housing_df['date'])

"""
1. NaN values noticeable in houses_sold and no_of_crimes.  
Former to be analysed; latter not expected to be required in this EDA
"""

# Understand area and code referents:
sales_per_area = housing_df['houses_sold'].groupby(housing_df['area']).sum().sort_values(ascending=False)
housing_df['area'].unique()
unique_codes = housing_df['code'].unique()

"""
2. England data at four levels: Country, England NUTS I, London Inner and Outer, London Borough
"""

# Test hypothesis that codes beginning E090... are London:
codes = housing_df['area'].groupby(housing_df['code']).unique()
london_boroughs = housing_df[housing_df['code'].str.startswith('E090')]
london_boroughs['area'].unique()

gss_map = {'E09': 'London Borough', 'E12': 'English Region', 'E13': 'Inner/Outer London', 'E92': 'Country'}
housing_df['GSS_prefix'] = housing_df['code'].str[:3]
housing_df['area_type'] = housing_df['GSS_prefix'].map(gss_map)
housing_df[housing_df['area_type'] == 'Country']
sales_by_area_type = housing_df['houses_sold'].groupby(housing_df['area_type']).sum().sort_values(ascending=False)

"""
3. English Region numbers show fewer houses sold than in Country, when they should be the same.
"""

regions = housing_df['area'][housing_df['area_type'] == 'English Region'].unique()
"""
4. Hackney appears incorrectly as English region i.e. incorrectly listed against 'E13' code
"""

# Identify if "hackney" area appearing as both borough and region is duplication:
hackney = housing_df[housing_df['area'].str.contains('hackney')]
hackney[hackney['area_type'] == 'English Region']
hackney[hackney['date'] == '1998-04-01']

# Remove duplicate entry:
duplicate = housing_df[(housing_df['area'] == 'hackney') & (housing_df['area_type'] == 'English Region') 
& (housing_df['date'] == '1998-04-01')]
clean_housing_df = housing_df.drop([3354])
clean_housing_df['area'].groupby(clean_housing_df['code']).unique()

# Examine and resolve other NaN in 'houses_sold':
missing_values = clean_housing_df.isna().sum()
missing_sales_numbers = clean_housing_df[clean_housing_df['houses_sold'].isnull() == True]
clean_housing_df.set_index('date', inplace=True, drop=False)
dec19_jan20 = clean_housing_df.loc['2019-12-01' : '2020-01-01']
nineties_enfield = clean_housing_df[clean_housing_df['area'] == 'enfield'].loc['1995-09-01':'1996-03-01']
nineties_tower_hamlets = clean_housing_df[clean_housing_df['area'] == 'tower hamlets'].loc['1995-09-01':'1996-03-01']
se = clean_housing_df[clean_housing_df['code'] == 'E09000012'].loc['1998-01-01':'1998-06-01']

""" 
5. No data yet available for Dec 2019 and Jan 2020;
Enfield and Tower Hamlets both have duplicate entries for 1996-02-01; 
Hackney has a duplicate entry for 1998-04-01.
Now confident that remaining rows containing houses_sold == NaN can be dropped.
"""
clean_housing_df.dropna(subset=['houses_sold'], inplace=True)
clean_housing_df.info()

# Filter to look at regions (data output to csv for further analysis):
regions = clean_housing_df[clean_housing_df['area_type'] == 'English Region']
region_df = regions[['area', 'average_price', 'houses_sold']].groupby('area').resample('A').agg({'average_price': 'mean', 'houses_sold': 'sum'})
region_df.to_csv('../raw_data/regions_dataset.csv')

# Filter to look at London boroughs (data output to csv for further analysis):
boroughs = clean_housing_df[clean_housing_df['area_type'] == 'London Borough']
boroughs[['area', 'average_price', 'houses_sold']].to_csv('../raw_data/borough_dataset.csv')
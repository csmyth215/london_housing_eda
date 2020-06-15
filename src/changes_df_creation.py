import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../raw_data/pops_sales_and_prices.csv', index_col=[0])

# Confirm data set structure:
df.info()

# Create column for each age bracket, houses sold and average price, in each borough, 
# with annual change and year-on-year percentage change:
column_names = df.columns.tolist()
int_column_names = column_names[2: ]
for column_name in int_column_names:
    df[f'{column_name}_change'] = df.groupby(['borough'])[column_name].diff()
    df[f'{column_name}_pct_change'] = df.groupby(['borough'])[column_name].pct_change()
df.to_csv('../raw_databorough_changes.csv')

# Select focus boroughs identified from 2002-2015 comparison:
steeps = ['westminster', 'kensington and chelsea', 'city of london', 'hackney', 'islington']
slights = ['hounslow', 'bexley', 'sutton', 'havering', 'croydon']
focus_df = df[(df['borough'].isin(steeps)) | (df['borough'].isin(slights))].copy()
focus_df.to_csv('../raw_datafocus_borough_changes.csv')

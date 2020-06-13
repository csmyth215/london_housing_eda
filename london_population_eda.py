import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ages = pd.read_csv('C:/Users/csmyth/Desktop/Code/london_housing_eda/ward-mid-year-estimates-sya-since-2002.csv')

# Explore and tidy data:

ages.columns.tolist()
ages.info()
ages.isna().sum()
total_pop_column = ages.columns[4]
ages = ages.rename(columns={total_pop_column: 'all_ages', 'Year': 'year', 'WD12CD': 'ward_code', 'WD12NM': 'ward_name', 'LAD12NM': 'borough', })
# Check format changes:
head_view = ages.iloc[:6, :6]

# Check plausibility - 2002, 2015 and average annual population per borough:
annual_borough_pop = ages.groupby(['borough', 'year'])['all_ages'].sum().reset_index()
avg_borough_pop = annual_borough_pop.groupby('borough')['all_ages'].mean().astype('int64')
min_borough_pop = annual_borough_pop.groupby('borough')['all_ages'].min().astype('int64')
max_borough_pop = annual_borough_pop.groupby('borough')['all_ages'].max().astype('int64')

first_year = annual_borough_pop[annual_borough_pop['year'] == 2002]
last_year = annual_borough_pop[annual_borough_pop['year'] == 2015]
first_year_pop = first_year['all_ages'].sum()
last_year_pop = last_year['all_ages'].sum()

data = {'min_pop': min_borough_pop, 
'max_pop': max_borough_pop, 'mean_pop': avg_borough_pop}
pop_trends = pd.DataFrame(data, columns=data.keys())
pop_trends.sort_values(by='mean_pop', inplace=True, ascending=False)
#Fig3
print(pop_trends.to_markdown())

""" Croydon most populous borough; City of London by far the least. """


# Bucket ages - Under 18s:
ages['minor'] = ages[['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10', 'm11', 
'm12', 'm13', 'm14', 'm15', 'm16', 'm17', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 
'f9', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17']].sum(1)

# Check first bucket creation:
ages['minor'].head()
ages.iloc[:6, 4:22]

# Bucket remaining ages:
ages['18_24'] = ages[['m18', 'm19', 'm20', 'm21', 'm22', 'm23', 'm24', 
'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24',]].sum(1)
ages['25_34'] = ages[['m25', 'm26', 'm27', 'm28', 'm29', 'm30', 'm31', 'm32', 'm33', 'm34', 
'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34']].sum(1)
ages['35_44'] = ages[['m35', 'm36', 'm37', 'm38', 'm39', 'm40', 'm41', 'm42', 'm43', 'm44', 
'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44']].sum(1)
ages['45_54'] = ages[['m45', 'm46', 'm47', 'm48', 'm49', 'm50', 'm51', 'm52', 'm53', 'm54', 
'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54']].sum(1)
ages['55_64'] = ages[['m55', 'm56', 'm57', 'm58', 'm59', 'm60', 'm61', 'm62', 'm63', 'm64', 
'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64']].sum(1)
ages['65+'] = ages[['m65', 'm66', 'm67', 'm68', 'm69', 'm70', 'm71', 'm72', 'm73', 
'm74', 'm75', 'm76', 'm77', 'm78', 'm79', 'm80', 'm81', 'm82', 'm83', 'm84', 'm85', 
'm86', 'm87', 'm88', 'm89', 'm90plus', 'f65', 'f66', 'f67', 'f68', 'f69', 'f70', 
'f71', 'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f79', 'f80', 'f81', 
'f82', 'f83', 'f84', 'f85', 'f86', 'f87', 'f88', 'f89', 'f90plus']].sum(1)

# Check age-bracket accuracy:
recent_year = ages[ages['year'] == 2015]
totals = [recent_year['minor'].sum(),
recent_year['18_24'].sum(), 
recent_year['25_34'].sum(),
recent_year['35_44'].sum(),
recent_year['45_54'].sum(),
recent_year['55_64'].sum(),
recent_year['65+'].sum()]

total_pop = 0
for x in totals:
    total_pop += x

# Create separate files for further analysis: 
# (i) SYA population 
# (ii) Population by age bracket:

column_names = ages.columns.tolist()
overview_columns = ['ward_code', 'year', 'ward_name', 'borough', 'all_ages', 'minor', '18_24', '25_34', '35_44', '45_54',
'55_64', '65+']
breakdown_columns = ['ward_code', 'year', 'ward_name', 'borough', ]
for name in column_names:
    if name not in overview_columns:
        breakdown_columns.append(name)

age_overview = ages[overview_columns]
age_breakdown = ages[breakdown_columns]
age_overview.to_csv('population_dataset_bracketed.csv')
age_breakdown.to_csv('population_dataset_sya.csv')
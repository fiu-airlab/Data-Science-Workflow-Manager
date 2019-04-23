import pandas as pd

# Import the csv files created by the other scripts
df_oil_mean = pd.read_csv('../Data/Oil_senior_project.csv').set_index('DATE')
df_cpi_un = pd.read_csv('../Data/CPI_senior_project.csv').set_index('DATE')
df_merge = pd.read_csv('../Data/Fare_senior_project.csv')

# Get the quarterly average of oil price
avg_oil = []
total_month = (2017 - 2006 + 1) * 12
for i in range(0, total_month, 3):
    avg_oil.append(df_oil_mean[i:i + 3].mean().values[0])

# Get the quarterly average of consumer price index
avg_cpi = []
for i in range(0, total_month, 3):
    avg_cpi.append(df_cpi_un[i:i + 3].mean().values[0])

df_trend = df_merge[['DATE', 'AVG_FARE']].groupby(['DATE']).mean().round(2)
df_cpi = pd.DataFrame(avg_cpi, index=df_trend.index)
df_oil = pd.DataFrame(avg_oil, index=df_trend.index)
df_cpi.columns = ['cpi']
df_oil.columns = ['oil']

# Until this step, all the pre-processing has completed. The df_merged is the final dataset used for model training.\n",
df_merged = df_trend.merge(df_oil, on=df_trend.index).merge(df_cpi, left_on='key_0', right_on=df_cpi.index)
df_merged['key_0'] = pd.to_datetime(df_merged['key_0'], format='%Y-%m-%d')
df_merged.index = df_merged['key_0']
df_merged = df_merged.drop(['key_0'], axis=1)
df_merged.index.names = ['Date']

df_merged.to_csv('../Data/Merged_senior_project.csv')

import sys
import pandas as pd
import dask.dataframe as dd
import os
import datetime

if len(sys.argv) <= 2 or len(sys.argv) > 3:
    print("To process the db1b we need to know the location.\n"
          "Directory is missing")
    sys.exit(1)

DIR_DEST = sys.argv[1]
OUT_DEST = sys.argv[2] + 'Fare_senior_project.csv'

if not os.path.isdir(DIR_DEST):
    print(f"The path {DIR_DEST} is not a directory")
    sys.exit(1)

list_of_files = os.listdir(DIR_DEST)
result_db1b_df = []
chunksize = 4 ** 11
for file_name in list_of_files:
    name, extension = os.path.splitext(file_name)
    if extension == '.csv':
        # Import the DB1B ticket data from 2006 to present
            df_chunk = dd.read_csv(DIR_DEST + file_name, dtype={'REPORTING_CARRIER': str})
            df_chunk['YEAR_QUARTER'] = df_chunk['YEAR'].astype('str') + 'Q' + df_chunk['QUARTER'].astype('str')
            df_chunk['DATETIME'] = df_chunk['YEAR_QUARTER'].map_partitions(pd.to_datetime, meta=('datetime64[ns]'))
            df_chunk = df_chunk[['ITIN_FARE', 'DATETIME', 'REPORTING_CARRIER', 'PASSENGERS']]
            df_chunk = df_chunk.dropna(how='any')
            df_chunk = df_chunk.rename(columns={'DATETIME': 'DATE'})
            # AVG_FARE column contains the itinerary fare per passenger
            df_chunk['AVG_FARE'] = df_chunk.ITIN_FARE / df_chunk.PASSENGERS
            df_chunk['DATE'] = df_chunk['DATE'].map_partitions(pd.to_datetime, meta=('datetime64[ns]')).dt.date
            result_db1b_df.append(df_chunk)

df_merge = dd.concat(result_db1b_df)
df_trend = df_merge[['DATE','AVG_FARE']].groupby(['DATE']).mean().round(2)
#df_trend = df_merge.groupby(['DATE'])['AVG_FARE'].mean().round(2)
df_trend = df_trend.compute()
df_trend = df_trend.sort_values(by='DATE')
df_trend.to_csv(OUT_DEST)

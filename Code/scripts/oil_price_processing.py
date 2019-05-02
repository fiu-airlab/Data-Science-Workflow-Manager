import pandas as pd
import os
import sys

if len(sys.argv) <= 2 or len(sys.argv) > 3:
    print("To process the Oil Price Data we need to know the location.\n"
          "Directory is missing")
    sys.exit(1)

DIR_DEST = sys.argv[1]
OUT_DEST = sys.argv[2] + 'Oil_senior_project.csv'

if not os.path.isdir(DIR_DEST):
    print(f"The path {DIR_DEST} is not a directory")
    sys.exit(1)

list_of_files = os.listdir(DIR_DEST)
result_oil_df = []
for file_name in list_of_files:
    filename, file_extension = os.path.splitext(file_name)
    if file_extension == '.csv':
        # Import the crude oil price from 2006 to present
        df_oil = pd.read_csv(DIR_DEST + file_name)
        df_oil.dropna(axis=0, inplace=True)
        df_oil = df_oil[df_oil.DCOILWTICO != '.']
        df_oil.DCOILWTICO = df_oil.DCOILWTICO.astype(float)
        df_oil.DATE = pd.to_datetime(df_oil.DATE, format='%Y-%m-%d')
        df_oil = df_oil.set_index('DATE')
        df_oil_mean = df_oil.groupby(pd.Grouper(freq="M")).mean().round(2)
        df_oil_mean.rename(columns={'DCOILWTICO': 'crude oil price'},
                           inplace=True)
        result_oil_df.append(df_oil_mean)
result = pd.concat(result_oil_df).drop_duplicates()
result.to_csv(OUT_DEST)

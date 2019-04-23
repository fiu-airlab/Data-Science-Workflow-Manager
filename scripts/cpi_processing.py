import sys
import pandas as pd
import os


if len(sys.argv) <= 2 or len(sys.argv) > 3:
    print("To process the Consumer Price Index Data we need to know the location."
          "Directory is missing")
    sys.exit(1)

DIR_DEST = sys.argv[1]
OUT_DEST = sys.argv[2] + 'CPI_senior_project.csv'

if not os.path.isdir(DIR_DEST):
    print(f"The path {DIR_DEST} is not a directory")
    sys.exit(1)

list_of_files = os.listdir(DIR_DEST)
result_cpi_df = []

for file_name in list_of_files:
    filename, file_extension = os.path.splitext(file_name)
    if file_extension == '.csv':
        # Import the crude oil price from 2006 to present
        df_cpi_un = pd.read_csv(DIR_DEST + file_name).round(2)
        df_cpi_un['DATE'] = pd.to_datetime(df_cpi_un['DATE'])
        df_cpi_un = df_cpi_un[df_cpi_un['DATE'] < '2018']
        df_cpi_un = df_cpi_un.set_index('DATE')
        df_cpi_un.rename(columns={'CPALTT01USM659N': 'cpi unadjusted'},
                         inplace=True)
        result_cpi_df.append(df_cpi_un)

result_df = pd.concat(result_cpi_df).drop_duplicates()
result_df.to_csv(OUT_DEST)

import pandas as pd
from pathlib import Path

# COMBINE ALL SOURCE CSV FILES #

# Read the 12 csv files
data1_df = pd.read_csv("data/sauce/to_share_2019-01.csv")
data2_df = pd.read_csv("data/sauce/to_share_2019-02.csv")
data3_df = pd.read_csv("data/sauce/to_share_2019-03.csv")
data4_df = pd.read_csv("data/sauce/to_share_2019-04.csv")
data5_df = pd.read_csv("data/sauce/to_share_2019-05.csv")
data6_df = pd.read_csv("data/sauce/to_share_2019-06.csv")
data7_df = pd.read_csv("data/sauce/to_share_2019-07.csv")
data8_df = pd.read_csv("data/sauce/to_share_2019-08.csv")
data9_df = pd.read_csv("data/sauce/to_share_2019-09.csv")
data10_df = pd.read_csv("data/sauce/to_share_2019-10.csv")
data11_df = pd.read_csv("data/sauce/to_share_2019-11.csv")
data12_df = pd.read_csv("data/sauce/to_share_2019-12.csv")

# Combine data
combined_data_df = pd.concat([data1_df, data2_df, data3_df, data4_df, data5_df, data6_df, data7_df, data8_df, data9_df, data10_df, data11_df, data12_df], ignore_index=True)

# Sort data by: site id, then the type of monitoring, then by time
# This step is unnecessary but makes the csv file easier to debug
combined_data_df = combined_data_df.sort_values(['site_id', 'con_type', 'utc_timestamp'])

# Save data as csv
filepath = Path('data/combined_data.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
combined_data_df.to_csv(filepath, index=False)

# Split file in half #
# Use case: Snowflake local file integration max. file size = 250 MB

import pandas as pd

# Adjust file name ---
df = pd.read_csv('SDUD-2021.csv')

# Number of splits (2) --
midpoint = len(df) // 2

first_half = df.iloc[:midpoint]
second_half = df.iloc[midpoint:]

first_half.to_csv('SDUD-2021_1.csv', index=False)
second_half.to_csv('SDUD-2021_2.csv', index=False)

print("File split into first_half.csv and second_half.csv")

##

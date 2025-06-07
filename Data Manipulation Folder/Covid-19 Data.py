import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Covid_data.csv") ##

print(df.head())
print(df.info())
print(df.describe())

#
#

num_records = df.shape[0]
years_range = df['Start Date'].min(), df['End Date'].max()
print(f"Total records: {num_records}")
print(f"Years covered: {years_range[0]} - {years_range[1]}")

#
#

usa_by_total_data = df[ (df['State'] == 'United States') &
                        (df['Group'] == 'By Total') &
                        (df['Age Group'] == 'All Ages')].shape[0]
total_deaths = df['COVID-19 Deaths'].sum()
num_mentions = df['Number of Mentions'].sum()
print(f"USA, by total, all ages records: {usa_by_total_data}")
print(f"USA, by total, all ages deaths: {total_deaths}")
print(f"USA, by total, all ages mentions: {num_mentions}")

#
# 

# plt.figure(figsize=(10, 6))
# plt.bar(x='Condition', y='COVID-19 Deaths', color = 'skyblue') # bar, scatter, plot
# plt.title('Condition by Deaths')
# plt.xlabel("Condition")
# plt.ylabel("Deaths")
# plt.show()

import pandas as pd
import sqlite3

# Load your CSV into a pandas DataFrame
df = pd.read_csv('Covid_data.csv')

# Create an in-memory SQLite database
conn = sqlite3.connect(':memory:')

# Load DataFrame into the SQLite database
df.to_sql('my_table', conn, index=False, if_exists='replace')

# Run your SQL query
query = """
SELECT 
    "Condition Group", 
    "Age Group",
    SUM("COVID-19 Deaths") AS Total_Deaths
FROM my_table
WHERE
    "State" = 'United States'
    AND "Group" = 'By Total'
    AND "Age Group" <> 'All Ages'
    AND "Age Group" <> 'Not stated'
GROUP BY "Condition Group", "Age Group"
HAVING 
    Total_Deaths <> 0
ORDER BY Total_Deaths DESC
"""

# Execute and fetch results
result_df = pd.read_sql_query(query, conn)

# Show result
print(result_df)

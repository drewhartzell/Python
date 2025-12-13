import pandas as pd
import sqlite3

df = pd.read_csv('Covid_data.csv')
conn = sqlite3.connect(':memory:')

df.to_sql('my_table', conn, index=False, if_exists='replace')

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

result_df = pd.read_sql_query(query, conn)
print(result_df)

##
##

import pandas as pd
import sqlite3

df = pd.read_csv('Etsy Items Combined.csv')
conn = sqlite3.connect(':memory:')

df.to_sql('my_table', conn, index=False, if_exists='replace')

query = """

SELECT
    SUM("Price") AS "Total_Price"
FROM my_table
"""

result_df = pd.read_sql_query(query, conn)
print(result_df)

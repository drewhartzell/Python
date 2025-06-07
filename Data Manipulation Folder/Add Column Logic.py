import pandas as pd

file_path = "drug name.xlsx"  
df = pd.read_excel(file_path)

product_use_mapping = {
    'TRULICITY': 'Diabetes',
    'EMGALITY P': 'Migraine Prevention',
    'EMGALITY S': 'Migraine Prevention',
    'EMGALITY': 'Migraine Prevention',
    'TALTZ AUTO': 'Autoimmune',
    'TALTZ': 'Autoimmune',
    'STRATTERA': 'ADHD',
    'CYMBALTA': 'Depression/Anxiety',
    'REYVOW': 'Migraine Relief',
    'ZYPREXA ZY': 'Antipsychotic',
    'EFFIENT': 'Cardiovascular',
    'VERZENIO': 'Cancer',
    'ZYPREXA': 'Antipsychotic',
    'FORTEO': 'Osteoporosis',
    'HUMALOG': 'Diabetes',
    'HUMULIN': 'Diabetes',
    'BASAGLAR': 'Diabetes',
    'JARDIANCE': 'Diabetes',
    'CIALIS': 'Erectile Dysfunction',
    'ALIMTA': 'Cancer',
    'BAQSIMI': 'Hypoglycemia',
    'OLUMIANT': 'Autoimmune',
    'TRIJARDY': 'Diabetes',
    'OMVOQ': 'Autoimmune',
    'REZUROCK': 'Autoimmune',
    'SYMBYAX': 'Bipolar Depression',
    'ZELAPAR': 'Parkinson’s Disease',
    'EVISTA': 'Osteoporosis',
    'DULERA': 'Asthma/COPD',
    'AXIRON': 'Testosterone Replacement',
    'ADUHELM': 'Alzheimer’s Disease',
    'STRATTERA,': 'ADHD'
}

df['Clean Product Name'] = df['Product Name'].str.strip().str.upper().str.replace(',', '')
df['Product Type Use'] = df['Clean Product Name'].map(product_use_mapping).fillna('Other')

df.drop(columns=['Clean Product Name'], inplace=True)

output_path = "updated_drug_use_classification.xlsx"
df.to_excel(output_path, index=False)

print(f"Updated file saved as: {output_path}")

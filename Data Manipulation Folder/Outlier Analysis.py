# Outlier Detection Using Z-score #

import pandas as pd
from scipy.stats import zscore

# Calculate Z-scores --
dataset['Z_Score'] = zscore(dataset['Sales'])

# Flag outliers --
dataset['Is_Outlier'] = abs(dataset['Z_Score']) > 3

# Filter outliers --
outliers = dataset[dataset['Is_Outlier']]

outliers

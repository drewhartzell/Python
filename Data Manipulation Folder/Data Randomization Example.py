import pandas as pd
import numpy as np

np.random.seed(42)  # for reproducibility

# Configuration
plants = ['P001', 'P002', 'P003']
materials = ['MAT1001', 'MAT1002', 'MAT1003']
num_rows = 200

# Generate random creation dates over ~2 years
date_range = pd.date_range(start='2023-01-01', end='2025-04-30', freq='D')
creation_dates = np.random.choice(date_range, num_rows)

# Simulate plant and material
plant_choices = np.random.choice(plants, num_rows)
material_choices = np.random.choice(materials, num_rows)

# Simulate lead times in days (normal distribution)
# P001: faster, P003: slower
lead_time_means = {'P001': 10, 'P002': 14, 'P003': 18}
lead_times = [
    int(np.clip(np.random.normal(loc=lead_time_means[p], scale=2.5), 5, 30))
    for p in plant_choices
]

# Create the DataFrame
dataset = pd.DataFrame({
    'Plant': plant_choices,
    'Material': material_choices,
    'Creation Date': pd.to_datetime(creation_dates),
    'Leadtime': lead_times
})

# Sort by date for visual consistency
dataset = dataset.sort_values(by='Creation Date').reset_index(drop=True)

# Display a preview
print(dataset.head())

# Save as CSV (optional)
# dataset.to_csv("simulated_leadtime_data.csv", index=False)

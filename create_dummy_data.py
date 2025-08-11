import pandas as pd
import numpy as np
import os

# Define features (columns)
columns = [
    'living_area_sqft', 'lot_size_sqft', 'bedrooms', 'bathrooms', 'age',
    'last_price_per_sqft', 'assessed_value', 'tax_delinquent_flag',
    'code_violations_count', 'pt_MultiFamily', 'pt_SingleFamily', 'pt_VacantLand'
]

# Create train data (100 rows)
train_data = pd.DataFrame({
    'living_area_sqft': np.random.randint(500, 3500, 100),
    'lot_size_sqft': np.random.randint(1000, 10000, 100),
    'bedrooms': np.random.randint(1, 6, 100),
    'bathrooms': np.random.randint(1, 4, 100),
    'age': np.random.randint(0, 100, 100),
    'last_price_per_sqft': np.random.randint(100, 300, 100),
    'assessed_value': np.random.randint(50000, 500000, 100),
    'tax_delinquent_flag': np.random.randint(0, 2, 100),
    'code_violations_count': np.random.randint(0, 5, 100),
    'pt_MultiFamily': np.random.randint(0, 2, 100),
    'pt_SingleFamily': np.random.randint(0, 2, 100),
    'pt_VacantLand': np.random.randint(0, 2, 100),
})

# Calculate price (target)
train_data['price'] = train_data['living_area_sqft'] * train_data['last_price_per_sqft'] * 1.1

# Create test data (10 rows)
test_data = pd.DataFrame({
    'living_area_sqft': np.random.randint(500, 3500, 10),
    'lot_size_sqft': np.random.randint(1000, 10000, 10),
    'bedrooms': np.random.randint(1, 6, 10),
    'bathrooms': np.random.randint(1, 4, 10),
    'age': np.random.randint(0, 100, 10),
    'last_price_per_sqft': np.random.randint(100, 300, 10),
    'assessed_value': np.random.randint(50000, 500000, 10),
    'tax_delinquent_flag': np.random.randint(0, 2, 10),
    'code_violations_count': np.random.randint(0, 5, 10),
    'pt_MultiFamily': np.random.randint(0, 2, 10),
    'pt_SingleFamily': np.random.randint(0, 2, 10),
    'pt_VacantLand': np.random.randint(0, 2, 10),
})

# Create data directory if it doesn't exist
os.makedirs('./data', exist_ok=True)

# Save CSV files
train_data.to_csv('./data/train_data.csv', index=False)
test_data.to_csv('./data/test_data.csv', index=False)

print("Dummy train and test data created.")


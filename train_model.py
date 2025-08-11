import pandas as pd
import lightgbm as lgb
import pickle
import os

# Load train data
train_data = pd.read_csv('./data/train_data.csv')

# Features and target
feature_names = [
    'living_area_sqft', 'lot_size_sqft', 'bedrooms', 'bathrooms', 'age',
    'last_price_per_sqft', 'assessed_value', 'tax_delinquent_flag',
    'code_violations_count', 'pt_MultiFamily', 'pt_SingleFamily', 'pt_VacantLand'
]

X_train = train_data[feature_names]
y_train = train_data['price']

# Prepare dataset for LightGBM
lgb_train = lgb.Dataset(X_train, label=y_train)

# Parameters for LightGBM
params = {
    'objective': 'regression',
    'metric': 'rmse',
    'verbose': -1
}

# Train the model
model = lgb.train(params, lgb_train, num_boost_round=100)

# Save model and features
os.makedirs('./outputs', exist_ok=True)
with open('./outputs/valuation_model.pkl', 'wb') as f:
    pickle.dump((model, feature_names), f)

print("Model trained and saved.")


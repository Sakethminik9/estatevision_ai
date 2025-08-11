import pickle
import pandas as pd

# Load the model and feature list
model_path = '/Users/sakethtalamarla/Downloads/realestate-ai-mvp/outputs/valuation_model.pkl'
with open(model_path, 'rb') as f:
    model, feature_names = pickle.load(f)

# Load test data
test_data_path = '/Users/sakethtalamarla/Downloads/realestate-ai-mvp/data/test_data.csv'
test_data = pd.read_csv(test_data_path)

# Select only the features model expects
X_test = test_data[feature_names]

# Predict prices
predictions = model.predict(X_test)

# Add predictions to dataframe
test_data['predicted_price'] = predictions

# Save to CSV
output_path = '/Users/sakethtalamarla/Downloads/realestate-ai-mvp/outputs/predicted_prices.csv'
test_data.to_csv(output_path, index=False)

print("Predictions done and saved.")


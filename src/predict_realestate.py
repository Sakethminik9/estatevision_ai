import pickle
import pandas as pd

def main():
    # Load the updated model
    model_path = '/Users/sakethtalamarla/Downloads/realestate-ai-mvp/outputs/valuation_model_updated.pkl'
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Load your test data that also includes underwriting metrics
    test_data_path = '/Users/sakethtalamarla/Downloads/realestate-ai-mvp/data/test_data_with_metrics.csv'  # Replace with your test CSV path
    test_data = pd.read_csv(test_data_path)

    # Feature columns must match what model expects
    feature_cols = [
        'living_area_sqft', 'lot_size_sqft', 'bedrooms', 'bathrooms', 'age',
        'last_price_per_sqft', 'assessed_value', 'tax_delinquent_flag',
        'code_violations_count', 'pt_MultiFamily', 'pt_SingleFamily', 'pt_VacantLand',
        'NOI', 'Cap_Rate', 'Cash_on_Cash_Return', 'RRR'
    ]

    X_test = test_data[feature_cols]

    # Predict
    predictions = model.predict(X_test)

    # Save predictions
    test_data['predicted_price'] = predictions
    output_path = '/Users/sakethtalamarla/Downloads/realestate-ai-mvp/outputs/predicted_prices.csv'
    test_data.to_csv(output_path, index=False)

    print("Predictions done and saved to", output_path)

if __name__ == "__main__":
    main()

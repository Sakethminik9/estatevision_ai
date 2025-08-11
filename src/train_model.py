import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import pickle

def main():
    df = pd.read_csv('/Users/sakethtalamarla/Downloads/realestate-ai-mvp/data/property_with_metrics.csv')

    # Feature columns (add your original + underwriting metrics)
    feature_cols = [
        'living_area_sqft', 'lot_size_sqft', 'bedrooms', 'bathrooms', 'age',
        'last_price_per_sqft', 'assessed_value', 'tax_delinquent_flag',
        'code_violations_count', 'pt_MultiFamily', 'pt_SingleFamily', 'pt_VacantLand',
        'NOI', 'Cap_Rate', 'Cash_on_Cash_Return', 'RRR'
    ]

    # Make sure all features exist in the data
    missing_cols = [col for col in feature_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing feature columns in data: {missing_cols}")

    X = df[feature_cols]
    y = df['price']  # Change if your target column name is different

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val)

    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'verbosity': -1
    }

    model = lgb.train(params, train_data, valid_sets=[val_data], early_stopping_rounds=50)

    with open('/Users/sakethtalamarla/Downloads/realestate-ai-mvp/outputs/valuation_model_updated.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("Model trained and saved successfully!")

if __name__ == "__main__":
    main()

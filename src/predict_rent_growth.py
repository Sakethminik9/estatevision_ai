import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def main():
    # Example synthetic data - replace with your real datasets
    data = {
        'year': [2018, 2019, 2020, 2021, 2022],
        'avg_rent': [1200, 1250, 1300, 1350, 1400],
        'migration_index': [1.0, 1.05, 1.10, 1.15, 1.20]  # hypothetical migration trend
    }

    df = pd.DataFrame(data)

    # Target variable: rent growth (next year rent - current year rent) / current year rent
    df['rent_growth'] = df['avg_rent'].pct_change().shift(-1)
    df = df.dropna()

    # Features: avg_rent and migration_index (lagged to current year)
    X = df[['avg_rent', 'migration_index']]
    y = df['rent_growth']

    model = LinearRegression()
    model.fit(X, y)

    # Predict next year's rent growth with latest data
    latest_data = np.array([[df['avg_rent'].iloc[-1], df['migration_index'].iloc[-1]]])
    predicted_growth = model.predict(latest_data)[0]

    print(f"Predicted rent growth for next year: {predicted_growth:.2%}")

if __name__ == "__main__":
    main()

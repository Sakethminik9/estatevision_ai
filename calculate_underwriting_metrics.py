import pandas as pd

def calculate_noi(gross_rental_income, operating_expenses):
    return gross_rental_income - operating_expenses

def calculate_cap_rate(noi, property_value):
    return noi / property_value if property_value else None

def calculate_cash_on_cash_return(cash_flow, cash_invested):
    return cash_flow / cash_invested if cash_invested else None

def calculate_required_rate_of_return(risk_free_rate, risk_premium):
    return risk_free_rate + risk_premium

def main(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    # Check required columns exist
    required_cols = ['gross_rent', 'operating_expenses', 'property_price', 'cash_invested']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column in input CSV: {col}")

    # Calculate metrics
    df['NOI'] = df.apply(lambda row: calculate_noi(row['gross_rent'], row['operating_expenses']), axis=1)
    df['Cap_Rate'] = df.apply(lambda row: calculate_cap_rate(row['NOI'], row['property_price']), axis=1)
    df['Cash_on_Cash_Return'] = df.apply(lambda row: calculate_cash_on_cash_return(row['NOI'], row['cash_invested']), axis=1)

    # Risk-free rate and risk premium example values (you can change)
    risk_free_rate = 0.03
    risk_premium = 0.05
    df['RRR'] = calculate_required_rate_of_return(risk_free_rate, risk_premium)

    df.to_csv(output_csv, index=False)
    print(f"Underwriting metrics saved to {output_csv}")

if __name__ == "__main__":
    input_csv = '/Users/sakethtalamarla/Downloads/realestate-ai-mvp/data/property_data.csv'  # Your input CSV path
    output_csv = '/Users/sakethtalamarla/Downloads/realestate-ai-mvp/data/property_with_metrics.csv'
    main(input_csv, output_csv)

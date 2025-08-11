import streamlit as st
import pandas as pd

# Load the predictions CSV with underwriting metrics + predicted price
DATA_PATH = './data/property_with_metrics.csv'

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

def main():
    st.title("Real Estate Investment Dashboard")

    df = load_data()

    st.subheader("Property Data with Underwriting Metrics and Predictions")
    st.dataframe(df)

    # Filter by Cap Rate
    min_cap_rate = st.slider("Minimum Cap Rate", float(df['Cap_Rate'].min()), float(df['Cap_Rate'].max()), float(df['Cap_Rate'].min()))
    filtered_df = df[df['Cap_Rate'] >= min_cap_rate]

    st.subheader(f"Properties with Cap Rate >= {min_cap_rate:.2f}")
    st.dataframe(filtered_df)

    # Sort by predicted price
    if st.checkbox("Sort by Predicted Price"):
        filtered_df = filtered_df.sort_values('predicted_price', ascending=False)
        st.dataframe(filtered_df)

if __name__ == "__main__":
    main()

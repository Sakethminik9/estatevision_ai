import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your predicted rent growth CSV or DataFrame (replace with your actual file path)
df = pd.read_csv('predicted_rent_growth.csv')  # Make sure this file exists

st.title("Rent Growth Predictions Dashboard")

# Show raw data
st.subheader("Raw Prediction Data")
st.dataframe(df)

# Simple line chart visualization
st.subheader("Rent Growth Over Time")
if 'year' in df.columns and 'predicted_rent_growth' in df.columns:
    fig, ax = plt.subplots()
    ax.plot(df['year'], df['predicted_rent_growth'], marker='o')
    ax.set_xlabel("Year")
    ax.set_ylabel("Predicted Rent Growth (%)")
    ax.set_title("Predicted Rent Growth Over Years")
    st.pyplot(fig)
else:
    st.write("Expected columns 'year' and 'predicted_rent_growth' not found in data.")

# You can add more charts or KPIs here as needed


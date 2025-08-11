import streamlit as st
import pandas as pd

# Title
st.title("Real Estate Price Predictions")

# Load predicted data
data_path = './outputs/predicted_prices.csv'
data = pd.read_csv(data_path)

# Show data table
st.write("### Predicted Property Prices")
st.dataframe(data)

# Add simple filters - example: filter by bedrooms
bedrooms = st.slider('Filter by number of bedrooms', min_value=int(data['bedrooms'].min()), max_value=int(data['bedrooms'].max()), value=(int(data['bedrooms'].min()), int(data['bedrooms'].max())))
filtered_data = data[(data['bedrooms'] >= bedrooms[0]) & (data['bedrooms'] <= bedrooms[1])]

st.write(f"Showing properties with bedrooms between {bedrooms[0]} and {bedrooms[1]}")
st.dataframe(filtered_data)

# Show summary stats
st.write("### Summary Statistics")
st.write(filtered_data.describe())


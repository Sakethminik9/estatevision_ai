# src/data_prep.py
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

url = "https://zillow-com4.p.rapidapi.com/properties/search-coordinates"
querystring = {
    "location":"Houston, TX",
    "eastLng":"-94.5172805",
    "westLng":"-96.1932336",
    "southLat":"29.170258",
    "northLat":"29.657254",
    "status":"forSale",
    "sort":"relevance"
}

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "zillow-com4.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
print(response.json())

import pandas as pd
import numpy as np
from pathlib import Path
import joblib

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)

def load_data(path=DATA_DIR / "sample_properties.csv"):
    df = pd.read_csv(path, parse_dates=["last_sale_date"], keep_default_na=True)
    return df

def engineer_features(df):
    # basic numeric features for valuation
    df2 = df.copy()
    # fill missing numeric with zeros (for vacant land etc.)
    for c in ["living_area_sqft","lot_size_sqft","bedrooms","bathrooms","year_built","assessed_value","est_mortgage_balance"]:
        if c in df2.columns:
            df2[c] = pd.to_numeric(df2[c], errors="coerce").fillna(0)
    # age
    df2["age"] = np.where(df2["year_built"]>0, 2025 - df2["year_built"], 0)
    # price per sqft (last sale)
    df2["last_price_per_sqft"] = np.where(df2["living_area_sqft"]>0, df2["last_sale_price"]/df2["living_area_sqft"], 0)
    # flags
    df2["tax_delinquent_flag"] = df2["tax_delinquent"].fillna(0).astype(int)
    df2["code_violations_count"] = df2["code_violations_count"].fillna(0).astype(int)
    # simple encoding for property type
    df2 = pd.get_dummies(df2, columns=["property_type"], prefix="pt", dummy_na=False)
    return df2

def save_features(df, out=OUT_DIR/"features.parquet"):
    df.to_parquet(out, index=False)
    print(f"Saved features to {out}")

if __name__ == "__main__":
    df = load_data()
    df2 = engineer_features(df)
    save_features(df2)

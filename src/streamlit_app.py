# src/streamlit_app.py
import streamlit as st
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "outputs"
RANKED_PATH = OUT_DIR / "ranked_deals.csv"

st.set_page_config(page_title="RealEstate AI - Ranked Deals", layout="wide")

st.title("RealEstate AI — Ranked Deals (MVP)")

if not RANKED_PATH.exists():
    st.error("No ranked_deals.csv found. Run the pipeline first (data_prep -> train_valuation -> scoring).")
else:
    df = pd.read_csv(RANKED_PATH)
    # show top N
    n = st.sidebar.slider("Top N", min_value=1, max_value=min(50, len(df)), value=10)
    st.subheader(f"Top {n} Deals")
    st.dataframe(df.head(n))

    sel = st.selectbox("Select property id to view details", df["property_id"].tolist())
    row = df[df["property_id"]==sel].iloc[0]
    st.markdown("### Property Summary")
    st.write({
        "Address": row["address"],
        "Listing Price": f"${row['current_listing_price']:,.0f}",
        "FMV Estimate": f"${row['fmv_est']:,.0f}",
        "Undervalue %": f"{row['undervalue_pct']:.1f}%",
        "Pred IRR (5y)": row["pred_IRR_5y"],
        "Cap Rate": f"{row['cap_rate']:.3f}",
        "Annual Cashflow": f"${row['annual_cashflow']:,.0f}",
        "Cash-on-Cash": f"{row['cash_on_cash']:.3f}",
        "Distress Prob": row["distress_prob"],
        "Zoning Upside": row["zoning_upside_idx"],
        "Final Score": row["final_score"]
    })

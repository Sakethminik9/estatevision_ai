# src/scoring.py
import pandas as pd
from pathlib import Path
import joblib
from src.underwriting import compute_noi, cap_rate, annual_debt_service, cash_on_cash, compute_irr

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "outputs"
FEATURES_PATH = OUT_DIR / "features.parquet"
MODEL_PATH = OUT_DIR / "valuation_model.pkl"
RANKED_PATH = OUT_DIR / "ranked_deals.csv"

def load_model():
    model, feature_cols = joblib.load(MODEL_PATH)
    return model, feature_cols

def run_scoring():
    df = pd.read_parquet(FEATURES_PATH)
    model, feature_cols = load_model()
    X = df[feature_cols].astype(float)
    fmv_pred = model.predict(X)
    df["fmv_est"] = fmv_pred
    df["undervalue_pct"] = (df["fmv_est"] - df["current_listing_price"]) / df["fmv_est"] * 100

    # Underwriting assumptions (simple)
    df["monthly_rent_est"] = df["living_area_sqft"].apply(lambda s: 1.8*s if s>0 else 0)  # $/sqft baseline 1.8
    df["gross_annual_rent"] = df["monthly_rent_est"] * 12
    vacancy_rate = 0.06
    op_exp_pct = 0.35
    df["NOI"] = df["gross_annual_rent"].apply(lambda g: compute_noi(g, vacancy_rate, op_exp_pct))
    df["cap_rate"] = df.apply(lambda r: cap_rate(r["NOI"], r["current_listing_price"]), axis=1)

    # financing & cashflow
    ltv = 0.7
    interest = 0.05
    term = 30
    df["loan_amount"] = df["current_listing_price"] * ltv
    df["equity"] = df["current_listing_price"] * (1 - ltv)
    df["annual_debt_service"] = df["loan_amount"].apply(lambda L: annual_debt_service(L, interest, term))
    df["annual_cashflow"] = df["NOI"] - df["annual_debt_service"]
    df["cash_on_cash"] = df.apply(lambda r: cash_on_cash(r["annual_cashflow"], r["equity"]), axis=1)

    # Sample IRR over 5 years with simple appreciation
    holding = 5
    appreciation = 0.02
    sale_price = df["current_listing_price"] * ((1 + appreciation) ** holding)
    # assume remaining loan balance roughly amortized — for demo, ignore remaining loan calc and use loan_amount
    sale_proceeds = sale_price - df["loan_amount"]  # crude
    irr_list = []
    for idx, row in df.iterrows():
        annual_cf = [row["annual_cashflow"]] * holding
        try:
            irr_value = compute_irr(-row["equity"], annual_cf, sale_proceeds.loc[idx])
        except Exception:
            irr_value = None
        irr_list.append(irr_value)
    df["pred_IRR_5y"] = irr_list

    # Distress score: simple heuristic combining tax delinq and code violations
    df["distress_prob"] = (0.6 * df["tax_delinquent_flag"] + 0.4 * (df["code_violations_count"]>0).astype(int))

    # Zoning upside stub (0-1)
    df["zoning_upside_idx"] = 0.1  # placeholder

    # Final score (simple normalization)
    # for simplicity, use rank on pred_IRR_5y (higher better) and undervalue (higher better)
    df["irr_rank"] = df["pred_IRR_5y"].rank(ascending=False, method="min").fillna(df.shape[0]+1)
    df["undervalue_rank"] = df["undervalue_pct"].rank(ascending=False, method="min").fillna(df.shape[0]+1)
    df["final_score"] = (df["irr_rank"].max() - df["irr_rank"]) * 0.6 + (df["undervalue_rank"].max() - df["undervalue_rank"]) * 0.4

    out_cols = ["property_id","address","current_listing_price","fmv_est","undervalue_pct","pred_IRR_5y","cap_rate","annual_cashflow","cash_on_cash","distress_prob","zoning_upside_idx","final_score"]
    df[out_cols].to_csv(RANKED_PATH, index=False)
    print(f"Saved ranked deals to {RANKED_PATH}")

if __name__ == "__main__":
    run_scoring()

# src/underwriting.py
import numpy as np
import pandas as pd
from numpy_financial import irr

def compute_noi(gross_annual_rent, vacancy_rate, operating_expense_pct):
    vacancy_loss = gross_annual_rent * vacancy_rate
    operating_expenses = gross_annual_rent * operating_expense_pct
    return gross_annual_rent - vacancy_loss - operating_expenses

def cap_rate(noi, purchase_price):
    return noi / purchase_price if purchase_price else 0.0

def annual_debt_service(loan_amount, annual_interest_rate=0.05, term_years=30):
    r = annual_interest_rate / 12
    n = term_years * 12
    monthly = (loan_amount * r) / (1 - (1 + r) ** (-n))
    return monthly * 12

def cash_on_cash(annual_cash_flow, initial_equity):
    return annual_cash_flow / initial_equity if initial_equity else 0.0

def compute_irr(cash_outflow_equity, annual_cashflows, sale_proceeds):
    # cash_outflow_equity: negative number (initial)
    # annual_cashflows: list of annual cashflow for years 1..N (pre-tax)
    # sale_proceeds: net proceeds at end of final year (after paying remaining loan)
    cf = [cash_outflow_equity] + annual_cashflows[:-1] + [annual_cashflows[-1] + sale_proceeds]
    try:
        r = irr(cf)
    except Exception:
        r = np.nan
    return r

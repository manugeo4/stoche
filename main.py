#!/usr/bin/env python3
import argparse
import yfinance as yf
from tabulate import tabulate

# --- Checklist scoring logic ---
def assess_company(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    metrics = {}
    scores = {}
    
    # --- Profitability ---
    metrics['ROE'] = info.get("returnOnEquity", None)
    metrics['ROCE'] = info.get("returnOnCapitalEmployed", None)  # sometimes not available
    metrics['Net Margin'] = info.get("profitMargins", None)
    
    scores['ROE'] = 1 if metrics['ROE'] and metrics['ROE'] > 0.12 else 0
    scores['ROCE'] = 1 if metrics['ROCE'] and metrics['ROCE'] > 0.15 else 0
    scores['Net Margin'] = 1 if metrics['Net Margin'] and metrics['Net Margin'] > 0.1 else 0
    
    # --- Growth ---
    metrics['Revenue Growth'] = info.get("revenueGrowth", None)
    metrics['Earnings Growth'] = info.get("earningsGrowth", None)
    
    scores['Revenue Growth'] = 1 if metrics['Revenue Growth'] and metrics['Revenue Growth'] > 0.05 else 0
    scores['Earnings Growth'] = 1 if metrics['Earnings Growth'] and metrics['Earnings Growth'] > 0.05 else 0
    
    # --- Safety ---
    metrics['Debt/Equity'] = info.get("debtToEquity", None)
    scores['Debt/Equity'] = 1 if metrics['Debt/Equity'] and metrics['Debt/Equity'] < 100 else 0
    
    # --- Cash ---
    metrics['Free Cash Flow'] = info.get("freeCashflow", None)
    scores['Free Cash Flow'] = 1 if metrics['Free Cash Flow'] and metrics['Free Cash Flow'] > 0 else 0
    
    # --- Valuation ---
    metrics['P/E'] = info.get("forwardPE", None)
    scores['P/E'] = 1 if metrics['P/E'] and metrics['P/E'] < 25 else 0
    
    # --- Total Score ---
    total_score = sum(scores.values())
    
    # Build table
    table = []
    for key in metrics:
        value = metrics[key]
        score = scores.get(key, "-")
        if isinstance(value, float):
            value = round(value, 3)
        table.append([key, value, score])
    
    print(f"\n📊 Assessment for {ticker}")
    print(tabulate(table, headers=["Metric", "Value", "Score"], tablefmt="pretty"))
    print(f"\n✅ Total Score: {total_score} / {len(scores)}\n")

# --- CLI Interface ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Company Health Assessment Tool")
    parser.add_argument("ticker", help="Company ticker symbol (e.g., AAPL, INFY.NS)")
    args = parser.parse_args()
    
    assess_company(args.ticker)


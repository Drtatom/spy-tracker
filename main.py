import yfinance as yf
import pandas as pd
import json
from datetime import datetime

def get_spy_data():
    ticker = "SPY"
    data = yf.Ticker(ticker)
    hist = data.history(period="1mo")
    
    current_price = hist['Close'].iloc[-1]
    moving_avg = hist['Close'].mean()
    
    report = {
        "ticker": ticker,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "price": round(float(current_price), 2),
        "moving_avg_30d": round(float(moving_avg), 2),
        "status": "bullish" if current_price > moving_avg else "bearish"
    }
    return report

if __name__ == "__main__":
    report = get_spy_data()
    print(json.dumps(report, indent=4))
    with open("spy_report.json", "w") as f:
        json.dump(report, f)

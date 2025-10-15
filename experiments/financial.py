"""
Financial cross-domain demo for UTL.
- If yfinance is available, fetches SPY/TSLA/BTC.
- Otherwise, expects CSVs in data/ with columns: Date, Open, High, Low, Close, Volume
"""
import sys, os
from pathlib import Path
import math
import numpy as np
import pandas as pd

try:
    import yfinance as yf
    HAS_YF = True
except Exception:
    HAS_YF = False

from utl.detector import UTLDetector

DATA_DIR = Path("data")

def load_asset(symbol: str) -> pd.DataFrame:
    if HAS_YF:
        df = yf.download(symbol, period="5y", interval="1d", progress=False)
        df = df.rename(columns=str.title).reset_index()
        return df
    # fallback to CSV
    csv_path = DATA_DIR / f"{symbol}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Install yfinance or provide {csv_path}")
    return pd.read_csv(csv_path)

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # Simple technicals: log return, rolling std, ROC
    df = df.copy()
    df["LogRet"] = np.log(df["Close"]).diff()
    df["Vol5"] = df["LogRet"].rolling(5).std()
    df["Vol20"] = df["LogRet"].rolling(20).std()
    df["ROC10"] = df["Close"].pct_change(10)
    df["RSI14"] = _rsi(df["Close"], 14)
    df = df.dropna().reset_index(drop=True)
    return df

def _rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0.0)
    down = -1*delta.clip(upper=0.0)
    roll_up = up.rolling(window).mean()
    roll_down = down.rolling(window).mean()
    rs = roll_up / (roll_down + 1e-9)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi

def run(symbol: str = "SPY"):
    print(f"=== UTL Financial Demo: {symbol} ===\n")
    df = load_asset(symbol)
    df = compute_indicators(df)

    det = UTLDetector(alpha=0.15, theta_mult=1.5, gamma=1.5, beta=0.8, tau=0.68)

    # Iterate rows as "turns"
    hazards = []
    for _, row in df.iterrows():
        # crude mapping of indicators into feature channels
        linguistic = float(np.clip(abs(row["ROC10"] or 0.0) * 10.0, 0.0, 1.0))  # "volatility-like"
        behavioral = float(np.clip((row["Vol5"] or 0.0) * 50.0, 0.0, 1.0))
        temporal = float(np.clip((row["Vol20"] or 0.0) * 50.0, 0.0, 1.0))
        resilience = float(np.clip(1.0 - (row["RSI14"] or 50.0)/100.0, 0.0, 1.0))  # overbought -> less resilience

        h, crisis = det.update({
            "linguistic": linguistic,
            "behavioral": behavioral,
            "temporal": temporal,
            "resilience": resilience
        })
        hazards.append(h)

    print(f"Turns processed: {len(hazards)}")
    print(f"Mean hazard: {np.mean(hazards):.3f} | Max hazard: {np.max(hazards):.3f}")
    # Simple crash signal: hazard > 0.7
    crash_days = int(np.sum(np.array(hazards) > 0.7))
    print(f"Days flagged as high-risk: {crash_days}")

if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "SPY"
    run(symbol)

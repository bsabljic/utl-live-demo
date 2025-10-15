"""
Figures for paper-style export (from synthetic results).
Saves names that are convenient to reference in the manuscript.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

RES = Path("results/crisis_turns.csv")
FIG = Path("figures"); FIG.mkdir(parents=True, exist_ok=True)

def figure_6_hazard_hist():
    df = pd.read_csv(RES)
    plt.figure()
    df["hazard"].hist(bins=30)
    plt.title("Hazard Distribution (Per-Turn)")
    plt.xlabel("Hazard")
    plt.ylabel("Frequency")
    plt.tight_layout()
    p = FIG / "figure_6_hazard_hist.png"
    plt.savefig(p, dpi=180)
    plt.close()
    print("Saved:", p)

def figure_12_conv_curve(conv_id:int = 0):
    df = pd.read_csv(RES)
    g = df[df["conversation_id"]==conv_id].sort_values("turn")
    if g.empty and len(df):
        conv_id = int(df["conversation_id"].iloc[0])
        g = df[df["conversation_id"]==conv_id].sort_values("turn")
    plt.figure()
    plt.plot(g["turn"].values, g["hazard"].values, marker="o")
    plt.axhline(0.68, linestyle="--")
    plt.title(f"Hazard over Turns (Conversation {int(g['conversation_id'].iloc[0])})")
    plt.xlabel("Turn")
    plt.ylabel("Hazard")
    plt.tight_layout()
    p = FIG / "figure_12_conv_curve.png"
    plt.savefig(p, dpi=180)
    plt.close()
    print("Saved:", p)

if __name__ == "__main__":
    if not RES.exists():
        print("Missing results/crisis_turns.csv; run experiments/crisis_chat.py first.")
    else:
        figure_6_hazard_hist()
        figure_12_conv_curve()

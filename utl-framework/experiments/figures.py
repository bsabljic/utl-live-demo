"""
Generate basic figures from synthetic demo using matplotlib.
Saves into figures/ directory.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FIG_DIR = Path("figures")
RES_PATH = Path("results/crisis_turns.csv")
FIG_DIR.mkdir(parents=True, exist_ok=True)

def fig_hazard_hist():
    df = pd.read_csv(RES_PATH)
    plt.figure()
    df["hazard"].hist(bins=30)
    plt.title("Hazard Distribution (Per-Turn)")
    plt.xlabel("Hazard")
    plt.ylabel("Frequency")
    plt.tight_layout()
    p = FIG_DIR / "fig_hazard_hist.png"
    plt.savefig(p, dpi=180)
    plt.close()
    print("Saved:", p)

def fig_sample_conversation(conv_id: int = 0):
    df = pd.read_csv(RES_PATH)
    g = df[df["conversation_id"]==conv_id].sort_values("turn")
    if g.empty:
        conv_id = int(df["conversation_id"].iloc[0])
        g = df[df["conversation_id"]==conv_id].sort_values("turn")
    plt.figure()
    plt.plot(g["turn"].values, g["hazard"].values, marker="o")
    plt.axhline(0.68, linestyle="--")
    plt.title(f"Hazard over Turns (Conversation {int(g['conversation_id'].iloc[0])})")
    plt.xlabel("Turn")
    plt.ylabel("Hazard")
    plt.tight_layout()
    p = FIG_DIR / "fig_conversation_curve.png"
    plt.savefig(p, dpi=180)
    plt.close()
    print("Saved:", p)

def fig_threshold_sweep():
    df = pd.read_csv(RES_PATH)
    thr_grid = np.linspace(0.1, 0.9, 17)
    precisions, recalls = [], []
    y_true = df["crisis_label"].values.astype(int)
    scores = df["hazard"].values
    for thr in thr_grid:
        y_pred = (scores > thr).astype(int)
        tp = ((y_pred==1) & (y_true==1)).sum()
        fp = ((y_pred==1) & (y_true==0)).sum()
        fn = ((y_pred==0) & (y_true==1)).sum()
        prec = tp / (tp+fp) if (tp+fp)>0 else 0.0
        rec = tp / (tp+fn) if (tp+fn)>0 else 0.0
        precisions.append(prec)
        recalls.append(rec)

    plt.figure()
    plt.plot(thr_grid, precisions, marker="o", label="Precision")
    plt.plot(thr_grid, recalls, marker="s", label="Recall")
    plt.title("Precision/Recall vs Threshold")
    plt.xlabel("Threshold")
    plt.ylabel("Score")
    plt.legend()
    plt.tight_layout()
    p = FIG_DIR / "fig_threshold_sweep.png"
    plt.savefig(p, dpi=180)
    plt.close()
    print("Saved:", p)

if __name__ == "__main__":
    if not RES_PATH.exists():
        print("Missing results/crisis_turns.csv. Run: python experiments/crisis_chat.py")
    else:
        fig_hazard_hist()
        fig_sample_conversation()
        fig_threshold_sweep()

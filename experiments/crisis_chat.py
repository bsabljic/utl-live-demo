"""
Crisis Chat reproducibility demo (uses synthetic demo CSV).
- Loads data/demo_synthetic.csv
- Runs UTLDetector per conversation
- Computes simple metrics vs. crisis_label using threshold on hazard
Outputs:
- results/crisis_turns.csv (turn-level hazards)
- results/summary.txt (metrics)
"""
from pathlib import Path
import numpy as np
import pandas as pd
from utl.detector import UTLDetector

DATA = Path("data/demo_synthetic.csv")
OUT_DIR = Path("results")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def evaluate_threshold(y_true, y_score, thr=0.68):
    y_pred = (y_score > thr).astype(int)
    tp = int(((y_pred==1) & (y_true==1)).sum())
    fp = int(((y_pred==1) & (y_true==0)).sum())
    tn = int(((y_pred==0) & (y_true==0)).sum())
    fn = int(((y_pred==0) & (y_true==1)).sum())
    prec = tp / (tp+fp) if (tp+fp)>0 else 0.0
    rec = tp / (tp+fn) if (tp+fn)>0 else 0.0
    acc = (tp+tn) / max(1, len(y_true))
    return dict(tp=tp, fp=fp, tn=tn, fn=fn, precision=prec, recall=rec, accuracy=acc)

def main():
    assert DATA.exists(), f"Missing {DATA}"
    df = pd.read_csv(DATA)
    df = df.sort_values(["conversation_id","turn"]).reset_index(drop=True)

    rows = []
    for conv_id, g in df.groupby("conversation_id"):
        det = UTLDetector()
        for _, row in g.iterrows():
            features = {
                "linguistic": float(row["linguistic_hazard"]),
                "behavioral": float(row["behavioral_hazard"]),
                "temporal": float(row["temporal_hazard"]),
                "resilience": float(row["resilience_score"]),
            }
            hazard, crisis = det.update(features)
            rows.append({
                "conversation_id": int(conv_id),
                "turn": int(row["turn"]),
                "hazard": hazard,
                "crisis_label": int(row["crisis_label"]),
            })

    res = pd.DataFrame(rows)
    res.to_csv(OUT_DIR / "crisis_turns.csv", index=False)

    # Evaluate per-turn
    metrics = evaluate_threshold(res["crisis_label"].values, res["hazard"].values, thr=0.68)

    # Simple per-conversation flag (max hazard)
    agg = res.groupby("conversation_id").agg(
        max_hazard=("hazard","max"),
        any_label=("crisis_label","max"),
    ).reset_index()
    m_conv = evaluate_threshold(agg["any_label"].values, agg["max_hazard"].values, thr=0.68)

    with open(OUT_DIR / "summary.txt", "w", encoding="utf-8") as f:
        f.write("=== UTL Crisis Chat Demo ===\n\n")
        f.write(f"Turns: {len(res)} | Conversations: {res['conversation_id'].nunique()}\n\n")
        f.write("[Per-Turn] thr=0.68\n")
        for k,v in metrics.items():
            f.write(f"- {k}: {v}\n")
        f.write("\n[Per-Conversation] thr=0.68\n")
        for k,v in m_conv.items():
            f.write(f"- {k}: {v}\n")

    print("Saved:", OUT_DIR / "crisis_turns.csv")
    print("Saved:", OUT_DIR / "summary.txt")

if __name__ == "__main__":
    main()

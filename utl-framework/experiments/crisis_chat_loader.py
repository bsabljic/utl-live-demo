"""
Generic crisis chat loader + evaluator.
Usage:
    python experiments/crisis_chat_loader.py --file path/to.csv --map linguistic=colA,behavioral=colB,temporal=colC,resilience=colD,label=labelCol,conv=conversation_id,turn=turn
If --map omitted, defaults to demo_synthetic.csv schema.
"""
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
from utl.detector import UTLDetector

DEFAULTS = {
    "conv": "conversation_id",
    "turn": "turn",
    "linguistic": "linguistic_hazard",
    "behavioral": "behavioral_hazard",
    "temporal": "temporal_hazard",
    "resilience": "resilience_score",
    "label": "crisis_label",
}

def parse_map(s: str):
    m = DEFAULTS.copy()
    if not s:
        return m
    for pair in s.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            m[k.strip()] = v.strip()
    return m

def evaluate(y_true, y_score, thr=0.68):
    y_pred = (y_score > thr).astype(int)
    tp = int(((y_pred==1) & (y_true==1)).sum())
    fp = int(((y_pred==1) & (y_true==0)).sum())
    tn = int(((y_pred==0) & (y_true==0)).sum())
    fn = int(((y_pred==0) & (y_true==1)).sum())
    prec = tp / (tp+fp) if (tp+fp)>0 else 0.0
    rec = tp / (tp+fn) if (tp+fn)>0 else 0.0
    acc = (tp+tn) / max(1, len(y_true))
    f1 = 2*prec*rec/(prec+rec) if (prec+rec)>0 else 0.0
    return dict(precision=prec, recall=rec, f1=f1, accuracy=acc, tp=tp, fp=fp, tn=tn, fn=fn)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="CSV path")
    ap.add_argument("--map", default="", help="column mapping e.g. linguistic=X,behavioral=Y,temporal=Z,resilience=R,label=Y,conv=C,turn=T")
    ap.add_argument("--thr", type=float, default=0.68, help="hazard threshold")
    ap.add_argument("--outdir", default="results", help="output directory")
    args = ap.parse_args()

    mp = parse_map(args.map)
    df = pd.read_csv(args.file).sort_values([mp["conv"], mp["turn"]]).reset_index(drop=True)

    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    det = None
    last_conv = None
    for _, row in df.iterrows():
        conv = row[mp["conv"]]
        if last_conv is None or conv != last_conv:
            det = UTLDetector()
            last_conv = conv
        feats = {
            "linguistic": float(row[mp["linguistic"]]),
            "behavioral": float(row[mp["behavioral"]]),
            "temporal": float(row[mp["temporal"]]),
            "resilience": float(row[mp["resilience"]]),
        }
        hazard, crisis = det.update(feats)
        rows.append({
            mp["conv"]: conv,
            mp["turn"]: int(row[mp["turn"]]),
            "hazard": hazard,
            "label": int(row[mp["label"]]),
        })
    res = pd.DataFrame(rows)
    res.to_csv(outdir / "loader_turns.csv", index=False)

    metrics = evaluate(res["label"].values, res["hazard"].values, thr=args.thr)

    with open(outdir / "loader_summary.txt", "w", encoding="utf-8") as f:
        f.write("=== UTL Loader Summary ===\n")
        for k, v in metrics.items():
            f.write(f"- {k}: {v}\n")

    print("Saved:", outdir / "loader_turns.csv")
    print("Saved:", outdir / "loader_summary.txt")

if __name__ == "__main__":
    main()

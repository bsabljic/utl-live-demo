"""
Ablation studies for UTL (synthetic demo).
- Loads data/demo_synthetic.csv
- Runs detector with selected feature channels zeroed out.
- Saves table CSV with metrics for each ablation setting.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from utl.detector import UTLDetector

DATA = Path("data/demo_synthetic.csv")
OUT = Path("results/ablations.csv")
THR = 0.68

ABLATIONS = [
    ("full_model", {"ling":True, "beh":True, "tmp":True, "res":True}),
    ("no_linguistic", {"ling":False, "beh":True, "tmp":True, "res":True}),
    ("no_behavioral", {"ling":True, "beh":False, "tmp":True, "res":True}),
    ("no_temporal", {"ling":True, "beh":True, "tmp":False, "res":True}),
    ("no_resilience", {"ling":True, "beh":True, "tmp":True, "res":False}),
]

def evaluate(y_true, y_score, thr=THR):
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

def run_variant(name, flags, df):
    det = UTLDetector()
    hazards = []
    for _, row in df.iterrows():
        ling = float(row["linguistic_hazard"]) if flags["ling"] else 0.0
        beh = float(row["behavioral_hazard"]) if flags["beh"] else 0.0
        tmp = float(row["temporal_hazard"]) if flags["tmp"] else 0.0
        res = float(row["resilience_score"]) if flags["res"] else 0.0
        h, c = det.update({"linguistic": ling, "behavioral": beh, "temporal": tmp, "resilience": res})
        hazards.append(h)
    m = evaluate(df["crisis_label"].values.astype(int), np.array(hazards), thr=THR)
    m.update(name=name, mean_hazard=float(np.mean(hazards)), max_hazard=float(np.max(hazards)))
    return m

def main():
    assert DATA.exists(), f"Missing {DATA}"
    df = pd.read_csv(DATA).sort_values(["conversation_id","turn"]).reset_index(drop=True)
    rows = []
    for name, flags in ABLATIONS:
        rows.append(run_variant(name, flags, df))
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print("Saved", OUT)

if __name__ == "__main__":
    main()

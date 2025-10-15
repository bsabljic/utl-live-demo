
<p align="left">
  <a href="https://github.com/bsabljic/utl-framework/actions">
    <img alt="CI" src="https://img.shields.io/github/actions/workflow/status/bsabljic/utl-framework/ci.yml?branch=main">
  </a>
  <a href="https://www.python.org/">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.11-blue">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg">
  </a>
</p>
[![DOI](https://zenodo.org/badge/DOI/10.0000/zenodo.placeholder.svg)](https://doi.org/10.0000/zenodo.placeholder)


# UTL Framework: Temporal Risk Detection in Conversational AI

**Paper**: "Temporal Risk Detection in Conversational AI: An EWMA-Based Framework with Cross-Domain Validation"  
**Author**: Branimir Sabljić  
**Status**: Under review (October 2025)

## Overview
UTL (Universal Transition Law) framework for real-time crisis detection in conversational AI systems using EWMA-based hazard accumulation and multi-signal coherence.

## Installation
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

## Quick Start
```python
from utl.detector import UTLDetector

# Initialize detector
detector = UTLDetector(alpha=0.15, theta_mult=1.5, gamma=1.5)

# Process conversation turn (toy example)
features = {
    "linguistic": 0.4,
    "behavioral": 0.3,
    "temporal": 0.2,
    "resilience": 0.5
}
hazard, crisis = detector.update(features)
print(hazard, crisis)
```

## Reproducibility (Minimal Demo)
Run a minimal end-to-end simulation:
```bash
python experiments/demo.py
```

This prints turn-by-turn hazard values, flags the first crisis detection, and estimates a recovery window.

## Data Availability
- **Crisis Text Line** data is not included due to privacy. See `data/README.md` for guidance and a synthetic demo CSV.
- **Financial data** can be fetched via Yahoo Finance (see comments in code for pointers).

## Citation
```bibtex
@article{sabljic2025utl,
  title={{Temporal Risk Detection in Conversational AI: An EWMA-Based Framework with Cross-Domain Validation}},
  author={{Sablji{{c}}}, Branimir},
  journal={arXiv preprint},
  year={2025}
}
```

## License
MIT License with **Ethical Use Addendum** (see `LICENSE`).

## Contact
- branimir.sabljic@gmail.com
- typotecture.design@gmail.com

## Acknowledgments
Crisis Text Line for dataset access. See paper for full acknowledgments.

## Reproduce Synthetic Crisis Chat Results
```bash
python experiments/crisis_chat.py
# Outputs:
#  - results/crisis_turns.csv
#  - results/summary.txt
```

## Make Figures (from synthetic results)
```bash
python experiments/figures.py
# Saves PNGs to figures/
```

## Financial Cross-Domain Demo
```bash
# Online (yfinance)
python experiments/financial.py SPY
python experiments/financial.py TSLA
python experiments/financial.py BTC-USD

# Offline (CSV fallback placed in data/)
python experiments/financial.py SPY
```


## Dev hooks (pre-commit)
```bash
pip install pre-commit
pre-commit install
# run on all files
pre-commit run --all-files
```

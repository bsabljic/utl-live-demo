"""
Generate all figures (synthetic + paper-style) in one pass.
Requires results/crisis_turns.csv. If missing, runs crisis_chat first.
"""
from pathlib import Path
import runpy

if not Path('results/crisis_turns.csv').exists():
    runpy.run_path('experiments/crisis_chat.py', run_name='__main__')

# Standard figures
runpy.run_path('experiments/figures.py', run_name='__main__')
# Paper-style figures
runpy.run_path('experiments/figures_paper.py', run_name='__main__')

print('All figures generated. See ./figures and ./paper')

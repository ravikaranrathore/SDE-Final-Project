"""
CLI Script: evaluate_model_impact.py
Simulates and reports the impact of data quality defects on LineVul classification metrics.
"""
import os
import argparse
import pandas as pd
import numpy as np
from src.models.linevul_evaluator import compute_metrics, simulate_cross_set_deduplication_impact

def run_impact_simulation():
    print('='*70)
    print('   DOWNSTREAM LINEVUL IMPACT SIMULATION (RQ2 REPLICATION)')
    print('='*70)
    
    # Paper published benchmarks (Table 5 & Table 6)
    results = [
        {'Dataset': 'Big-Vul', 'Experiment': 'Duplicate Removal (Uniqueness)', 'Raw_MCC': 0.830, 'Clean_MCC': 0.829, 'Delta': '0.0%'},
        {'Dataset': 'Devign', 'Experiment': 'Duplicate Removal (Uniqueness)', 'Raw_MCC': 0.284, 'Clean_MCC': 0.244, 'Delta': '-13.9%'},
        {'Dataset': 'D2A', 'Experiment': 'Duplicate Removal (Uniqueness)', 'Raw_MCC': 0.774, 'Clean_MCC': 0.141, 'Delta': '-81.7% (Collapse!)'},
        {'Dataset': 'Juliet', 'Experiment': 'Duplicate Removal (Uniqueness)', 'Raw_MCC': 0.909, 'Clean_MCC': 0.814, 'Delta': '-10.4%'},
        {'Dataset': 'D2A', 'Experiment': 'Inconsistency Filter (Consistency)', 'Raw_MCC': 0.000, 'Clean_MCC': 0.748, 'Delta': 'Full Recovery'}
    ]
    df_res = pd.DataFrame(results)
    print(df_res.to_string(index=False))
    print('='*70)
    print('\nKey Demonstration on Simulated Test Set:')
    # Simulate cross-set duplicate leakage
    np.random.seed(42)
    n = 200
    y_true = np.random.binomial(1, 0.2, n)
    y_pred = y_true.copy()
    
    # Make cross-set duplicates trivial to classify
    is_cross_dup = np.zeros(n, dtype=bool)
    is_cross_dup[:120] = True # 60% are cross-set duplicates
    
    # On non-duplicate samples, model makes mistakes
    noise_idx = np.random.choice(np.where(~is_cross_dup)[0], size=30, replace=False)
    y_pred[noise_idx] = 1 - y_pred[noise_idx]
    
    sim = simulate_cross_set_deduplication_impact(y_true, y_pred, is_cross_dup)
    print(f'Raw Metrics (with duplicates):     MCC = {sim["Raw"]["MCC"]}, Recall = {sim["Raw"]["Recall"]}, Precision = {sim["Raw"]["Precision"]}')
    print(f'Clean Metrics (without duplicates): MCC = {sim["Cleaned"]["MCC"]}, Recall = {sim["Cleaned"]["Recall"]}, Precision = {sim["Cleaned"]["Precision"]}')
    print(f'Observed MCC Inflation Drop:        {sim["MCC_Change_Percent"]}%\n')

if __name__ == '__main__':
    run_impact_simulation()

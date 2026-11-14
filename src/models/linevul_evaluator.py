"""
Module: linevul_evaluator.py
Computes classification metrics (Precision, Recall, F1, MCC) and evaluates downstream impact.
"""
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, matthews_corrcoef

def compute_metrics(y_true, y_pred):
    """
    Computes Precision, Recall, F1-Score, and Matthews Correlation Coefficient (MCC).
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    # Handle zero division edge cases safely
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    mcc = matthews_corrcoef(y_true, y_pred)
    
    return {
        'Precision': round(prec, 4),
        'Recall': round(rec, 4),
        'F1': round(f1, 4),
        'MCC': round(mcc, 4)
    }

def simulate_cross_set_deduplication_impact(y_true, y_pred, is_cross_duplicate):
    """
    Simulates removing cross-set duplicate test samples that match training samples.
    Demonstrates the severe drop in MCC and Recall when memorized duplicates are removed.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    is_dup = np.asarray(is_cross_duplicate, dtype=bool)
    
    # Raw benchmark (with duplicates)
    raw_metrics = compute_metrics(y_true, y_pred)
    
    # Cleaned benchmark (cross duplicates removed from test set)
    non_dup_idx = ~is_dup
    clean_metrics = compute_metrics(y_true[non_dup_idx], y_pred[non_dup_idx])
    
    mcc_change = 0.0
    if raw_metrics['MCC'] > 0:
        mcc_change = (clean_metrics['MCC'] - raw_metrics['MCC']) / raw_metrics['MCC'] * 100.0
        
    return {
        'Raw': raw_metrics,
        'Cleaned': clean_metrics,
        'MCC_Change_Percent': round(mcc_change, 2)
    }

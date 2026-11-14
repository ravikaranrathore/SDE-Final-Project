"""
Module: accuracy.py
Evaluates label correctness and thematic categorization of label errors.
"""
import pandas as pd
import numpy as np

def calculate_accuracy(df_samples):
    """
    Compute empirical accuracy ratio: dq(i) = 1 if correctly labeled, 0 otherwise.
    Formula: Accuracy = sum(dq(i)) / N
    """
    if 'Label_Correct' not in df_samples.columns:
        raise ValueError("Dataset must contain 'Label_Correct' column indicating ground truth correctness.")
    total = len(df_samples)
    if total == 0:
        return 0.0
    correct = (df_samples['Label_Correct'] == 1).sum()
    return correct / total

def compute_thematic_error_distribution(df_samples):
    """
    Categorizes errors into the 3 paper themes:
    - Irrelevant code changes (style, refactoring, comments, tangled edits)
    - Cleanup changes (defensive null checks, secondary parameter modifications)
    - Inaccurate vulnerability fix identification (failed tracing, tool false alarm)
    """
    errors = df_samples[df_samples['Label_Correct'] == 0]
    total_errors = len(errors)
    if total_errors == 0:
        return {'Irrelevant': 0.0, 'Cleanup': 0.0, 'Inaccurate': 0.0}
    
    counts = errors['Error_Theme'].value_counts()
    return {
        'Irrelevant': counts.get('Irrelevant', 0) / total_errors,
        'Cleanup': counts.get('Cleanup', 0) / total_errors,
        'Inaccurate': counts.get('Inaccurate', 0) / total_errors
    }

def cohen_kappa_score(rater1, rater2):
    """
    Calculates inter-rater agreement between two independent expert annotators.
    """
    rater1 = np.asarray(rater1)
    rater2 = np.asarray(rater2)
    po = np.mean(rater1 == rater2)
    p_yes1 = np.mean(rater1 == 1)
    p_yes2 = np.mean(rater2 == 1)
    pe = (p_yes1 * p_yes2) + ((1 - p_yes1) * (1 - p_yes2))
    if pe == 1:
        return 1.0
    return (po - pe) / (1 - pe)

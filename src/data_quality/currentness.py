"""
Module: currentness.py
Measures concept drift using Jensen-Shannon Divergence across historical commit dates.
"""
import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
import re

def get_token_frequency_distribution(functions):
    vocab = {}
    total_tokens = 0
    for func in functions:
        if not isinstance(func, str):
            continue
        tokens = re.findall(r'[A-Za-z_][A-Za-z0-9_]*', func)
        for t in tokens:
            vocab[t] = vocab.get(t, 0) + 1
            total_tokens += 1
            
    if total_tokens == 0:
        return {}
    return {k: v / total_tokens for k, v in vocab.items()}

def calculate_currentness(df):
    """
    Splits dataset chronologically into older half and newer half.
    Calculates Jensen-Shannon Divergence (JSD).
    Currentness = 1.0 - JSD (bounded between 0 and 1).
    """
    if 'Date' not in df.columns:
        return 1.0
        
    df_valid = df[df['Date'].notnull() & (df['Date'] != '-')].copy()
    if len(df_valid) < 10:
        return 1.0
        
    df_valid['Date'] = pd.to_datetime(df_valid['Date'], errors='coerce')
    df_valid = df_valid.dropna(subset=['Date']).sort_values('Date')
    
    mid = len(df_valid) // 2
    old_half = df_valid.iloc[:mid]['Function'].tolist()
    new_half = df_valid.iloc[mid:]['Function'].tolist()
    
    dist_old = get_token_frequency_distribution(old_half)
    dist_new = get_token_frequency_distribution(new_half)
    
    all_words = list(set(dist_old.keys()).union(set(dist_new.keys())))
    p = np.array([dist_old.get(w, 1e-12) for w in all_words])
    q = np.array([dist_new.get(w, 1e-12) for w in all_words])
    
    p = p / np.sum(p)
    q = q / np.sum(q)
    
    jsd = jensenshannon(p, q, base=2)
    return max(0.0, 1.0 - jsd)

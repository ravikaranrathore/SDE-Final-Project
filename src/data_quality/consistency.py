"""
Module: consistency.py
Detects contradictory class labels where identical code has conflicting labels.
"""
import pandas as pd
from collections import defaultdict
from .uniqueness import normalize_code

def find_inconsistent_instances(df):
    """
    Groups normalized functions and detects cases where Vulnerable has both 0 and 1.
    """
    func_map = defaultdict(list)
    for idx, row in df.iterrows():
        norm = normalize_code(row['Function'])
        func_map[norm].append((row['UID'], int(row['Vulnerable'])))
    
    inconsistent_uids = []
    inconsistent_clusters = []
    
    for norm, instances in func_map.items():
        if len(instances) > 1 and norm != "":
            labels = set(lbl for _, lbl in instances)
            if 0 in labels and 1 in labels:
                inconsistent_clusters.append(instances)
                inconsistent_uids.extend(uid for uid, _ in instances)
                
    return inconsistent_clusters, inconsistent_uids

def calculate_consistency(df):
    """Consistency = 1 - (Inconsistent records / Total records)"""
    total = len(df)
    if total == 0:
        return 1.0
    _, inconsistent_uids = find_inconsistent_instances(df)
    return max(0.0, 1.0 - (len(inconsistent_uids) / total))

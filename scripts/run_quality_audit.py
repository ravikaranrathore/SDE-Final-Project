"""
Main CLI Script: run_quality_audit.py
Runs the ISO/IEC 25012 Inherent Data Quality audit across specified datasets.
"""
import os
import argparse
import pandas as pd
from src.data_quality.accuracy import calculate_accuracy, compute_thematic_error_distribution
from src.data_quality.uniqueness import find_duplicate_clusters, calculate_uniqueness
from src.data_quality.consistency import calculate_consistency, find_inconsistent_instances
from src.data_quality.completeness import calculate_completeness
from src.data_quality.currentness import calculate_currentness

def audit_dataset(name, filepath):
    if not os.path.exists(filepath):
        print(f'Error: File not found: {filepath}')
        return
        
    df = pd.read_csv(filepath)
    print('='*70)
    print(f'   ISO/IEC 25012 AUDIT REPORT FOR: {name.upper()}')
    print('='*70)
    print(f'Total Function Records: {len(df)}')
    print(f'Vulnerable Ratio: {df["Vulnerable"].mean():.2%}')
    print('-'*70)
    
    # 1. Accuracy
    acc = calculate_accuracy(df)
    thematic = compute_thematic_error_distribution(df)
    print(f'1. Accuracy Score:     {acc:.3f}')
    print(f'   - Irrelevant Edits: {thematic["Irrelevant"]:.1%}')
    print(f'   - Cleanup Edits:    {thematic["Cleanup"]:.1%}')
    print(f'   - Inaccurate Fix:   {thematic["Inaccurate"]:.1%}')
    
    # 2. Uniqueness
    dup_clusters = find_duplicate_clusters(df, type_clone=1)
    uniq = calculate_uniqueness(df, dup_clusters)
    print(f'2. Uniqueness Score:   {uniq:.3f} (Clusters: {len(dup_clusters)})')
    
    # 3. Consistency
    inconsist_clusters, inconsist_uids = find_inconsistent_instances(df)
    cons = calculate_consistency(df)
    print(f'3. Consistency Score:  {cons:.3f} (Conflicting Records: {len(inconsist_uids)})')
    
    # 4. Completeness
    comp = calculate_completeness(df)
    print(f'4. Completeness Score: {comp:.3f}')
    
    # 5. Currentness
    curr = calculate_currentness(df)
    print(f'5. Currentness Score:  {curr:.3f}')
    print('='*70 + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Audit Software Vulnerability Datasets')
    parser.add_argument('--dataset', type=str, default='all', choices=['Big-Vul', 'D2A', 'all'],
                        help='Dataset to audit')
    args = parser.parse_args()
    
    sample_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples')
    
    if args.dataset in ['Big-Vul', 'all']:
        audit_dataset('Big-Vul (Vendor-provided sample)', os.path.join(sample_dir, 'big_vul_sample.csv'))
    if args.dataset in ['D2A', 'all']:
        audit_dataset('D2A (Tool-created sample)', os.path.join(sample_dir, 'd2a_sample.csv'))

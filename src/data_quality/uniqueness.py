"""
Module: uniqueness.py
Evaluates code clone duplication across Type-1, Type-2, and Type-3 clones.
"""
import re
from collections import defaultdict

def normalize_code(code_str):
    """Strip comments, extraneous whitespace and newlines for Type-1 matching."""
    if not isinstance(code_str, str):
        return ""
    # Strip multi-line and single-line comments
    code_str = re.sub(r'/\*.*?\*/', '', code_str, flags=re.DOTALL)
    code_str = re.sub(r'//.*', '', code_str)
    # Normalize whitespace
    code_str = re.sub(r'\s+', ' ', code_str).strip()
    return code_str

def tokenize_code(code_str):
    """Extract lexical word/syntax tokens."""
    clean = normalize_code(code_str)
    return set(re.findall(r'[A-Za-z_][A-Za-z0-9_]*|==|!=|<=|>=|->|\+\+|--|[^\w\s]', clean))

def jaccard_similarity(tokens_a, tokens_b):
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = len(tokens_a.intersection(tokens_b))
    union = len(tokens_a.union(tokens_b))
    return intersection / union if union > 0 else 0.0

def find_duplicate_clusters(df, type_clone=1, similarity_threshold=0.85):
    """
    Finds clusters of duplicate functions.
    Type 1: Exact syntactic match after normalization.
    Type 3: High token Jaccard similarity.
    """
    clusters = []
    seen = set()
    rows = df.to_dict('records')
    
    if type_clone == 1:
        exact_map = defaultdict(list)
        for r in rows:
            norm = normalize_code(r['Function'])
            exact_map[norm].append(r['UID'])
        for norm, uids in exact_map.items():
            if len(uids) > 1 and norm != "":
                clusters.append(uids)
    else:
        tokens_list = [(r['UID'], tokenize_code(r['Function'])) for r in rows]
        for i in range(len(tokens_list)):
            uid_i, tok_i = tokens_list[i]
            if uid_i in seen:
                continue
            curr_cluster = [uid_i]
            for j in range(i + 1, len(tokens_list)):
                uid_j, tok_j = tokens_list[j]
                if uid_j in seen:
                    continue
                if jaccard_similarity(tok_i, tok_j) >= similarity_threshold:
                    curr_cluster.append(uid_j)
                    seen.add(uid_j)
            if len(curr_cluster) > 1:
                clusters.append(curr_cluster)
                seen.add(uid_i)
    return clusters

def calculate_uniqueness(df, clusters):
    """
    Uniqueness = 1 - (Number of redundant duplicate instances / Total instances)
    """
    total = len(df)
    if total == 0:
        return 1.0
    redundant = sum(len(c) - 1 for c in clusters)
    return max(0.0, 1.0 - (redundant / total))

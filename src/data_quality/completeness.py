"""
Module: completeness.py
Identifies syntactic truncation (START, END, or EMPTY function bodies).
"""
import re

def check_function_truncation(func_str):
    """
    Inspects whether a C/C++ function snippet suffers from:
    - 'START': Truncated return type or missing function name signature.
    - 'END': Truncated body missing final closing braces.
    - 'EMPTY': Pure declaration without implementation body.
    - 'NONE': Syntactically complete.
    """
    if not isinstance(func_str, str) or not func_str.strip():
        return 'EMPTY'
        
    code = func_str.strip()
    status = ''
    
    # Check start signature
    first_line = code.splitlines()[0].strip()
    if '(' in first_line:
        pre_paren = first_line.rsplit('(', 1)[0].strip()
        # If no whitespace before opening paren, likely truncated multi-line return type
        if ' ' not in pre_paren:
            status += 'START'
            
    # Check end braces
    clean_end = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL).rstrip()
    clean_end = re.sub(r'//.*', '', clean_end).rstrip()
    if not (clean_end.endswith('}') or clean_end.endswith('};')):
        status += 'END'
        
    # Check empty declaration (e.g., int foo();)
    if '{' not in code and code.endswith(';'):
        return 'DECLARATION'
        
    return 'NONE' if status == '' else status

def calculate_completeness(df):
    """Completeness = (Total - Incomplete functions) / Total"""
    total = len(df)
    if total == 0:
        return 1.0
    truncations = df['Function'].apply(check_function_truncation)
    incomplete_count = (truncations != 'NONE').sum()
    return max(0.0, (total - incomplete_count) / total)

import pandas as pd
import numpy as np

# Sample data representing Big-Vul archetype
big_vul_samples = [
    {'UID': 101, 'Function': 'int process_header(char *buf, int len) {\n    char dest[64];\n    strcpy(dest, buf);\n    return 0;\n}', 'Vulnerable': 1, 'Date': '2018-04-12', 'Label_Correct': 1, 'Error_Theme': 'None'},
    {'UID': 102, 'Function': 'int process_header(char *buf, int len) {\n    char dest[64];\n    strcpy(dest, buf);\n    return 0;\n}', 'Vulnerable': 1, 'Date': '2018-04-12', 'Label_Correct': 1, 'Error_Theme': 'None'}, # Type 1 clone
    {'UID': 103, 'Function': 'int update_flags(struct ctx *c, int fl) {\n    c->flags = fl;\n    return 1;\n}', 'Vulnerable': 1, 'Date': '2018-06-20', 'Label_Correct': 0, 'Error_Theme': 'Irrelevant'}, # Tangled refactor
    {'UID': 104, 'Function': 'void cleanup_handle(void *ptr) {\n    if (ptr) ptr = NULL;\n}', 'Vulnerable': 1, 'Date': '2019-01-15', 'Label_Correct': 0, 'Error_Theme': 'Cleanup'}, # Auxiliary null check
    {'UID': 105, 'Function': 'static inline int get_val(int x) {\n    return x * 2;\n}', 'Vulnerable': 0, 'Date': '2019-02-10', 'Label_Correct': 1, 'Error_Theme': 'None'},
    {'UID': 106, 'Function': 'parse_packet(uint8_t *pkt, size_t sz) {\n    memcpy(global_buf, pkt, sz);\n}', 'Vulnerable': 1, 'Date': '2019-03-01', 'Label_Correct': 1, 'Error_Theme': 'None'}, # Truncated return type
    {'UID': 107, 'Function': 'int compute_crc(const char *data) {\n    return 0xAA;\n}', 'Vulnerable': 0, 'Date': '2019-05-18', 'Label_Correct': 1, 'Error_Theme': 'None'},
    {'UID': 108, 'Function': 'int compute_crc(const char *data) {\n    return 0xAA;\n}', 'Vulnerable': 1, 'Date': '2019-07-22', 'Label_Correct': 0, 'Error_Theme': 'Inaccurate'}, # Conflicting label!
]
df_bv = pd.DataFrame(big_vul_samples)
df_bv.to_csv(r'C:\Users\Ravikaran Singh\.gemini\antigravity\scratch\Software_Vulnerability_Data_Quality_Project\github_repository\data\samples\big_vul_sample.csv', index=False)

# Sample data representing D2A archetype (High duplication, high inconsistency)
d2a_samples = []
for i in range(1, 20):
    # Clones of function A across commits
    d2a_samples.append({'UID': 200+i, 'Function': 'void handle_connection(int sock) {\n    char temp[128];\n    read(sock, temp, 256);\n}', 'Vulnerable': 1 if i < 10 else 0, 'Date': f'2020-0{i%9+1}-10', 'Label_Correct': 0, 'Error_Theme': 'Inaccurate'})
for i in range(21, 35):
    d2a_samples.append({'UID': 200+i, 'Function': f'int calculate_offset_{i}(int a) {{\n    return a + {i};\n}}', 'Vulnerable': 0, 'Date': '2020-10-15', 'Label_Correct': 1, 'Error_Theme': 'None'})
df_d2a = pd.DataFrame(d2a_samples)
df_d2a.to_csv(r'C:\Users\Ravikaran Singh\.gemini\antigravity\scratch\Software_Vulnerability_Data_Quality_Project\github_repository\data\samples\d2a_sample.csv', index=False)
print('Generated test sample datasets.')

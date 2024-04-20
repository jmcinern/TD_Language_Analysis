import pandas as pd
from scipy import stats

# Load data from the saved file
df = pd.read_csv('scores.csv')

# Group by source
grouped = df.groupby('Source')

# Extract lexical and structural complexity scores for each source
lex_by_source = {source: group['Lexical_Complexity'].tolist() for source, group in grouped}
struc_by_source = {source: group['Structural_Complexity'].tolist() for source, group in grouped}

# Perform Kruskal-Wallis test for Lexical Complexity
lex_kw_stat, lex_kw_p_value = stats.kruskal(*lex_by_source.values())

print("Kruskal-Wallis Test for Lexical Complexity:")
print("Test Statistic:", lex_kw_stat)
print("p-value:", lex_kw_p_value)

# Perform Kruskal-Wallis test for Structural Complexity
struc_kw_stat, struc_kw_p_value = stats.kruskal(*struc_by_source.values())

print("\nKruskal-Wallis Test for Structural Complexity:")
print("Test Statistic:", struc_kw_stat)
print("p-value:", struc_kw_p_value)

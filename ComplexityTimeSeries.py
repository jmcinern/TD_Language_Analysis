import pandas as pd
from lexicalrichness import LexicalRichness
from scipy.stats import mannwhitneyu
import spacy
import itertools
import numpy as np
import concurrent.futures

nlp = spacy.load("en_core_web_sm")

def ratio_of_clauses_per_t_unit(row):
    text = nlp(row['Text'])

    t_unit_count = 0
    # Loop through sentences split by spaCy dependency parser
    for sn in text.sents:
        t_unit_count += 1
        in_cconj = False
        for token in sn:
            if token.pos_ == 'CCONJ':
                in_cconj = True
            # identify if there is a verb in the coordinating conjunction clause
            if token.pos_ == 'VERB' and in_cconj:
                t_unit_count += 1
                in_cconj = False

    v_fin_count = 0
    # t units
    for token in text:
        if 'VerbForm=Fin' in token.morph:
            v_fin_count += 1

    if t_unit_count > 0:
        return (t_unit_count + v_fin_count) / t_unit_count

    else:
        return np.nan

# Function to calculate Moving Average Type Token Ratio (MATTR)
# This function calculates TTR for each sliding window of text
def MATTR(text, windowsize):
    # split text on white space
    text = text.split()
    #print(len(text))
    # list of words in text
    words = []
    print('TEXT')
    print(text)
    for token in text:
        if token.isalpha():
            words.append(token)
    print('WORDS')
    print(words)


    # don't calculate MATTR if text less than window size
    if len(words) <= windowsize:
        return np.nan
    # Otherwise calculate MATTR
    else:
        # list to store TTR for each window
        TTR_values = []
        # Calculate the TTR for each window
        for i in range(len(words) - windowsize + 1):
            # Get words in window
            window_words = words[i:i + windowsize]
            types = set(window_words)
            TTR_values.append(len(types) / windowsize)

        # Calculate moving average TTR for text
        MATTR = np.mean(TTR_values)
        return MATTR



def process_source(group_df):
    lex_scores = group_df['Text'].apply(MATTR, windowsize=25).tolist()
    struc_scores = group_df.apply(ratio_of_clauses_per_t_unit, axis=1).tolist()
    return lex_scores, struc_scores

def perform_mannwhitneyu(group1, group2):
    mw_stat, mw_p_value = mannwhitneyu(group1, group2)
    return mw_stat, mw_p_value

corpus_df = pd.read_csv('corpus_output.tsv', sep='\t')

grouped = corpus_df.groupby('Source')

# Extract lexical and structural complexity scores for each source
lex_by_source = {source: group['Text'].apply(MATTR, windowsize=50).dropna().tolist() for source, group in grouped}

struc_by_source = {source: group.apply(ratio_of_clauses_per_t_unit, axis=1).dropna().tolist() for source, group in grouped}
# Perform Mann-Whitney U test between each pair of sources for lexical complexity
lex_mw_results = {}
for source1, source2 in itertools.combinations(lex_by_source.keys(), 2):
    mw_stat, mw_p_value = perform_mannwhitneyu(lex_by_source[source1], lex_by_source[source2])
    lex_mw_results[(source1, source2)] = (mw_stat, mw_p_value)

# Perform Mann-Whitney U test between each pair of sources for structural complexity
struc_mw_results = {}
for source1, source2 in itertools.combinations(struc_by_source.keys(), 2):
    mw_stat, mw_p_value = perform_mannwhitneyu(struc_by_source[source1], struc_by_source[source2])
    struc_mw_results[(source1, source2)] = (mw_stat, mw_p_value)

# Print results for lexical complexity
print("Mann-Whitney U Test Results for Lexical Complexity:")
for (source1, source2), (mw_stat, mw_p_value) in lex_mw_results.items():
    print(f"Comparison between {source1} and {source2}:")
    print("Test Statistic:", mw_stat)
    print("p-value:", mw_p_value)
    print()

# Print results for structural complexity
print("Mann-Whitney U Test Results for Structural Complexity:")
for (source1, source2), (mw_stat, mw_p_value) in struc_mw_results.items():
    print(f"Comparison between {source1} and {source2}:")
    print("Test Statistic:", mw_stat)
    print("p-value:", mw_p_value)
    print()

def save_to_csv(scores_by_source, filename_prefix):
    for source, scores in scores_by_source.items():
        df = pd.DataFrame({source: scores})
        df.to_csv(f"{filename_prefix}_{source}_scores.csv", index=False)

save_to_csv(lex_by_source, 'lexical_complexity')
save_to_csv(struc_by_source, 'structural_complexity')

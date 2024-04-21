import pandas as pd
from scipy.stats import mannwhitneyu
import spacy
import numpy as np

nlp = spacy.load("en_core_web_sm")


def structural_complexity(text):
    text = nlp(text)

    main_clause_count = 0
    t_unit_count = 0
    clause = False
    fin_verb = False
    subj = False
    # split sentences using dependency parser (spaCy)
    for sn in text.sents:
        main_clause_count += 1
        in_cconj = False
        subj_in_cconj = False
        prev_pos = None
        for token in sn:
            # count clauses
            if 'VerbForm=Fin' in token.morph:
                fin_verb = True

            if token.dep_ == 'nsubj':
                subj = True

            if fin_verb and subj:
                clause = True
                subj = False
                fin_verb = False

            # count of main clauses and subordinate clauses (t_units)
            if clause:
                t_unit_count += 1
                clause = False

            # split main clauses connected by cconj and increase t-unit count
            if token.pos_ == 'SCONJ' and prev_pos != 'CCONJ':
                in_cconj = False
            if token.pos_ == 'CCONJ':
                in_cconj = True
            # identify if there is a subj in the clause
            if token.dep_ == 'nsubj' and in_cconj:
                subj_in_cconj = True
            # identify if there is a finite verb in the coordinating conjunction clause
            if 'VerbForm=Fin' in token.morph and in_cconj and subj_in_cconj:
                fin_verb_in_cconj = True
                in_cconj = False
                subj_in_cconj = False
                main_clause_count += 1
            prev_pos = token.pos_

    complexity = t_unit_count / main_clause_count
    if complexity < 1 or main_clause_count < 5:
        return np.nan
    else:
        return complexity


# Function to calculate Moving Average Type Token Ratio (MATTR)
# This function calculates TTR for each sliding window of text
def MATTR(text, windowsize):
    # split text on white space
    text = text.split()
    # list of words in text
    words = []
    for token in text:
        if token.isalpha():
            words.append(token)

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
    struc_scores = group_df['Text'].apply(structural_complexity).tolist()

    # Make all lists of equal length by padding with NaNs
    max_length = max(len(lex_scores), len(struc_scores))
    lex_scores += [np.nan] * (max_length - len(lex_scores))
    struc_scores += [np.nan] * (max_length - len(struc_scores))

    return lex_scores, struc_scores


corpus_df = pd.read_csv('corpus_output.tsv', sep='\t')

grouped = corpus_df.groupby('Source')

# Extract lexical and structural complexity scores for each source
lex_by_source = {source: group['Text'].apply(MATTR, windowsize=50).dropna().tolist() for source, group in grouped}
struc_by_source = {source: group['Text'].apply(structural_complexity).dropna().tolist() for source, group in grouped}

# Process scores to ensure equal length lists
lex_scores_list, struc_scores_list = zip(*[process_source(group_df) for _, group_df in grouped])

# Save lexical and structural complexity scores to CSV
lex_df = pd.DataFrame(lex_scores_list).transpose()
lex_df.columns = lex_by_source.keys()
lex_df.to_csv('lexical_complexity_scores.csv', index=False)

struc_df = pd.DataFrame(struc_scores_list).transpose()
struc_df.columns = struc_by_source.keys()
struc_df.to_csv('structural_complexity_scores.csv', index=False)

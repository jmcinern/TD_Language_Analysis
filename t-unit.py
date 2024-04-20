import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
import nltk
from nltk.tokenize import sent_tokenize

# Class to calculate average clauses per t-unit in text
t1 = "I like the movie we saw about Moby Dick, the white whale."
t2 = "The captain said if you can kill the white whale, Moby Dick, and it is worth sixteen dollars."
t3 = "And it is worth sixteen dollars."
t4 = 'They tried and tried.'
# gap filler
t5 = 'But while they were trying they killed a whale and used the oil for the lamps'
t6 = 'They almost caught the white whale'
tx = "I like the movie we saw about Moby Dick, the white whale. The captain said if you can kill the white whale, Moby Dick. And it is worth sixteen dollars. But while they were trying they killed a whale and used the oil for the lamps. They almost caught the white whale. They tried and tried."
tn = 'I like pizza and chicken or chocolate'


def subordinate_count(text):
    v_fin_count = 0
    # t units
    for token in text:
        if 'VerbForm=Fin' in token.morph:
            v_fin_count += 1
            #print(token.text)

    return v_fin_count

# takes string, splits on full stop / ?


conj = "I like pizza and cake"
conjcc = "I like and hate pizza"
conj2 = "I like pizza and the man likes cake because he is cool." #1 extra t-unit
conj3 = 'I like pizza and the man likes cake and cheese' #one extra t-unit
text = nlp(conjcc)





t_unit_count = 0
# Loop through sentences split by spaCy dependency parser
for sn in text.sents:
    t_unit_count += 1
    in_cconj = False
    fin_verb_in_cconj = False
    subj_in_cconj = False

    for token in sn:
        print(token.text)
        print(f'cconj: {in_cconj}')
        print(f'subj: {subj_in_cconj}')
        print(f'fin: {fin_verb_in_cconj}')
        if token.pos_ == 'CCONJ':
            in_cconj = True
        # identify if there is a subj in the clause
        if token.dep_ == 'nsubj' and in_cconj:
            subj_in_cconj = True
        # identify if there is a finite verb in the coordinating conjunction clause
        if 'VerbForm=Fin' in token.morph and in_cconj and subj_in_cconj:
            fin_verb_in_cconj = True
            in_cconj = False
            t_unit_count +=1




fin_count = subordinate_count(text)
print(f"main clauses: {t_unit_count}")
print(f"subordinate clauses: {fin_count}")



#main + sub / main
print(f"Complexity: {(t_unit_count + fin_count) /t_unit_count}")




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


# Main + subord
def clause_count(text):
    v_fin_count = 0
    nsubj_count = 0
    clause_count = 0
    # t units
    for token in text:
        if 'VerbForm=Fin' in token.morph:
            #print(token.text)
            v_fin_count += 1
            #print(token.text)
        if token.dep_ == 'nsubj':
            nsubj_count +=1



    clause_count = min(v_fin_count, nsubj_count)

    return clause_count

# takes string, splits on full stop / ?

conj = "I like pizza and cake"
conjcc = "I like and hate pizza"
conj2 = "I like pizza and the man likes cake because he is cool." #1 extra t-unit
conj3 = 'I like pizza and the man likes cake and cheese' #one extra t-unit
conj4 = 'I am not sure whether I should go to the shop or not as it is already late'
alltext = ("""I like the movie we saw about Moby Dick, the white whale. The captain said if you can kill the white whale,
           Moby Dick, I Will give this gold to the one that can do it and it is worth sixteen dollars. 
           They tried and tried but while they were trying they killed a whale and used the oil for the lamps. They almost caught the white whale.""")

# Loop through sentences split by spaCy dependency parser
def structural_complexity(text):
    t_unit_count = 0
    fin_count = clause_count(text)
    complexity = 1
    for sn in text.sents:
        print(sn)
        t_unit_count += 1
        in_cconj = False
        fin_verb_in_cconj = False
        subj_in_cconj = False
        prev_pos = None
        for token in sn:
            print(token.dep_)

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

                t_unit_count +=1
            prev_pos = token.pos_

    complexity = fin_count / t_unit_count
    print(fin_count)
    print(t_unit_count)
    return complexity

complexity = structural_complexity(nlp(alltext))
print(complexity)













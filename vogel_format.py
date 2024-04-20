from datetime import datetime

import pandas as pd
import sys

raw_corpus = {
    "name": [],
    "party": [],
    "age": [],
    "constituency": [],
    "forum": [],
    "speeches": [],
    "questions": [],
    "answers": [],
    "formal media": [],
    "social media": [],
    "language": [],
    "date of content": [],
    "topic": [],
    "speaking_order": []
}

def add_record(name, party, age, constituency, forum, speeches, questions, answers, formal_media, social_media, language, date_of_content, topic, speaking_order):
    raw_corpus["name"].append(name)
    raw_corpus["party"].append(party)
    raw_corpus["age"].append(age)
    raw_corpus["constituency"].append(constituency)
    raw_corpus["forum"].append(forum)
    raw_corpus["speeches"].append(speeches)
    raw_corpus["questions"].append(questions)
    raw_corpus["answers"].append(answers)
    raw_corpus["formal media"].append(formal_media)
    raw_corpus["social media"].append(social_media)
    raw_corpus["language"].append(language)
    raw_corpus["date of content"].append(date_of_content)
    raw_corpus["topic"].append(topic)
    raw_corpus["speaking_order"].append(speaking_order)

luke_in = pd.read_csv("DATA/Leo-Varadkar.D.2007-06-14_limit5000.tsv", sep='\t')

def get_years_difference(date1_str, date2_str):
    date1 = datetime.strptime(date1_str, "%Y-%m-%d")
    date2 = datetime.strptime(date2_str, "%Y-%m-%d")
    difference = date2 - date1
    years = difference.days / 365.25  # considering leap years
    return int(years)

for index, row in luke_in.iterrows():
    age = get_years_difference(sys.argv[4], row['date'])
    add_record(sys.argv[1], sys.argv[2], age, sys.argv[3], row['house_no'], row['contribution'], row['contribution'], row['contribution'], "", "", "English", row['date'], row['debate_section_topic'], row['order_in_discourse'])

out = pd.DataFrame(raw_corpus)
out.to_csv('data/vogel_formatted.tsv', sep="\t")
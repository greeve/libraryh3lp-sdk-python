#!/usr/bin/env python

# import-faq.py
# -------------
# Bulk import a list of questions and answers into a LibraryH3lp FAQ.
# Expects a CSV file with columns corresponding to question, answer,
# and a list of topic tags.  Topics in the topic list column are
# separated by a semicolon.


import csv
import lh3.api
import sys

def format_topics(topics):
    return map(lambda topic: topic.strip(), topics.split(';'))

# Takes one command line argument, FAQ ID.
faq_id = sys.argv[1]

client = lh3.api.Client()
faq = client.one('faqs', faq_id).all('questions')

with open('faq.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for question, answer, topics in reader:
        faq.post(dict(question = question, answer = answer, topics = format_topics(topics)))

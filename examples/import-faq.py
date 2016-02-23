#!/usr/bin/env python

# import-faq.py
# -------------
# Bulk import a list of questions and answers into a LibraryH3lp FAQ.
# Expects a CSV file with columns corresponding to question, answer,
# expiration date (may be empty), and a list of topic tags.

import csv
import lh3.api

MY_FAQ_ID = 1234

client = lh3.api.Client()
faq = client.one('faqs', MY_FAQ_ID).all('questions')

with open('faq.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for question, answer, expires, *topics in reader:
        faq.post(dict(question = question, answer = answer, expires = expires, topics = topics))

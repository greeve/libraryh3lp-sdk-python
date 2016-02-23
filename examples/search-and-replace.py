#!/usr/bin/env python

# search-and-replace.py
# ---------------------
# Perform a search and replace operation across all your FAQs.

import lh3.api
import sys

faq_id, pattern, substitution = sys.argv

client = lh3.api.Client()
questions = client.one('faqs', faq_id).all('questions')

for question in questions.get_list()
    details = questions.one(question['id']).get()
    answer = question['answer'].replace_all(pattern, substitution)
    questions.one(question['id'].patch({'answer': answer})

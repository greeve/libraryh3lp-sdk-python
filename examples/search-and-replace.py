#!/usr/bin/env python

# search-and-replace.py
# ---------------------
# Perform a search and replace operation across all your FAQs (answer text only,
# not question text).

import lh3.api
import sys

# Takes three command line arguments, FAQ ID, search pattern, replacement text.
faq_id, pattern, substitution = sys.argv[1:]

client = lh3.api.Client()
questions = client.one('faqs', faq_id).all('questions')

for question in questions.get_list():
    details = questions.get(question['id'])
    answer = details['answer'].replace(pattern, substitution)
    questions.patch(question['id'], {'answer': answer})

#!/usr/bin/env python

# faq-usage.py
# ------------
# Download a record of FAQ views and searches.

import lh3.api
import sys

# Takes one command line argument, FAQ ID.
faq_id = sys.argv[1]

client = lh3.api.Client()
faq = client.one('faqs', faq_id)

for question in faq.all('questions').get_list():
    print('{question} views: {views} likes: {likes} dislikes: {dislikes}'.format(**question))

for search in faq.all('searches').get_list():
    print('{timestamp} {search}'.format(**search))

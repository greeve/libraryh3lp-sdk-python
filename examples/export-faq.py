#!/usr/bin/env python

# export-faq.py
# -------------
# Bulk export of questions and answers from a LibraryH3lp FAQ.
#
# Produces a CSV file with columns corresponding to question, answer,
# list of topic tags, views, likes, and dislikes.
#
# Topics in the topic list column are separated by a semicolon.


import csv
import lh3.api
import sys

# Takes one command line argument, FAQ ID.
faq_id = sys.argv[1]

def encode_html(html, encoding = 'utf-8'):
    '''
    Using Windows-1252 for encoding may yield better results when importing
    into MS Excel. Otherwise is probably best to stick with unicode.
    '''
    formatted = html.replace('&#13;', u'\u000D')
    return formatted.encode(encoding=encoding, errors='ignore')

def format_topics(topics):
    return map(lambda topic: topic.strip(), topics.split(';'))

client = lh3.api.Client()
faq = client.one('faqs', faq_id)

with open('faq-export.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, dialect=csv.excel)

    writer.writerow(('question', 'answer', 'topics', 'views', 'likes', 'dislikes'))

    for question in faq.all('questions').get_list():
        answer = faq.one('questions', question['id']).get()
        writer.writerow((encode_html(question['question']),
                         encode_html(answer['answer']),
                         ';'.join(question['topics']),
                         str(question['views']),
                         str(question['likes']),
                         str(question['dislikes'])))

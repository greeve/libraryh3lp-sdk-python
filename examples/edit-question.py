#!/usr/bin/env python

# edit-question.py
# ----------------
# Edit your FAQ in the console.  Because consoles rock.

from subprocess import call

import lh3.api
import os
import sys
import tempfile

# Takes two command line arguments, FAQ ID and Question ID.
faq_id, question_id = sys.argv[1:]

client = lh3.api.Client()
question = client.one('faqs', faq_id).one('questions', question_id).get(params = {'format': 'json'})

EDITOR = os.environ.get('EDITOR', 'vim')

_, temp = tempfile.mkstemp(suffix = '.tmp')

with open(temp, 'w') as f:
    f.write(question['answer'])
    f.flush()

call([EDITOR, temp])

with open(temp, 'r') as f:
    answer = f.read()
    client.one('faqs', faq_id).one('questions', question_id).patch({'answer': answer})

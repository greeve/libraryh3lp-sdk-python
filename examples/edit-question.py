#!/usr/bin/env python

# edit-question.py
# ----------------
# Edit your FAQ in the console.  Because consoles rock.

from subprocess import call

import lh3.api
import os
import sys
import tempfile

faq_id, question_id = sys.argv

client = lh3.api.Client()
question = client.one('faqs', faq_id).one('questions', question_id).get(format = 'json')

EDITOR = os.environ.get('EDITOR', 'vim')

with tempfile.NamedTemporaryFile(suffix = '.tmp') as tempfile:
    tempfile.write(question['answer'])
    tempfile.flush()
    call([EDITOR, tempfile.name])

    with file(tempfile) as f:
        answer = f.read()
        client.one('faqs', faq_id).one('questions', question_id).patch({'answer': answer})

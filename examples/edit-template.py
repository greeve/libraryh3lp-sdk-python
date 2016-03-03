#!/usr/bin/env python

# edit-template.py
# ----------------
# Edit your FAQs templates in the console.  Because consoles rock.

from subprocess import call

import lh3.api
import os
import sys
import tempfile

# Takes two command line arguments, FAQ ID and template name.
faq_id, template_name = sys.argv[1:]

# Lazy typers don't need to add the .html extension on the template name.
if template_name.find('.html') == -1:
    template_name += '.html'
template_name = unicode(template_name, 'utf-8')

client = lh3.api.Client()
templates = client.one('faqs', faq_id).all('templates').get_list(params = {'format': 'json'})
template = (template for template in templates if template['name'] == template_name).next()

EDITOR = os.environ.get('EDITOR', 'vim')

_, temp = tempfile.mkstemp(suffix = '.tmp')

with open(temp, 'w') as f:
    f.write(template['content'])
    f.flush()

call([EDITOR, temp])

with open(temp, 'r') as f:
    content = f.read()
    client.one('faqs', faq_id).one('templates', template['id']).patch({'content': content})

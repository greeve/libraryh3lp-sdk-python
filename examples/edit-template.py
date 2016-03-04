#!/usr/bin/env python

# edit-template.py
# ----------------
# Edit your FAQs templates in the console.  Because consoles rock.

from cursesmenu import SelectionMenu
from subprocess import call

import argparse
import lh3.api
import os
import sys
import tempfile

parser = argparse.ArgumentParser(description = 'Edit a FAQ template')
parser.add_argument('-f', '--faq', help = 'faq name')
parser.add_argument('-t', '--template', help = 'template name')

args = parser.parse_args()
client = lh3.api.Client()

faqs = client.all('faqs').get_list()
if args.faq:
    faq = (faq for faq in faqs if faq['name'] == faq_name).next()
else:
    selection = SelectionMenu.get_selection([f['name'] for f in faqs])
    faq = faqs[selection]

faq_id = faq['id']
templates = client.one('faqs', faq_id).all('templates').get_list(params = {'format': 'json'})
if args.template:
    template_name = args.template
    if template_name.find('.html') == -1:
        template_name += '.html'
    template_name = unicode(template_name, 'utf-8')
    template = (template for template in templates if template['name'] == template_name).next()
else:
    selection = SelectionMenu.get_selection([t['name'] for t in templates])
    template = templates[selection]

EDITOR = os.environ.get('EDITOR', 'vim')

_, temp = tempfile.mkstemp(suffix = '.tmp')

with open(temp, 'w') as f:
    f.write(template['content'])
    f.flush()

call([EDITOR, temp])

with open(temp, 'r') as f:
    content = f.read()
    client.one('faqs', faq_id).one('templates', template['id']).patch({'content': content})

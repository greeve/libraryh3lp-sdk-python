#!/usr/bin/env python

# user-editor.py
# --------------
# Interactively browse and edit your users.

from cursesmenu import SelectionMenu
from subprocess import call

import argparse
import lh3.api
import os
import sys
import tempfile

parser = argparse.ArgumentParser(description = 'Edit users')
parser.add_argument('-u', '--username', help = 'user name')

args = parser.parse_args()
client = lh3.api.Client()

users = client.all('users').get_list()
if args.username:
    user = next(user for user in users if user['name'] == args.username)
else:
    selection = SelectionMenu.get_selection([user['name'] for user in users])
    user = users[selection]

details = client.api().get('v1', '/users/{}'.format(user['id']))
print(details)

_, temp = tempfile.mkstemp(suffix = '.tmp')
with open(temp, 'w') as f:
    f.write("name: {}\n".format(user['name']))
    for k, v in details.items():
        f.write("{}: {}\n".format(k, v))
    f.write("password:\n")
    f.flush()

EDITOR = os.environ.get('EDITOR', 'vim')
call([EDITOR, temp])

with open(temp, 'r') as f:
    json = {}
    for line in f.readlines():
        k, v = line.split(':')
        if v.strip():
            json[k.strip()] = v.strip()
    client.api().put('v1', '/users/{}'.format(user['id']), json = json)

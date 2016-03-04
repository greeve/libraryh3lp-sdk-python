#!/usr/bin/env python

# create-sdk-user.py
# ------------------
# Create a user for SDK access.  This allows for more restrictive
# permission settings and provides isolation against admin password
# changes.

import argparse
import getpass
import hashlib
import lh3.api

parser = argparse.ArgumentParser(description = 'Create a dedicated user for SDK access.  Can auto-generate both name and password.')
parser.add_argument('-u', '--username', help = 'create a user with this login identity')
parser.add_argument('-g', '--group', help = 'use this name for the permissions group')
parser.add_argument('-p', '--prompt', help = 'prompt for a password for the new user', action = 'store_true')

args = parser.parse_args()
client = lh3.api.Client()

if args.username:
    username = args.username
else:
    username = client.api().username + '-sdk-user'

if args.prompt:
    password = getpass.getpass('Enter a password for the user: ')
else:
    password = hashlib.sha256((client.api().salt + username).encode('UTF-8')).hexdigest()

# Find the top-level folders.
folders = client.api().get('v1', '/queues', params = {'node': 0})

# Find or create the permissions group.
group_name = args.group or 'SDK Users'
group = None
for g in client.all('groups').get_list():
    if g['name'] == group_name:
        group = g
        break
else:
    group = client.all('groups').post({'name': group_name})

group_id = group['id']

# Grant permissions to the group.
for folder in folders:
    if folder['type'] != 'folder':
        continue

    folder_id = -folder['id']
    client.one('groups', group_id).one('aces', folder_id).patch({'grant': ['read', 'write']})

# Create the user.
users = client.api().post('v1', '/users', json = {
    'name': username,
    'password': password,
    'type': 'user',
    'parent_id': folders[0]['id']
})
user = users[0]
user_id = user['id']

# Add user to permissions group.
client.one('groups', group_id).all('members').post({'id': user_id})
print('created user with name ' + user['name'])

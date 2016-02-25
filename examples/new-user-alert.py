#!/usr/bin/env python

# new-user-alert.py
# -----------------
# Get notified of new users.

import json
import lh3.api

DATAFILE = '/var/lib/lh3/users.txt'

prev_users = []
try:
    with open(DATAFILE) as f:
        prev_users = json.load(f)
except:
    pass
prev_ids = [u['id'] for u in prev_users]

client = lh3.api.Client()
users = client.all('users').get_list()

for user in users:
    if user['id'] not in prev_ids:
        print('{} is a new user account, it may need attention'.format(user['name']))

with open(DATAFILE, 'wb') as f:
    json.dump(users, f)

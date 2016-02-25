#!/usr/bin/env python

# in-out-board.py
# ---------------
# Who's around?

import requests

USERS = ['dilbert', 'dogbert', 'ratbert']

for user in USERS:
    url = 'http://libraryh3lp.com/presence/jid/{}/libraryh3lp.com/text'.format(user)
    result = requests.get(url)
    status = result.text
    if status != 'unavailable':
        print('{} is {}'.format(user, status))

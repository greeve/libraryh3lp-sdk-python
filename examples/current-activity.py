#!/usr/bin/env python

# current-activity.py
# -------------------
# Count the number of active chats and the number of librarians that
# are staffing services.

from datetime import datetime

import lh3.api

client = lh3.api.Client()

# Fetch today's chats.
now = datetime.now()
chats = client.chats().list_day(now.year, now.month, now.day)

num_active = 0
num_unanswered = 0
for chat in chats:
    if chat['ended']:
        continue

    # Only count those starting in the last 15 minutes.
    started = datetime.strptime(chat['started'], '%Y-%m-%d %H:%M:%S')
    if (now - started).total_seconds() >= 900:
        continue

    if chat['accepted']:
        num_active += 1
    else:
        num_unanswered += 1

print('{} active chats, {} unanswered'.format(num_active, num_unanswered))

# For each user...
client.set_options(version = 'v1')
users = client.all('users')
num_users = 0
for user in users.get_list():
    if user['show'] != u'chat' and user['show'] != u'available':
        continue

    # Is that user staffing any queue?
    staffing = False
    assignments = users.one(user['id']).all('assignments').get_list()
    for assignment in assignments:
        if assignment['enabled']:
            staffing = True

    # If so, then great!
    if staffing:
        num_users += 1

print('{} online operators'.format(num_users))

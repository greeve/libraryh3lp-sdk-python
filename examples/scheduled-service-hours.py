#!/usr/bin/env python

# scheduled-service-hours.py
# --------------------------
# Opt users into and out of queues on a schedule.  Opting a user out
# of a queue will not interrupt chats in progress.

from datetime import datetime

import lh3.api

SCHEDULE = [
    [0, { 'refqueue': []}],
    [8, {'refqueue': ['alice', 'bob']}],
    [12, {'refqueue': ['bob', 'charles']}],
    [16, {'refqueue': ['alice', 'charles']}],
    [20, { 'refqueue': []}]
]

client = lh3.api.Client()
hour = datetime.now().hour

def enable_queue(queue, operators):
    assignments = client.find_queue_by_name(queue).all('operators')
    for assignment in assignments.get_list():
        enabled = assignment['name'] in operators
        if enabled != assignment['enabled']:
            assignments.one(assignment['id']).patch({'enabled': enabled})

for i in range(len(SCHEDULE)):
    curr = SCHEDULE[i]
    next = None
    if i < len(SCHEDULE) - 1:
        next = SCHEDULE[i + 1]

    if curr[0] <= hour and (next is None or hour < next[0]):
        for queue, operators in curr[1].items():
            enable_queue(queue, operators)

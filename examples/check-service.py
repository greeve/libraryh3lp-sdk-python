#!/usr/bin/env python

# check-service.py
# ----------------
# Look to see if your services are online and, if not, why not.  Also
# reports if you have too few operators staffing.  Meant to be called
# occasionally during service hours by cron (so that cron can email
# you if there is a problem).

import lh3.api
import requests

QUEUES = ['reference', 'ill']
MIN_OPERATORS = 2

# Librarians are considered available if their status is chatty
# or available.
def is_available(operator):
    status = operator['show']
    return status == u'chat' or status == u'available'

# Librarians are considered to be actively staffing a queue if they are
# available and they are opted into the queue assignment.
def is_staffing(operator):
    return is_available(operator) and operator['enabled']

# Find the number of librarians that are staffing queues, and the
# number that are currently available to handle new chats.
def count_operators(client, queue):
    num_staffing = 0
    num_available = 0

    operators = client.find_queue_by_name(queue).all('operators').get_list()
    for operator in operators:
        if is_staffing(operator):
            num_staffing += 1
        if is_available(operator):
            num_available += 1

    return dict(num_staffing = num_staffing, num_available = num_available)

# Print an alert if not enough librarians are available.
def check_min_operators(client, queue):
    operators = count_operators(client, queue)
    if operators['num_staffing'] < MIN_OPERATORS:
        print('  only {num_staffing} operators staffing the queue'.format(**operators))
    if operators['num_available'] < MIN_OPERATORS:
        print('  only {num_available} operators are available'.format(**operators))

# Why is my service offline?
def why_offline(client, queue):
    operators = count_operators(client, queue)
    if operators['num_staffing'] == 0:
        print('  nobody is staffing the queue')
    elif operators['num_available'] == 0:
        print('  nobody is available to take questions')

def check_queue(client, queue):
    result = requests.get('http://libraryh3lp.com/presence/jid/{}/chat.libraryh3lp.com/text'.format(queue))
    status = result.text
    if status == 'chat' or status == 'available':
        print('{} is available: {}'.format(queue, status))
        check_min_operators(client, queue)
    else:
        print('{} is not available: {}'.format(queue, status))
        why_offline(client, queue)

def main():
    client = lh3.api.Client()
    for queue in QUEUES:
        check_queue(client, queue)

if __name__ == '__main__':
    main()

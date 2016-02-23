#!/usr/bin/env python

# kill-switch.py
# --------------
# Somebody forgot to log out.  Take the queue offline so patrons don't
# mistakenly think you're available.

import lh3.api

def engage(queue_name):
    client = lh3.api.Client()
    queue = client.find_queue_by_name(queue_name)
    operators = queue.all('operators').get_list()
    for operator in operators:
        status = operator['userShow']
        if status == 'chat' or status == 'available':
            print('{} forgot to log out!'.format(operator['user']))
            queue.one('operators', operator['id']).patch({'enabled': False})

if __name__ = __main__:
    engage('my-queue')

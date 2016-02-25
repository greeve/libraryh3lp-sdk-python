#!/usr/bin/env python

# kill-switch.py
# --------------
# Somebody forgot to log out.  Take the queue offline so patrons don't
# mistakenly think you're available.

import lh3.api
import sys

def engage(name):
    client = lh3.api.Client()
    queue = client.find_queue_by_name(name)
    operators = queue.all('operators').get_list()
    for operator in operators:
        status = operator['show']
        if status == 'chat' or status == 'available':
            print('{} forgot to log out!'.format(operator['name']))
            queue.one('operators', operator['id']).patch({'enabled': False})

if __name__ == '__main__':
    name = sys.argv[1]
    engage(name)

#!/usr/bin/env python

# new-user-setup.py
# -----------------
# Create a new user, automatically adding it to queues, conference rooms,
# canned message pools, and setting up buddy relationships.

import lh3.api
import sys

name, password, email = sys.argv[1:]

# Create the user.
client = lh3.api.Client()
client.set_options(version = 'v1')

user = client.all('users').post({'name': name, 'password': password})[0]
client.one('users', user['id']).patch({'email': email})

# Add the user to all queues.
for queue in client.all('queues').get_list():
    client.one('queues', queue['id']).all('operators').post({'userId': user['id']})

def roster_user(name):
    return dict(name = name, subscription = 'B', groups = '')

# Ensure everybody is buddied to everybody else.
users = client.all('users').get_list()
queues = client.all('queues').get_list()
client.one('contacts', user['name']).post(None, {
    'users': [roster_user(u['name']) for u in users],
    'queues': [roster_user(q['name']) for q in queues],
    'reciprocal': True,
    'comprehensive': True
})

# Add the user to all conference rooms.
client.set_options(version = 'v2')
for room in client.all('rooms').get_list():
    client.one('rooms', room['id']).all('users').post({'id': user['id']})

# Add the user to all canned message pools.
for pool in client.all('pools').get_list():
    client.one('pools', pool['id']).all('users').post({'id': user['id']})

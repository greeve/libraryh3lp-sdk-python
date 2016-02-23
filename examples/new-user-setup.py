#!/usr/bin/env

# new-user-setup.py
# -----------------
# Create a new user, automatically adding it to queues and setting up
# buddy relationships.

import lh3.api
import sys

name, password, email = sys.argv[1:]

# Create the user.
client = lh3.api.Client()
user = client.all('users').post({'name': name, 'password': password})
client.one('users', user['id']).patch({'email': email})

# Add the user to all queues.
for queue in client.all('queues').get_list():
    client.one('queues', queue['id']).all('operators').post({'userId': user['id']})

# Ensure everybody is buddied to everybody else.
users = client.all('users').get_list()
queues = client.all('queues').get_list()
client.one('contacts', user['name']).custom_post({
    'users': [u['name'] for u in users],
    'queues': [q['name'] for q in queues],
    'subscription': 'B',
    'reciprocal': True,
    'comprehensive': True
})

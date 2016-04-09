#!/usr/bin/env python

# one-shot.py
# -------
# Send a guest-initiated a call-out to a queue or user. When someone answers
# the call-out, the guest is notified and the response is shown to the guest.
#
# Usage: ./one-shot.py queue-name

import configparser
import os
import requests
import sys

from threading import Thread

def get_config(profile = None):
    config = configparser.SafeConfigParser(dict(server='libraryh3lp.com'))
    config.read([os.path.expanduser('~/.lh3/config')])

    options = config.defaults().copy()
    options.update(dict(config.items('default')))
    if config.has_section(profile):
        options.update(dict(config.items(profile)))

    return options

def maybe_json(result):
    try:
        return result.json()
    except ValueError as e:
        return result.text

def run_box(box):
    try:
        box.run()
    except:
        pass

def main():
    # Takes one command line argument, a queue name.
    queue = sys.argv[1]

    config = get_config()
    server = config['server']
    url = 'https://{}/widget/oneshot'.format(server)

    print "Notifying librarian.  Please wait."

    # Send the callout to the librarian.
    message = 'The call button has been pressed.  A patron needs help!'
    response = maybe_json(requests.post(url, data=dict(to='{}@chat.{}'.format(queue, server), body=message)))

    if not isinstance(response, dict):
        print "ERROR!  Aborting request."
        print response
        return

    guest = response[u'jid']

    # Wait for a response from the librarian.
    reply = None
    while not reply:
      response = maybe_json(requests.get(url, params=dict(jid=guest), timeout=25))
      reply = response[u'body'] if isinstance(response, dict) and response.has_key(u'body') else response

    print 'Librarian responded: {}'.format(reply)

if __name__ == '__main__':
    main()

#!/usr/bin/env python

# biff.py
# -------
# Poll 3mail for new messages and send notifications to the terminal.
# See https://www.freebsd.org/cgi/man.cgi?query=biff
#
# Usage: ./biff.py &

from datetime import datetime

import lh3.api
import time

# Fetch all email threads, including their read status and the time of
# the last message.
def current_threads(client, mailboxes):
    threads = client.all('emails').get_list({'mailboxes[]': mailboxes})
    for t in threads:
        t['updated'] = datetime.strptime(t['updated'], '%Y-%m-%d %I:%M %p')
    return threads

# Return only those threads we have not seen before.
def new_or_updated(prev_threads, threads):
    prev = {t['id']: t['updated'] for t in prev_threads}
    return [t for t in threads if not t['read'] and t['updated'] > prev.get(t['id'], datetime.min)]

# Summarize the new activity on the console.
def notify_user(threads):
    print('New messages in {} threads'.format(len(threads)))
    for t in threads:
        print('{subject} from {guest}'.format(**t))

def main():
    client = lh3.api.Client()
    mailboxes = [m['id'] for m in client.all('emails').get_list('mailboxes')]

    prev_threads = current_threads(client, mailboxes)
    while True:
        time.sleep(300)
        threads = current_threads(client, mailboxes)
        new_threads = new_or_updated(prev_threads, threads)
        notify_user(new_threads)
        prev_threads = threads

if __name__ == '__main__':
    main()

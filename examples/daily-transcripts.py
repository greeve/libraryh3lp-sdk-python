#!/usr/bin/env python

# daily-transcripts.py
# --------------------
# Each morning, forward all of yesterday's chats to the inbox.

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import lh3.api
import smtplib

INBOX = 'inbox@email.library.edu'

client = lh3.api.Client()

# Fetch yesterday's chats.
yesterday = datetime.today() - timedelta(days = 1)
chats = client.chats().list_day(yesterday.year, yesterday.month, yesterday.day)

for chat in chats:
    # Download the chat transcript.
    id = chat['id']
    transcript = client.one('chats', id).get()

    # Forward it via email.
    message = MIMEMultipart('alternative')
    message['From'] = INBOX
    message['To'] = INBOX
    message['Subject'] = 'Chat {} on {}/{}/{}'.format(id, yesterday.year, yesterday.month, yesterday.day)
    html = MIMEText('transcript', 'html')
    message.attach(html)
    s = smtplib.SMTP('localhost')
    s.sendmail(INBOX, INBOX, message.as_string())
    s.quit()

#!/usr/bin/env python

# scheduled-reports.py
# --------------------
# Let's summarize last week's activity.

from datetime import datetime, timedelta

import lh3.api

today = datetime.today()
monday = today - timedelta(days = today.weekday())
last_monday = (monday - timedelta(days = 7)).strftime('%Y-%m-%d')
last_sunday = (monday - timedelta(days = 1)).strftime('%Y-%m-%d')

client = lh3.api.Client()
chats_per_operator = \
    client.reports().chats_per_operator(start = last_monday, end = last_sunday)

print(chats_per_operator)

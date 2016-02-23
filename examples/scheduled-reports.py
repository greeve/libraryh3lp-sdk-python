#!/usr/bin/env python

# scheduled-reports.py
# --------------------
# Let's summarize last week's activity.

from datetime import datetime, timedelta

import lh3

today = datetime.today()
monday = today - timedelta(days = today.weekday())
last_monday = monday - timedelta(days = 7)
last_sunday = monday - timedelta(days = 1)

client = lh3.api.Client()
chats_per_operator = \
    client.all('reports').custom_get('chats-per-operator', dict(start = last_monday, end = last_sunday)

print(chats_per_operator)

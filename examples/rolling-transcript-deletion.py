#!/usr/bin/env python

# rolling-transcript-deletion.py
# ------------------------------
# Each morning, delete the transcripts from a month ago.

from datetime import datetime, timedelta

import lh3.api

client = lh3.api.Client()
delete_day = datetime.today() - timedelta(days = 30)
chats = client.chats().list_day(delete_day.year, delete_day.month, delete_day.day)
ids = [c['id'] for c in chats]
client.chats().delete_transcripts(ids)

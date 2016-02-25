#!/usr/bin/env python

# csv-transcripts.py
# ------------------
# Flatten and escape transcripts suitable for inclusion in a csv file
# and import into excel.

from datetime import date

import csv
import lh3.api
import requests
import sys
import tempfile
import zipfile

client = lh3.api.Client()
today = date.today()
chats = client.chats().list_day(today.year, today.month, today.day)
ids = [c['id'] for c in chats]

writer = csv.writer(sys.stdout)

with tempfile.TemporaryFile() as f:
    client.chats().download_xml(ids, f)
    f.seek(0)

    zip = zipfile.ZipFile(f)
    for entry in zip.infolist():
        xml = zip.read(entry)
        writer.writerow([xml])

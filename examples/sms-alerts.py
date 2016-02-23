#!/usr/bin/env python

# sms-alerts.py
# -------------
# LibraryH3lp SMS integrates with Twilio.  You can either send staff
# alerts by SMS, or you can send notices to patrons.  Patron replies
# will automatically be routed in chat or 3mail.

from twilio.rest import TwilioRestClient

account = 'ACXXXXXXXXXXXXXXXXX'
token = 'YYYYYYYYYYYYYYYYYY'
client = TwilioRestClient(account, token)

client.messages.create(
    to = '+12316851234', from_ = '+15555555555', body = 'your books are late!!!')

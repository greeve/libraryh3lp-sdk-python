#!/usr/bin/env python

# chat-bot.py
# -----------
# Don't leave patrons hanging.  Get to them with an automated response
# even if everyone is busy.

import sleekxmpp
import sys

class ChatBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        super(ChatBot, self).__init__(jid, password)
        self.add_event_handler('message', self.message)
        self.add_event_handler('session_start', self.session_start)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        pass

if __name__ == '__main__':
    jid, password = sys.argv[1:]

    bot = ChatBot(jid, password)
    bot.register_plugin('xep_0199')

    if bot.connect():
        bot.process(block = True)
